# Service Registry

> Central registry of all services, their endpoints, dependencies, and status.
> Version: 1.0
> Last Updated: [DATE]

---

## Overview

This registry maintains the authoritative list of all services in the system, their relationships, and current status. It serves as the source of truth for service coordination and dependency management.

---

## Services

### [Service Name]

| Property | Value |
|----------|-------|
| **Service ID** | `[service-id]` |
| **Version** | `[major.minor.patch]` |
| **Status** | ACTIVE \| DEPRECATED \| DEVELOPMENT \| RETIRED |
| **Owner** | `[team-name]` |
| **Repository** | `[repo-url]` |
| **Documentation** | `[docs-url]` |

#### Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| GET | `/api/v1/resource` | List resources | Yes |
| POST | `/api/v1/resource` | Create resource | Yes |
| GET | `/api/v1/resource/{id}` | Get resource | Yes |
| PUT | `/api/v1/resource/{id}` | Update resource | Yes |
| DELETE | `/api/v1/resource/{id}` | Delete resource | Yes |

#### Dependencies

| Dependency | Type | Version | Status |
|------------|------|---------|--------|
| `[dep-service-id]` | HARD \| SOFT \| OPTIONAL | `[version]` | HEALTHY \| DEGRADED \| DOWN |
| `[dep-service-id]` | EVENT | `[schema-version]` | HEALTHY |

#### Events Produced

| Event Name | Schema Version | Consumers | Description |
|------------|----------------|-----------|-------------|
| `user.created` | v1.0.0 | notification, analytics | User account created |
| `user.updated` | v1.0.0 | notification, analytics | User profile updated |
| `user.deleted` | v1.0.0 | analytics | User account deleted |

#### Events Consumed

| Event Name | Schema Version | Producer | Purpose |
|------------|----------------|----------|---------|
| `order.completed` | v1.0.0 | order-service | Send order confirmation |

#### Configuration

| Key | Environment | Value Source |
|-----|-------------|--------------|
| `DATABASE_URL` | All | AWS Secrets Manager |
| `REDIS_URL` | All | Environment Variable |
| `FEATURE_FLAGS` | All | LaunchDarkly |

#### Health Check

| Endpoint | Interval | Timeout | Unhealthy Threshold |
|----------|----------|---------|---------------------|
| `/health` | 30s | 5s | 3 failures |
| `/health/ready` | 30s | 5s | 3 failures |

---

## Dependency Graph

```
                    ┌─────────────┐
                    │   gateway   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         v                 v                 v
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │   user    │     │   order   │     │  catalog  │
   │  service  │     │  service  │     │  service  │
   └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
         │                 │                 │
         │         ┌───────┴───────┐         │
         │         │               │         │
         v         v               v         v
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │  auth    │     │  payment  │     │ inventory │
   │ service  │     │  service  │     │  service  │
   └───────────┘     └───────────┘     └───────────┘
```

---

## Service Categories

### Core Services
Services that are essential for system operation.

| Service | Purpose | Dependencies |
|---------|---------|--------------|
| `[service-id]` | `[description]` | `[deps]` |

### Domain Services
Business logic services.

| Service | Purpose | Dependencies |
|---------|---------|--------------|
| `[service-id]` | `[description]` | `[deps]` |

### Infrastructure Services
Supporting services for cross-cutting concerns.

| Service | Purpose | Dependencies |
|---------|---------|--------------|
| `[service-id]` | `[description]` | `[deps]` |

---

## Communication Patterns

### Synchronous (REST/gRPC)

| From Service | To Service | Protocol | Purpose |
|--------------|------------|----------|---------|
| `[source]` | `[target]` | REST \| gRPC | `[purpose]` |

### Asynchronous (Events)

| Event | Producer | Consumers | Schema |
|-------|----------|-----------|--------|
| `[event-name]` | `[producer]` | `[consumers]` | `[schema-url]` |

---

## Deployment Information

### Environments

| Environment | URL | Status | Version |
|-------------|-----|--------|---------|
| Production | `https://api.example.com` | ACTIVE | `[version]` |
| Staging | `https://api-staging.example.com` | ACTIVE | `[version]` |
| Development | `https://api-dev.example.com` | ACTIVE | `[version]` |

### Deployment Pipeline

```
development -> staging -> canary -> production
```

---

## Status History

| Date | Service | Status Change | Reason |
|------|---------|---------------|--------|
| [DATE] | [service-id] | DEPLOYED -> ACTIVE | Initial deployment |
| [DATE] | [service-id] | ACTIVE -> DEGRADED | Database connection issues |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | [DATE] | [Author] | Initial registry |

---

## Registry Maintenance

### Adding a New Service

1. Copy the service template section
2. Fill in all required fields
3. Update dependency graph
4. Add to appropriate category
5. Submit for review

### Updating Service Information

1. Locate service in registry
2. Update relevant fields
3. Increment version if API changes
4. Update dependency graph if needed
5. Submit for review

### Deprecating a Service

1. Change status to DEPRECATED
2. Add deprecation date
3. Notify all consumers
4. Create migration plan
5. Remove after deprecation period

### Retiring a Service

1. Verify no consumers exist
2. Change status to RETIRED
3. Remove from dependency graph
4. Archive documentation
5. Update registry