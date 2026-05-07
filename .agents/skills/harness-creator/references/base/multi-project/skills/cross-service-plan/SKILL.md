---
name: cross-service-plan
description: "Plans and coordinates changes that affect multiple services. Identifies breaking changes, determines deployment order, and manages rollback strategies."
user-invocable: true
---

# Cross-Service Planning Skill

You are facilitating cross-service change planning. Your role is to ensure that changes spanning multiple services are coordinated safely with minimal risk and clear rollback strategies.

## Purpose

Cross-service changes are high-risk. This skill ensures:
- All affected services are identified
- Dependencies are respected in deployment order
- Breaking changes are handled properly
- Rollback strategies are prepared
- Communication is clear between service owners

## When to Use

- Planning changes to shared interfaces
- Deploying features that span multiple services
- Migrating to new API versions
- Refactoring cross-service communication
- Database schema changes affecting multiple services

## Planning Workflow

### Phase 1: Impact Assessment

1. **Identify Changed Services**
   - Which services are directly modified?
   - Which services depend on those modifications?
   - What is the full dependency chain?

2. **Classify Changes**
   ```
   | Change Type | Risk Level | Coordination Required |
   |-------------|------------|----------------------|
   | Additive | Low | Minimal - backward compatible |
   | Optional Field | Low | Document in schema |
   | Required Field | Medium | Coordinate consumers first |
   | Removal | High | Migrate all consumers first |
   | Type Change | High | Version bump required |
   | Behavioral | Medium | Test all consumers |
   ```

3. **Map Dependencies**
   ```markdown
   ## Dependency Graph
   
   service-a (changed)
     -> service-b (depends on service-a)
        -> service-c (depends on service-b)
     -> service-d (depends on service-a)
   
   Deployment Order: service-c -> service-b -> service-d -> service-a
   ```

### Phase 2: Deployment Sequencing

1. **Determine Order**
   - Consumers deploy before producers for breaking changes
   - Producers deploy before consumers for additive changes
   - Parallel deployment possible for independent changes

2. **Create Deployment Plan**
   ```markdown
   ## Deployment Plan
   
   ### Stage 1: Preparation (No Downtime)
   - [ ] Deploy service-c update (backward compatible)
   - [ ] Verify service-c health
   
   ### Stage 2: Consumer Updates (No Downtime)
   - [ ] Deploy service-b update (handles both old and new)
   - [ ] Deploy service-d update (handles both old and new)
   - [ ] Verify all consumers healthy
   
   ### Stage 3: Producer Update (No Downtime)
   - [ ] Deploy service-a with new feature
   - [ ] Verify service-a health
   - [ ] Enable new feature in consumers
   
   ### Stage 4: Cleanup (No Downtime)
   - [ ] Remove backward compatibility code from consumers
   - [ ] Verify final state
   ```

3. **Define Checkpoints**
   - Health checks between stages
   - Rollback triggers
   - Success criteria

### Phase 3: Breaking Change Handling

1. **Detect Breaking Changes**
   - API contract changes
   - Event schema changes
   - Database schema changes
   - Configuration changes

2. **Create Migration Path**
   ```markdown
   ## Migration Strategy: [Change Name]
   
   ### Current State
   - Version: v1
   - Schema: [current schema]
   
   ### Target State
   - Version: v2
   - Schema: [new schema]
   
   ### Migration Steps
   1. Deploy v2 alongside v1 (parallel running)
   2. Migrate consumers to v2 incrementally
   3. Monitor for issues
   4. Deprecate v1
   5. Remove v1 after deprecation period
   
   ### Rollback Plan
   1. Switch consumers back to v1
   2. Remove v2
   3. Investigate issues
   ```

### Phase 4: Rollback Strategy

1. **Define Rollback Triggers**
   - Error rate exceeds threshold (e.g., >1%)
   - Latency exceeds threshold (e.g., >500ms p99)
   - Specific error patterns appear
   - Business metrics degrade

2. **Create Rollback Playbook**
   ```markdown
   ## Rollback Playbook: [Service Name]
   
   ### Trigger
   - [Condition that triggers rollback]
   
   ### Steps
   1. [First action - usually disable feature flag]
   2. [Second action - usually traffic shift]
   3. [Third action - usually code rollback]
   
   ### Verification
   - [How to verify rollback succeeded]
   
   ### Communication
   - [Who to notify]
   - [What to communicate]
   
   ### Post-Rollback
   - [Investigation steps]
   - [Prevention measures]
   ```

3. **Test Rollback**
   - Document rollback procedure
   - Practice in staging
   - Verify data consistency after rollback

## Coordination Checklist

```markdown
## Cross-Service Change Checklist

### Before Deployment
- [ ] All affected services identified
- [ ] Dependency graph documented
- [ ] Deployment order determined
- [ ] Breaking changes identified and mitigated
- [ ] Migration path defined
- [ ] Rollback plan created and tested
- [ ] All service owners notified
- [ ] Monitoring dashboards ready
- [ ] Alerts configured for failure detection

### During Deployment
- [ ] Deploy in planned sequence
- [ ] Verify health after each stage
- [ ] Monitor error rates and latency
- [ ] Check business metrics
- [ ] Document any deviations from plan

### After Deployment
- [ ] All services healthy
- [ ] Business metrics normal
- [ ] Remove deprecated code paths
- [ ] Update documentation
- [ ] Post-deployment review
```

## Communication Template

```markdown
## Cross-Service Change: [Change Name]

### Summary
[2-3 sentence description of the change]

### Impact
- **Services Affected**: [list]
- **Breaking Changes**: [yes/no, details]
- **Downtime Required**: [yes/no, duration if yes]

### Timeline
| Time | Action | Service |
|------|--------|---------|
| [T] | [Action] | [Service] |

### Rollback Plan
[Brief summary of rollback strategy]

### Contacts
- **Primary**: [Name]
- **Backup**: [Name]

### Questions?
Post in #deployment-channel
```

## Usage

```
/cross-service-plan [change-description]
```

This will:
1. Analyze the proposed change for cross-service impact
2. Generate a dependency graph
3. Create a deployment sequence
4. Identify breaking changes
5. Create rollback playbook
6. Generate communication template