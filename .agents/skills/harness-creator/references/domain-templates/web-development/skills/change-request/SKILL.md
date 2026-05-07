---
name: change-request
description: "Guided workflow for handling requirement changes in existing features. Analyzes impact, plans modifications, and coordinates updates."
user-invocable: true
---

# Change Request Skill

You are facilitating the Change Request process. Your role is to handle requirement changes to existing features with proper impact analysis and coordination.

## Purpose

Change request handling ensures:
- Impact is analyzed before changes
- Existing functionality is protected
- Changes are properly coordinated
- Regression risk is minimized

## Change Request Flow

```
CHANGE REQUEST -> IMPACT ANALYSIS -> DOMAIN ASSESSMENT -> APPROVAL -> IMPLEMENTATION PLAN
```

## Workflow

### Phase 1: Change Request Analysis

1. Parse the requested change
2. Identify what feature is affected
3. Determine change type:
   - **Addition**: New functionality to existing feature
   - **Modification**: Change to existing behavior
   - **Removal**: Remove functionality
   - **Replacement**: Replace functionality with alternative

### Phase 2: Impact Analysis

Analyze impact across all domains:

**Frontend Impact:**
- Component changes needed
- State management changes
- UI/UX changes
- Test updates

**Backend Impact:**
- Endpoint changes
- Service logic changes
- Validation changes
- Test updates

**Database Impact:**
- Schema changes
- Migration needed
- Query changes

**DevOps Impact:**
- Configuration changes
- Environment updates

### Phase 3: Regression Risk Assessment

Identify regression risks:
- What existing functionality might break
- What tests need updating
- What documentation needs changes
- What dependent features are affected

### Phase 4: Domain Assessment

For each affected domain, determine:
- Can the domain handle changes independently?
- Does the change require coordination?
- What agent should implement the change?

### Phase 5: Approval Request

Present analysis to user:
- Summary of change
- Impact analysis
- Regression risks
- Implementation approach
- Estimated effort

## Change Request Template

```markdown
# Change Request: [CR-ID]

## Request
**Feature**: [Affected feature]
**Type**: Addition | Modification | Removal | Replacement
**Description**: [What change is requested]

## Impact Analysis

### Frontend
- **Affected**: [Yes/No]
- **Components**: [List affected components]
- **Changes Required**: [Description]
- **Agent**: frontend-dev

### Backend
- **Affected**: [Yes/No]
- **Endpoints**: [List affected endpoints]
- **Changes Required**: [Description]
- **Agent**: api-dev

### Database
- **Affected**: [Yes/No]
- **Tables**: [List affected tables]
- **Migration Needed**: [Yes/No]
- **Agent**: database-dev

### DevOps
- **Affected**: [Yes/No]
- **Changes Required**: [Description]
- **Agent**: devops-dev

## Regression Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Implementation Order
1. [Step 1]
2. [Step 2]

## Tests to Update
- [Test 1]
- [Test 2]

## Documentation Updates
- [Doc 1]
- [Doc 2]

## Approval
- [ ] User approved
- [ ] architect-lead approved (if cross-domain)
- [ ] Domain leads approved

## Status
DRAFT | PENDING_APPROVAL | APPROVED | IN_PROGRESS | COMPLETE
```

## Change Types and Handling

### Addition
- Lower regression risk
- May require new API contracts
- Usually requires database schema additions

### Modification
- Higher regression risk
- Requires careful test coverage review
- May break dependent features

### Removal
- Check all dependencies first
- Update all dependent features
- Remove tests, docs, and references

### Replacement
- Treat as removal + addition
- Requires migration strategy
- Update all consumers

## Impact Severity Levels

| Level | Description | Approval Required |
|-------|-------------|-------------------|
| Low | Single domain, isolated change | Domain lead |
| Medium | Multiple domains, limited scope | Both leads |
| High | Cross-domain, wide impact | architect-lead |
| Critical | Breaking change, major refactor | architect-lead + user |

## Coordination Rules

1. Changes affecting frontend AND backend require both leads to approve
2. Breaking API changes require frontend-lead sign-off
3. Database schema changes require backend-lead approval
4. Cross-domain changes require architect-lead review

## Usage

```
/change-request [change description]
```

Example:
```
/change-request Add email verification to user registration
```

## Best Practices

1. **Always analyze impact first**: Never jump to implementation
2. **Check tests**: Update tests before making changes
3. **Document changes**: Update docs alongside code
4. **Plan rollback**: Know how to reverse if needed