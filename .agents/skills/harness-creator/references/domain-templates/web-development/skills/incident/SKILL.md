---
name: incident
description: "Production incident response workflow — triage, root cause analysis, and resolution."
argument-hint: "[incident description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Agent, AskUserQuestion
---

# Incident Response Workflow

Structured workflow for handling production incidents with full audit trail.

---

## Workflow

### Phase 1: Initial Triage

1. **Gather information**
   - "What's the symptom? (error message, behavior, alert)"
   - "When did it start?"
   - "What's the scope? (all users, subset, single user)"
   - "Is it blocking users?"

2. **Assess severity**

   | Severity | Criteria | Response Time |
   |----------|----------|---------------|
   | **P1 - Critical** | Service down, data loss risk | Immediate |
   | **P2 - High** | Major feature broken | <1 hour |
   | **P3 - Medium** | Degraded performance | <4 hours |
   | **P4 - Low** | Minor issue, workaround exists | Next business day |

3. **Create incident record**
   ```markdown
   # Incident: [Date-Time] - [Brief Description]

   ## Status: INVESTIGATING / IDENTIFIED / FIXING / RESOLVED

   ## Severity: P1/P2/P3/P4

   ## Timeline
   - [Time] Incident detected
   - [Time] [Action taken]

   ## Impact
   - Users affected: [count or description]
   - Duration: [time]
   - Features affected: [list]

   ## Root Cause
   [To be filled during investigation]

   ## Resolution
   [To be filled after fix]

   ## Follow-up
   [ ] Postmortem scheduled
   [ ] Monitoring improved
   [ ] Tests added
   ```

---

### Phase 2: Investigation

1. **Gather evidence**
   - Check logs: `docker logs [container]` or equivalent
   - Check metrics: error rates, latency, resource usage
   - Check recent deployments: `git log --oneline -10`
   - Check configuration changes

2. **Form hypotheses**
   - Recent code change?
   - Infrastructure change?
   - External dependency?
   - Data corruption?
   - Capacity issue?

3. **Test hypotheses**
   - Check specific log patterns
   - Reproduce in staging if possible
   - Review related code

---

### Phase 3: Resolution

1. **Immediate fix** (if available)
   - Rollback recent deployment
   - Scale resources
   - Disable problematic feature flag
   - Restart service

2. **Root cause fix** (if time allows)
   - Spawn relevant Specialist to implement fix
   - Have fix reviewed
   - Test fix in staging

3. **Verify resolution**
   - Confirm service is healthy
   - Check error rates return to normal
   - Verify user-facing functionality

---

### Phase 4: Documentation

Create postmortem document:

```markdown
# Postmortem: [Incident Title]

**Date**: [Date]
**Severity**: P1/P2/P3/P4
**Duration**: [Time from detection to resolution]
**Author**: [Name]

## Summary

[2-3 sentence summary of what happened]

## Impact

- **Users affected**: [Count or description]
- **Duration**: [Total time]
- **Revenue impact**: [If applicable]

## Timeline

| Time | Event |
|------|-------|
| [HH:MM] | Incident detected via [monitoring/user report] |
| [HH:MM] | [Team member] acknowledged |
| [HH:MM] | Root cause identified |
| [HH:MM] | Fix deployed |
| [HH:MM] | Incident resolved |

## Root Cause

[Detailed explanation of what caused the incident]

## Contributing Factors

1. [Factor that contributed to the issue]
2. [Another factor]

## Resolution

[What was done to fix the issue]

## Lessons Learned

### What went well
- [Positive aspects of the response]

### What could be improved
- [Areas for improvement]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [ ] [Action 1] | [Name] | [Date] | TODO |
| [ ] [Action 2] | [Name] | [Date] | TODO |

## Appendix

- [Links to logs, graphs, PRs, etc.]
```

---

## Output

- Incident record with full timeline
- Root cause analysis
- Fix implementation (if applicable)
- Postmortem document
- Action items to prevent recurrence