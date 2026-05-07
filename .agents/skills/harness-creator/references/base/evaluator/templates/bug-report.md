# Bug Report Template

> Use this template to document issues found during evaluation that are not covered by sprint contract criteria.
> Not all quality issues fit contract criteria - use bug reports for these cases.

---

## Bug Report Format

### BUG-[ID]: [Bug Title]

| Field | Value |
|-------|-------|
| **ID** | BUG-[sequential number] |
| **Title** | [Brief, descriptive title] |
| **Severity** | Critical / Major / Minor |
| **Status** | Open / In Progress / Fixed / Wontfix |
| **Discovered By** | [Evaluator Agent / Manual / Automated] |
| **Discovered Date** | [YYYY-MM-DD] |

---

## Issue Description

### What is the problem?
[Clear, concise description of the bug. Focus on the observable behavior, not the cause.]

### Where does it occur?
[Specific file, component, page, or API endpoint]

### When does it occur?
[Under what conditions or user actions does this bug appear]

---

## Steps to Reproduce

```
1. [First step - be specific]
2. [Second step]
3. [Third step]
4. [Continue as needed]
```

**Prerequisites**:
- [Any setup required before reproducing]
- [Test data or account needed]

---

## Expected vs Actual Behavior

### Expected Behavior
[What should happen according to requirements or best practices]

### Actual Behavior
[What actually happens - the bug]

### Impact
[User impact, business impact, or technical impact of this bug]

---

## Evidence

### Screenshots
[Links or embedded images showing the issue]

### Logs
```
[Paste relevant log output here]
```

### Code Reference
```
[File:Line reference or code snippet showing the issue]
```

---

## Severity Classification

### Critical
- System crash or data loss
- Security vulnerability
- Blocks core functionality
- No workaround available
- Example: Authentication bypass, database corruption

### Major
- Significant feature broken
- Major user impact
- Workaround exists but is difficult
- Example: Payment processing fails for certain cards, search returns no results

### Minor
- Cosmetic issue
- Minor inconvenience
- Easy workaround exists
- Example: Typo in error message, misaligned button, slight color inconsistency

---

## Suggested Fix

### Root Cause (if known)
[What is causing this bug at the code/architecture level]

### Recommended Solution
[How to fix the bug - be specific]

### Alternative Solutions
[Other approaches considered]

### Estimated Effort
- [ ] Small (< 1 hour)
- [ ] Medium (1-4 hours)
- [ ] Large (> 4 hours)

---

## Complete Bug Report Example

```markdown
### BUG-3: SQL Injection Vulnerability in Login Form

| Field | Value |
|-------|-------|
| **ID** | BUG-3 |
| **Title** | SQL Injection Vulnerability in Login Form |
| **Severity** | Critical |
| **Status** | Open |
| **Discovered By** | Evaluator Agent |
| **Discovered Date** | 2026-04-04 |

#### Issue Description

The login form accepts SQL injection strings without sanitization, potentially
allowing attackers to bypass authentication or extract user data.

**Location**: `/src/backend/routes/auth.py:45-52`
**Trigger**: Entering SQL injection payloads in the email field

#### Steps to Reproduce

```
1. Navigate to login page at /login
2. Enter "admin@example.com' OR '1'='1" in email field
3. Enter any password
4. Click "Sign In"
5. Observe successful authentication without valid credentials
```

**Prerequisites**: None, affects all users

#### Expected vs Actual Behavior

**Expected**: Login should reject malformed input and show error message.
**Actual**: Login succeeds with SQL injection payload, bypassing authentication.

**Impact**:
- Complete authentication bypass
- Potential data exfiltration
- Regulatory compliance violation (GDPR, etc.)
- User accounts at risk

#### Evidence

**Log Output**:
```
2026-04-04 14:23:15 [WARNING] Suspicious query executed:
SELECT * FROM users WHERE email = 'admin@example.com' OR '1'='1' AND password = '...'
```

**Code Reference**:
```python
# auth.py:45-52 - VULNERABLE CODE
@router.post("/login")
async def login(email: str, password: str):
    query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{hash(password)}'"
    # Direct string interpolation allows SQL injection
    user = db.execute(query)
    ...
```

#### Severity: Critical

Justification:
- Core functionality (authentication) completely bypassed
- No workaround - vulnerability is inherent to the code
- Security risk is severe
- Affects all users

#### Suggested Fix

**Root Cause**: User input is directly interpolated into SQL query without sanitization.

**Recommended Solution**:
```python
# Use parameterized queries
@router.post("/login")
async def login(email: str, password: str):
    query = "SELECT * FROM users WHERE email = $1 AND password = $2"
    user = db.execute(query, [email, hash(password)])
    ...
```

**Alternative Solutions**:
1. Use ORM with automatic parameterization
2. Add input validation layer before query
3. Use stored procedures

**Estimated Effort**: Small (< 1 hour)
```

---

## Bug Report Checklist

Before submitting a bug report, verify:

- [ ] **Reproducible**: Can someone else reproduce this bug?
- [ ] **Specific**: Is the location and trigger clearly identified?
- [ ] **Evidence**: Is there concrete evidence (logs, code, screenshots)?
- [ ] **Severity**: Is the severity correctly classified?
- [ ] **Actionable**: Is there a clear suggested fix?

---

## Bug Report Template (Copy)

```markdown
### BUG-[ID]: [Bug Title]

| Field | Value |
|-------|-------|
| **ID** | BUG-[] |
| **Title** | [] |
| **Severity** | Critical / Major / Minor |
| **Status** | Open |
| **Discovered By** | [] |
| **Discovered Date** | [YYYY-MM-DD] |

#### Issue Description

[What is the problem? Where does it occur? When does it happen?]

#### Steps to Reproduce

```
1. []
2. []
3. []
```

**Prerequisites**: []

#### Expected vs Actual Behavior

**Expected**: []
**Actual**: []
**Impact**: []

#### Evidence

**Screenshots**: []
**Logs**: []
**Code Reference**: []

#### Severity Justification

[Why this severity level?]

#### Suggested Fix

**Root Cause**: []
**Recommended Solution**: []
**Alternative Solutions**: []
**Estimated Effort**: Small / Medium / Large
```

---

## Tracking Bugs in Evaluation

When bugs are found during evaluation, they should be:

1. **Documented** using this template
2. **Linked** from the evaluation report
3. **Prioritized** by severity
4. **Assigned** for fixing (if FAIL verdict)
5. **Tracked** in the session state

### Bug Summary Table

Include in evaluation reports:

| ID | Title | Severity | Status | Action Required |
|----|-------|----------|--------|-----------------|
| BUG-1 | [Title] | Critical | Open | Fix before merge |
| BUG-2 | [Title] | Major | Open | Fix this sprint |
| BUG-3 | [Title] | Minor | Open | Backlog |

---

## Relationship to Criteria

Bugs differ from criteria failures:

| Aspect | Criteria Failure | Bug Report |
|--------|------------------|------------|
| Source | Sprint contract | Discovered during testing |
| Scope | Contract-defined | Any quality issue |
| Verdict Impact | Affects PASS/FAIL | Informational only |
| Resolution | Required for PASS | Prioritized separately |
| Tracking | In evaluation report | Separate bug tracker |

Use **criteria failures** for contract violations.
Use **bug reports** for issues outside contract scope.