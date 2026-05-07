# Evaluation Criteria Template

> Use this template to define objective, testable criteria for sprint contracts.
> **Key Principle**: If you can't write a test for it, it's not a criterion.

---

## Criterion Definition Format

### [CRITERION ID]: [Criterion Name]

| Field | Value |
|-------|-------|
| **ID** | [Unique identifier, e.g., AC1, B1.1] |
| **Name** | [Clear, specific name] |
| **Description** | [What behavior or outcome to test] |
| **Category** | [Functional, Performance, Security, UX, etc.] |
| **Priority** | P1 (Blocker) / P2 (Important) / P3 (Nice-to-have) |
| **Weight** | [Impact on overall score: High/Medium/Low] |
| **Threshold** | [Minimum score to pass, typically 6/10] |

---

## Grading Guide

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceeds expectations, exceptional quality, no issues |
| 9/10 | Excellent | Meets all criteria fully, minor polish possible |
| 8/10 | Very Good | Meets criteria completely, small edge case issues |
| 7/10 | Good | Meets criteria well, some minor issues |
| 6/10 | Acceptable | Meets basic criteria, notable gaps or edge cases |
| 5/10 | Marginal | Partially meets criteria, significant improvements needed |
| 4/10 | Below Standard | Fails some aspects, needs rework |
| 3/10 | Poor | Major issues, substantial rework required |
| 2/10 | Very Poor | Critical failures, mostly broken |
| 1/10 | Fail | Does not meet criteria at all |
| 0/10 | No Attempt | Criterion not addressed |

### PASS/FAIL Determination

- **PASS**: Score >= threshold AND no critical issues
- **FAIL**: Score < threshold OR critical blocker found

---

## PASS Example

```
CRITERION: AC1 - User can log in with valid credentials

Status: PASS
Score: 9/10
Evidence:
- Tested login with 5 valid user accounts
- All logins succeeded within 500ms (requirement: < 2s)
- Session tokens correctly generated
- Redirect to dashboard works correctly
- Minor: Password field could show/hide toggle (P3 enhancement)

Action: None required for PASS. Optional: Add password visibility toggle.
```

---

## FAIL Example

```
CRITERION: AC2 - Invalid password shows error message

Status: FAIL
Score: 4/10
Evidence:
- Correct credentials show "Welcome" (expected)
- Wrong password shows "Invalid credentials" (correct)
- Empty password shows "Field required" (correct)
- SQL injection string '<script>alert(1)</script>' causes 500 error
- Password over 256 characters crashes the server
- No rate limiting on failed attempts (security risk)

Action:
1. Add input validation before database query
2. Implement length limits (max 128 chars)
3. Add rate limiting (max 5 attempts per minute)
4. Return generic error for malformed input
```

---

## Complete Criterion Template

```markdown
### [CRITERION ID]: [Criterion Name]

| Field | Value |
|-------|-------|
| **ID** | [e.g., AC1] |
| **Name** | [e.g., User Authentication Success] |
| **Description** | [e.g., User can successfully authenticate with valid credentials and receive appropriate feedback on authentication status] |
| **Category** | [e.g., Functional] |
| **Priority** | [P1/P2/P3] |
| **Weight** | [High/Medium/Low] |
| **Threshold** | 6/10 |

#### Test Conditions
- **Happy Path**: [What should work]
- **Edge Cases**: [Boundary conditions to test]
- **Error Cases**: [How errors should be handled]

#### Pass Condition
[Specific, measurable condition for PASS]

#### Fail Condition
[Specific conditions that constitute FAIL]

#### Testing Method
- [ ] Manual testing
- [ ] Automated tests
- [ ] Code review
- [ ] Performance testing
- [ ] Security testing

#### Dependencies
- [Other criteria this depends on]
- [External dependencies]

#### Notes
[Any additional context or considerations]
```

---

## Quality Checklist for Criteria

Before adding a criterion to the sprint contract, verify:

- [ ] **Specific**: Can a tester understand exactly what to test?
- [ ] **Measurable**: Can results be quantified (pass/fail, score)?
- [ ] **Achievable**: Is it realistic to implement in this sprint?
- [ ] **Relevant**: Does it directly relate to the sprint goals?
- [ ] **Testable**: Can evidence be gathered objectively?
- [ ] **Unambiguous**: Could two evaluators reach different conclusions?

---

## Priority Guidelines

### P1 (Blocker) - Must Pass
- Core functionality
- Security requirements
- Data integrity
- Critical user paths
- Legal/compliance requirements

### P2 (Important) - Should Pass
- User experience quality
- Performance standards
- Edge case handling
- Error messaging
- Cross-browser compatibility

### P3 (Nice-to-have) - Failure Acceptable
- Polish and refinements
- Optional features
- Future-proofing
- Documentation
- Minor UX improvements

---

## Common Pitfalls to Avoid

### Vague Criteria
- BAD: "The UI should look good"
- GOOD: "All form inputs have visible labels and error states appear within 100ms of validation failure"

### Untestable Criteria
- BAD: "The code should be clean"
- GOOD: "All functions have type annotations and cyclomatic complexity < 10"

### Subjective Criteria
- BAD: "The app should feel fast"
- GOOD: "Page load time is under 2 seconds on 3G connection"

### Missing Edge Cases
- BAD: "User can submit the form"
- GOOD: "User can submit valid forms, empty submissions show validation errors, and duplicate submissions are prevented"

---

## Example Criteria Set

### AC1: Login Authentication (P1)

| Field | Value |
|-------|-------|
| **ID** | AC1 |
| **Name** | Login Authentication |
| **Description** | User can authenticate with valid credentials |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: User enters valid credentials and is redirected to dashboard within 2 seconds.

**Fail Condition**: Valid credentials rejected, redirect fails, or response time > 2s.

---

### AC2: Error Feedback (P1)

| Field | Value |
|-------|-------|
| **ID** | AC2 |
| **Name** | Authentication Error Feedback |
| **Description** | Invalid credentials show appropriate error message |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Invalid credentials show "Invalid email or password" message within 500ms.

**Fail Condition**: No error shown, wrong error shown, or delayed > 500ms.

---

### AC3: Session Management (P2)

| Field | Value |
|-------|-------|
| **ID** | AC3 |
| **Name** | Session Persistence |
| **Description** | User session persists across page refreshes |
| **Category** | Functional |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Refreshing the page keeps user logged in for 24 hours.

**Fail Condition**: Session lost on refresh or expires before 24 hours.