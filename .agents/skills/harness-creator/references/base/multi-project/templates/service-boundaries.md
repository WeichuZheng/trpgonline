# Service Boundaries: [Service Name]

> Defines what this service owns, its responsibilities, and integration points
> Version: [major.minor.patch]
> Last Updated: [DATE]

---

## Service Identity

### Service Name
`[service-id]`

### Description
[2-3 sentences describing the service's purpose in the system]

### Domain
[Business domain this service belongs to: e.g., User Management, Order Processing, Payment]

### Criticality
CRITICAL | HIGH | MEDIUM | LOW

---

## Ownership

### Data Ownership

| Data Entity | CRUD Rights | Source of Truth | Shared With |
|-------------|------------|-----------------|-------------|
| User | CRUD | This service | Read-only: order-service |
| UserPreferences | CRUD | This service | None |
| UserSession | CRD | This service | None |

### Business Capability Ownership

| Capability | Description | Owner |
|------------|-------------|-------|
| User Registration | Create new user accounts | This service |
| User Authentication | Validate user credentials | This service |
| Profile Management | Update user profiles | This service |
| Password Reset | Handle password recovery | This service |

### Process Ownership

| Process | Trigger | Owner | Participants |
|---------|---------|-------|---------------|
| User Onboarding | User created event | This service | notification, analytics |
| Account Deletion | Delete request | This service | order, payment, notification |
| Password Change | User request | This service | notification |

---

## API Boundaries

### Public APIs (External Consumers)

| Endpoint | Purpose | Stability |
|----------|---------|-----------|
| `POST /users` | Create user account | Stable |
| `GET /users/{id}` | Get user profile | Stable |
| `PUT /users/{id}` | Update user profile | Stable |
| `DELETE /users/{id}` | Delete user account | Stable |

### Internal APIs (Service-to-Service)

| Endpoint | Purpose | Consumer Services |
|----------|---------|-------------------|
| `GET /internal/users/{id}/validate` | Validate user exists | order, payment |
| `POST /internal/users/batch` | Batch user lookup | analytics |

### Events Produced

| Event | Purpose | Schema | Consumers |
|-------|---------|--------|-----------|
| `user.created` | New user account | [schema-link] | notification, analytics |
| `user.updated` | Profile updated | [schema-link] | notification, analytics |
| `user.deleted` | Account deleted | [schema-link] | order, payment, notification |

### Events Consumed

| Event | Purpose | Producer | Processing |
|-------|---------|----------|------------|
| `order.completed` | Track user orders | order-service | Async, at-least-once |
| `payment.failed` | Update user status | payment-service | Async, at-least-once |

---

## Data Boundaries

### Primary Database

| Database | Type | Purpose | Access Pattern |
|----------|------|---------|----------------|
| `users_db` | PostgreSQL | User profiles | CRUD |
| `sessions_db` | Redis | Session storage | Key-Value, TTL |

### Tables Owned

| Table | Purpose | Retention | Access |
|-------|---------|-----------|--------|
| `users` | User profiles | Indefinite | This service only |
| `user_preferences` | User settings | Indefinite | This service only |
| `sessions` | Active sessions | 7 days | This service only |

### Tables Accessed (Read-Only)

| Table | Owner Service | Purpose | Access |
|-------|---------------|---------|--------|
| `orders` | order-service | User order history | Read replica |

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────>│  This       │────>│  Database   │
│   App       │     │  Service    │     │  (owned)    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           │ Events
                           v
                    ┌─────────────┐
                    │  Message    │
                    │  Bus       │
                    └─────────────┘
                           │
              ┌────────────┼────────────┐
              v            v            v
       ┌───────────┐ ┌───────────┐ ┌───────────┐
       │notification│ │ analytics │ │  order    │
       │  service  │ │  service  │ │  service  │
       └───────────┘ └───────────┘ └───────────┘
```

---

## Integration Patterns

### Synchronous Integration

| Consumer | Protocol | Purpose | SLA |
|----------|----------|---------|-----|
| frontend-app | REST | User operations | p99 < 200ms |
| mobile-app | REST | User operations | p99 < 300ms |
| order-service | gRPC | User validation | p99 < 50ms |

### Asynchronous Integration

| Consumer | Event | Purpose | Guarantee |
|----------|-------|---------|-----------|
| notification | user.created | Send welcome email | At-least-once |
| analytics | user.* | Track user events | At-least-once |

### Failure Modes

| Dependency | Failure Mode | Response | Fallback |
|------------|--------------|----------|----------|
| Database | Connection failure | Return 503 | Retry with backoff |
| Cache | Cache miss | Query database | No degradation |
| Message Bus | Publish failure | Retry 3x | Log and continue |

---

## Scaling Boundaries

### Horizontal Scaling

| Metric | Scale-Out Threshold | Scale-In Threshold |
|--------|---------------------|-------------------|
| CPU | > 70% for 5 min | < 30% for 10 min |
| Memory | > 80% for 5 min | < 40% for 10 min |
| Requests | > 1000 req/sec per instance | < 100 req/sec per instance |

### Vertical Scaling

| Environment | CPU | Memory | Instances |
|-------------|-----|--------|-----------|
| Development | 1 core | 512MB | 1 |
| Staging | 2 cores | 2GB | 2 |
| Production | 4 cores | 8GB | 3-10 |

### Rate Limits

| Consumer | Rate Limit | Burst | Reason |
|----------|-----------|-------|--------|
| Anonymous | 10/min | 20 | Prevent abuse |
| Authenticated | 100/min | 200 | Fair usage |
| Service Account | 1000/min | 2000 | High-volume |

---

## Security Boundaries

### Authentication Requirements

| Endpoint Type | Auth Required | Method |
|---------------|---------------|--------|
| Public API | Yes | JWT |
| Internal API | Yes | mTLS |
| Health Check | No | None |

### Authorization Model

| Role | Permissions |
|------|--------------|
| User | Read/Write own data |
| Admin | Read/Write all data |
| Service | Read specific fields |

### Data Classification

| Data Type | Classification | Encryption |
|-----------|---------------|------------|
| Email | Sensitive | At rest, in transit |
| Password | Critical | Hashed (bcrypt) |
| Profile | Internal | At rest, in transit |
| Sessions | Internal | At rest |

---

## Operational Boundaries

### Deployment

| Property | Value |
|----------|-------|
| Deployment Strategy | Blue-green |
| Rollback Time | < 5 minutes |
| Health Check | /health |
| Ready Check | /health/ready |

### Monitoring

| Metric | Alert Threshold | Severity |
|--------|-----------------|----------|
| Error Rate | > 1% | Critical |
| Latency (p99) | > 500ms | Warning |
| Availability | < 99.9% | Critical |
| CPU | > 80% | Warning |

### Logging

| Log Level | Retention | Purpose |
|-----------|-----------|---------|
| ERROR | 90 days | Incident investigation |
| WARN | 30 days | Trend analysis |
| INFO | 7 days | Debugging |
| DEBUG | 1 day | Development |

---

## Dependencies

### Hard Dependencies (Service fails without)

| Dependency | Purpose | Failure Impact |
|------------|---------|----------------|
| PostgreSQL | User data storage | Complete outage |
| Redis | Session storage | Login failures |
| Auth Service | Token validation | Auth failures |

### Soft Dependencies (Degraded functionality)

| Dependency | Purpose | Failure Impact |
|------------|---------|----------------|
| Notification | Email sending | No emails, core works |
| Analytics | Event tracking | No analytics, core works |

### Optional Dependencies (Enhanced features)

| Dependency | Purpose | Failure Impact |
|------------|---------|----------------|
| Image CDN | Avatar images | No avatars, core works |

---

## Migration History

| Version | Date | Changes | Breaking |
|---------|------|---------|----------|
| 1.0.0 | [DATE] | Initial release | No |
| 1.1.0 | [DATE] | Added preferences API | No |
| 2.0.0 | [DATE] | Changed user schema | Yes |

---

## Team

| Role | Name | Contact |
|------|------|---------|
| Service Owner | [Name] | [email] |
| Tech Lead | [Name] | [email] |
| On-Call | [Team] | [pagerduty] |

---

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| [DATE] | Use PostgreSQL for user data | Relational data, ACID compliance | MongoDB, DynamoDB |
| [DATE] | Use Redis for sessions | Fast access, TTL support | Memcached, Database |