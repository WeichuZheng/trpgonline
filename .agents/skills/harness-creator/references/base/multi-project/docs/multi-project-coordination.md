# Multi-Project Coordination

> A guide to coordinating development across multiple projects, services, and teams in a monorepo or microservices architecture.

---

## Overview

Multi-project coordination is essential when:
- Multiple services share code or dependencies
- Changes impact multiple teams
- Deployments must be sequenced
- API contracts span service boundaries

This guide establishes patterns and practices for effective coordination.

---

## Coordination Patterns

### Pattern 1: Shared Library Updates

When updating shared libraries:

```
1. UPDATE     Make changes in shared library
      |
      v
2. VERSION    Bump version, update CHANGELOG
      |
      v
3. RELEASE    Publish new version
      |
      v
4. NOTIFY     Alert consuming services
      |
      v
5. MIGRATE    Services update dependency
      |
      v
6. VERIFY     All services pass tests
```

**Checklist:**
- [ ] Check all consumers before making breaking changes
- [ ] Use semantic versioning
- [ ] Provide migration guide for breaking changes
- [ ] Support previous major version for 6 months
- [ ] Update all consumers within 30 days of release

### Pattern 2: Cross-Service Feature Development

When developing features that span services:

```
1. DESIGN     Create cross-service design document
      |
      v
2. CONTRACT   Define API contracts first
      |
      v
3. IMPLEMENT  Develop services in dependency order
      |
      v
4. INTEGRATE  Test end-to-end flow
      |
      v
5. DEPLOY     Deploy in reverse dependency order
```

**Design Document Template:**

```markdown
## Cross-Service Feature: [Feature Name]

### Overview
[What the feature does, from user perspective]

### Services Involved
| Service | Role | Owner |
|---------|------|-------|
| service-a | [role] | [team] |
| service-b | [role] | [team] |

### Integration Points
| From | To | Protocol | Contract |
|------|-----|---------| ---------|
| service-a | service-b | REST | [link] |

### Dependency Order
1. service-c (no dependencies)
2. service-b (depends on c)
3. service-a (depends on b)

### Deployment Order
1. service-c
2. service-b
3. service-a

### Rollback Order
Reverse of deployment order
```

### Pattern 3: Database Schema Changes

When changing shared database schemas:

```
1. ANALYZE    Identify all affected services
      |
      v
2. PLAN       Create migration strategy
      |
      v
3. PREPARE    Add new columns/tables (non-breaking)
      |
      v
4. DEPLOY     Deploy all services with dual-write
      |
      v
5. MIGRATE    Backfill data if needed
      |
      v
6. SWITCH     Move reads to new schema
      |
      v
7. CLEANUP    Remove old columns/tables
```

**Schema Migration Checklist:**
- [ ] All services identified
- [ ] Backward compatible changes made first
- [ ] Dual-write period completed
- [ ] Data migration verified
- [ ] Old schema removed after verification

### Pattern 4: API Versioning

When evolving APIs:

```
Version Strategy:
- Major: Breaking changes (v1 -> v2)
- Minor: New features, backward compatible
- Patch: Bug fixes

Lifecycle:
1. CURRENT     Active development
      |
      v
2. DEPRECATED  No new features, security fixes only (6 months)
      |
      v
3. RETIRED     No support, endpoints removed
```

**Deprecation Checklist:**
- [ ] Announce deprecation 6 months in advance
- [ ] Add `Deprecation` header to responses
- [ ] Add `Sunset` header with removal date
- [ ] Provide migration guide
- [ ] Monitor usage of deprecated version
- [ ] Contact all known consumers
- [ ] Remove after deprecation period

---

## Communication Protocols

### Service-to-Service Communication

#### Synchronous (REST/gRPC)

**Best Practices:**
- Define contracts in OpenAPI/Protobuf
- Version all APIs
- Set appropriate timeouts
- Implement circuit breakers
- Use correlation IDs for tracing

**Timeout Guidelines:**
| Call Type | Timeout | Retry |
|-----------|---------|-------|
| Within datacenter | 100ms | Yes |
| Cross-region | 1s | Yes |
| Third-party | 5s | Limited |

#### Asynchronous (Events/Messages)

**Best Practices:**
- Define event schemas
- Use schema evolution patterns
- Ensure idempotency
- Handle out-of-order messages
- Implement dead letter queues

**Event Schema Versioning:**
```json
{
  "event_type": "user.created",
  "event_version": "1.0.0",
  "event_id": "uuid",
  "timestamp": "ISO8601",
  "data": {
    // Version-specific payload
  }
}
```

### Team Communication

#### Change Notification Template

```markdown
## Change Notification

### What
[Description of the change]

### When
[Timeline for rollout]

### Impact
- Services affected: [list]
- Breaking changes: [yes/no]
- Downtime required: [yes/no]

### Action Required
- [Team 1]: [Action needed]
- [Team 2]: [Action needed]

### Questions
Post in #[change-channel]
```

#### RFC Process

For significant changes:

```
1. DRAFT       Create RFC document
      |
      v
2. SHARE       Distribute to affected teams
      |
      v
3. DISCUSS     5 business days for feedback
      |
      v
4. REVISE      Address feedback
      |
      v
5. APPROVE     Get sign-off from stakeholders
      |
      v
6. IMPLEMENT   Begin implementation
```

**RFC Template:**
```markdown
# RFC: [Title]

## Summary
[1-2 paragraph summary]

## Motivation
[Why is this change needed?]

## Proposed Solution
[Detailed technical proposal]

## Alternatives Considered
[Other approaches and why they were rejected]

## Impact
- Services affected: [list]
- Breaking changes: [details]
- Migration required: [details]

## Timeline
- RFC: [date]
- Implementation: [date range]
- Migration: [date range]

## Stakeholders
- [Team]: [sign-off required]
```

---

## Dependency Management

### Dependency Types

| Type | Description | Coordination Level |
|------|-------------|-------------------|
| **Hard** | Service fails without dependency | Must deploy together |
| **Soft** | Degraded functionality without dependency | Can deploy separately |
| **Optional** | Enhanced features with dependency | Independent deployment |
| **Event** | Async communication | Schema coordination |

### Dependency Graph

Maintain a dependency graph for your services:

```
                    ┌─────────┐
                    │ gateway │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         v               v               v
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │  user   │    │  order  │    │ product │
    │ service │    │ service │    │ service │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         v               v               v
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │   auth  │    │ payment │    │inventory│
    │ service │    │ service │    │ service │
    └─────────┘    └─────────┘    └─────────┘
```

### Dependency Rules

1. **No Circular Dependencies**: If A depends on B, B cannot depend on A
2. **Explicit Dependencies**: All dependencies must be declared in service registry
3. **Version Constraints**: Specify minimum and maximum versions
4. **Health Checks**: Monitor health of all dependencies

---

## Deployment Coordination

### Deployment Strategies

#### Blue-Green Deployment

```
┌─────────────┐          ┌─────────────┐
│   Blue      │          │   Green     │
│  (v1.0.0)   │          │  (v1.1.0)   │
│   LIVE      │          │   IDLE      │
└─────────────┘          └─────────────┘
       │                        │
       └────────────────────────┘
                  │
             Switch Traffic
                  │
                  v
┌─────────────┐          ┌─────────────┐
│   Blue      │          │   Green     │
│  (v1.0.0)   │          │  (v1.1.0)   │
│   IDLE      │          │   LIVE      │
└─────────────┘          └─────────────┘
```

#### Canary Deployment

```
┌─────────────┐
│   Stable    │  90% traffic
│  (v1.0.0)   │
└─────────────┘
       │
       v
┌─────────────┐
│   Canary    │  10% traffic
│  (v1.1.0)   │
└─────────────┘
```

#### Feature Flags

```
if (featureFlag.isEnabled('new-feature', user)) {
  return newImplementation();
} else {
  return oldImplementation();
}
```

### Deployment Order

For coordinated deployments:

```
1. INFRASTRUCTURE  Deploy infrastructure changes
        |
        v
2. FOUNDATION     Deploy foundational services (auth, config)
        |
        v
3. CORE           Deploy core business services
        |
        v
4. EDGE           Deploy edge services (gateway, frontend)
        |
        v
5. VERIFY         Run integration tests
```

**Rollback Order:** Reverse of deployment order

### Deployment Checklist

```markdown
## Pre-Deployment
- [ ] All services tested in staging
- [ ] Dependency order verified
- [ ] Rollback plan documented
- [ ] On-call engineer identified
- [ ] Monitoring dashboards ready
- [ ] Stakeholders notified

## During Deployment
- [ ] Deploy in planned order
- [ ] Verify health after each service
- [ ] Monitor error rates
- [ ] Check business metrics
- [ ] Document any issues

## Post-Deployment
- [ ] All services healthy
- [ ] Integration tests pass
- [ ] Business metrics normal
- [ ] Notify stakeholders of success
- [ ] Update deployment record
```

---

## Conflict Resolution

### Common Conflicts

#### Resource Conflicts
- Shared database connections
- Limited infrastructure resources
- Deployment window competition

#### Solution:
- Resource quotas per service
- Coordinated deployment windows
- Shared infrastructure team

#### API Conflicts
- Breaking changes without coordination
- Duplicate endpoints
- Inconsistent naming

#### Solution:
- API design review process
- Central API registry
- Naming conventions

#### Dependency Version Conflicts
- Different versions of same library
- Transitive dependency conflicts
- Security patch requirements

#### Solution:
- Shared dependency management
- BOM (Bill of Materials) for common versions
- Automated dependency updates

### Escalation Path

```
1. Team Level     Teams resolve directly
       |
       v
2. Service Owner  Service owners negotiate
       |
       v
3. Architecture   Architecture team decides
       |
       v
4. Leadership     Engineering leadership decides
```

---

## Tools and Automation

### Recommended Tools

| Category | Tool | Purpose |
|----------|------|---------|
| Service Registry | Consul, Eureka | Service discovery |
| API Gateway | Kong, Ambassador | Request routing |
| Message Bus | Kafka, RabbitMQ | Event coordination |
| Config Management | Consul, Spring Cloud Config | Centralized config |
| Monitoring | Prometheus, Grafana | Health monitoring |
| Tracing | Jaeger, Zipkin | Request tracing |

### Automation Scripts

#### Dependency Check

```bash
#!/bin/bash
# check-dependencies.sh

SERVICE=$1
REGISTRY_URL="http://service-registry"

# Get service dependencies
DEPS=$(curl -s "$REGISTRY_URL/services/$SERVICE/dependencies")

# Check health of each dependency
for dep in $(echo $DEPS | jq -r '.[] | .name'); do
  HEALTH=$(curl -s "$REGISTRY_URL/services/$dep/health")
  if [ "$HEALTH" != "HEALTHY" ]; then
    echo "WARNING: $dep is not healthy"
  fi
done
```

#### Contract Drift Detection

```bash
#!/bin/bash
# detect-drift.sh

SPEC_DIR="specs"
IMPL_DIR="src"

for spec in $SPEC_DIR/*.yaml; do
  SERVICE=$(basename $spec .yaml)
  
  # Compare spec endpoints with implementation
  SPEC_ENDPOINTS=$(yq eval '.paths | keys | .[]' $spec)
  IMPL_ENDPOINTS=$(grep -r "router\." $IMPL_DIR/$SERVICE | grep -oP '(?<=["'"'"']).+(?=["'"'"'])')
  
  for endpoint in $SPEC_ENDPOINTS; do
    if ! echo "$IMPL_ENDPOINTS" | grep -q "$endpoint"; then
      echo "DRIFT: $endpoint in spec but not in implementation"
    fi
  done
done
```

---

## Best Practices

### DO
- Document all service boundaries clearly
- Version all APIs from the start
- Use feature flags for gradual rollouts
- Monitor cross-service metrics
- Coordinate deployments with affected teams
- Maintain backward compatibility during migrations

### DON'T
- Make breaking changes without coordination
- Create circular dependencies
- Skip the RFC process for significant changes
- Deploy during peak traffic without coordination
- Assume other services are available
- Hardcode service URLs or versions

---

## Summary

Effective multi-project coordination requires:

1. **Clear Boundaries**: Define what each service owns
2. **Explicit Contracts**: Document all APIs and events
3. **Communication**: Notify affected parties of changes
4. **Automation**: Use tools to detect drift and enforce rules
5. **Process**: Follow RFC and review processes
6. **Patience**: Plan migrations carefully, don't rush

When done well, coordination enables teams to move independently while maintaining system integrity.