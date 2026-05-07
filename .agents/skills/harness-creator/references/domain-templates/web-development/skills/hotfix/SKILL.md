---
name: hotfix
description: "Emergency fix workflow for production issues with minimal scope and fast turnaround. Creates hotfix branch, fix, and rapid deployment."
user-invocable: true
---

# Hotfix Skill

You are facilitating the Hotfix process. Your role is to handle emergency production fixes with minimal scope and fast turnaround.

## Purpose

Hotfix workflow ensures:
- Critical issues are fixed quickly
- Minimal changes reduce risk
- Fix is properly tested
- Deployment is rapid and tracked

## Hotfix Flow

```
ISSUE REPORT -> TRIAGE -> HOTFIX BRANCH -> MINIMAL FIX -> QUICK TEST -> DEPLOY -> VERIFY -> MERGE BACK
```

## Hotfix Principles

1. **Minimal Scope**: Fix only the critical issue, nothing else
2. **Speed**: Time is critical for production issues
3. **Reversible**: Fix can be rolled back if needed
4. **Documented**: Issue and fix are fully documented

## Workflow

### Phase 1: Triage

1. Receive issue report
2. Assess severity:
   - **P1 Critical**: System down, data loss risk
   - **P2 High**: Major functionality broken
   - **P3 Medium**: Significant bug, workaround exists
3. Determine if hotfix is appropriate
4. Identify affected domain(s)

### Phase 2: Create Hotfix Branch

1. Create branch from production tag:
   ```bash
   git checkout v[current-production]
   git checkout -b hotfix/[issue-id]-[description]
   ```
2. Document branch purpose

### Phase 3: Minimal Fix

1. Identify root cause
2. Implement MINIMAL fix (only what's needed)
3. NO refactoring, NO improvements, NO side changes
4. Document fix in code comments

### Phase 4: Quick Test

Run essential tests:
- [ ] Fix resolves the issue
- [ ] No regression in critical paths
- [ ] Fix works in staging environment

### Phase 5: Deploy

1. Build and deploy hotfix version
2. Monitor for immediate issues
3. Verify fix in production

### Phase 6: Merge Back

After fix is verified:
1. Merge hotfix to main branch
2. Update changelog
3. Close issue ticket
4. Schedule full review (post-hotfix)

## Hotfix Report Template

```markdown
# Hotfix: [Issue ID]

**Date**: [Date]
**Severity**: P1/P2/P3
**Status**: IDENTIFIED | FIXING | TESTING | DEPLOYING | VERIFIED | COMPLETE

---

## Issue

**Description**: [What's broken]
**Impact**: [Who is affected, how badly]
**Root Cause**: [Why it's broken]
**Reported By**: [Source]

---

## Fix

**Approach**: [How we fixed it]
**Changes Made**:
| File | Change | Domain |
|------|--------|--------|
| [path] | [change] | [domain] |

**Scope**: [Minimal/Standard]
**Risk**: Low/Medium/High

---

## Testing

- [ ] Issue resolved in staging
- [ ] No regression in critical paths
- [ ] Production verified

**Test Results**:
- [Test 1]: PASS/FAIL
- [Test 2]: PASS/FAIL

---

## Deployment

**Branch**: hotfix/[issue-id]
**Version**: v[version]-hotfix.[n]
**Deployed At**: [Time]
**Deployed By**: [Agent]

---

## Verification

**Status**: VERIFIED / ISSUE_FOUND
**Evidence**: [How we verified fix works]
**Monitoring**: [What we're watching]

---

## Merge Back

- [ ] Merged to main
- [ ] Changelog updated
- [ ] Issue closed
- [ ] Post-hotfix review scheduled

---

## Timeline

| Time | Action |
|------|--------|
| [T1] | Issue reported |
| [T2] | Triage complete |
| [T3] | Hotfix branch created |
| [T4] | Fix implemented |
| [T5] | Tests passed |
| [T6] | Deployed to staging |
| [T7] | Deployed to production |
| [T8] | Fix verified |

---

## Post-Hotfix Actions

1. [Full review scheduled]
2. [Root cause analysis needed]
3. [Permanent fix to implement]
4. [Monitoring to add]
```

## Severity Classification

| Severity | Description | Response Time | Hotfix? |
|----------|-------------|---------------|---------|
| P1 Critical | System down | Immediate | YES |
| P2 High | Major broken | < 1 hour | YES |
| P3 Medium | Significant bug | < 4 hours | MAYBE |
| P4 Low | Minor issue | Next release | NO |

## Minimal Fix Rules

### What to Fix
- Only the specific bug/issue
- Direct cause of the problem
- Safety checks to prevent recurrence

### What NOT to Fix (in Hotfix)
- Related refactoring
- Code improvements
- Documentation updates
- Other bugs (even if found)
- Style/formatting

## Hotfix Branch Naming

```
hotfix/[issue-id]-[short-description]

Examples:
hotfix/issue-123-login-error
hotfix/security-xss-fix
hotfix/db-connection-leak
```

## Hotfix Versioning

```
v[version]-hotfix.[number]

Examples:
v1.2.3-hotfix.1  (first hotfix on 1.2.3)
v1.2.3-hotfix.2  (second hotfix on 1.2.3)
```

## Quick Test Checklist

Essential tests only:
- [ ] Bug is fixed (manual test)
- [ ] Critical user flow works
- [ ] Authentication works
- [ ] Database operations work
- [ ] No new errors in logs

## Deployment Commands

```bash
# Build hotfix version
docker build -t app:v1.2.3-hotfix.1 .

# Deploy to staging
docker-compose -f docker-compose.staging.yml up -d

# Verify staging
curl staging-url/health

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Monitor production
curl production-url/health
```

## Anti-Patterns to Avoid

- Fixing more than the specific issue
- Skipping staging verification
- No rollback plan
- No documentation
- Hotfixing on Friday
- Multiple hotfixes in sequence

## Usage

```
/hotfix [issue description]
```

Example:
```
/hotfix Login returns 500 error on production
/hotfix XSS vulnerability in user profile
```

## Coordination

- architect-lead approves P1/P2 hotfixes
- Domain lead approves domain-specific hotfixes
- devops-dev handles deployment
- All hotfixes must be merged back to main