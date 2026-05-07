# Evaluation Standards Documentation

> This document establishes standards and best practices for evaluation within the Dev-Squad framework. It serves as the reference guide for creating, tuning, and applying evaluation criteria.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Default Criteria Categories](#default-criteria-categories)
3. [Defining New Criteria](#defining-new-criteria)
4. [Tuning Evaluator Behavior](#tuning-evaluator-behavior)
5. [Well-Calibrated Evaluation Examples](#well-calibrated-evaluation-examples)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
7. [Calibration Process](#calibration-process)

---

## Core Principles

### The Evaluator's Mindset

**Key Principle from Anthropic**: "Tune the Evaluator: Skeptical prompting, few-shot examples, calibrate against human judgment"

The evaluator is not a rubber stamp. Its job is to find issues, not justify work.

| Mindset Aspect | Correct Approach | Incorrect Approach |
|----------------|------------------|-------------------|
| Default assumption | Something is wrong until proven right | Give benefit of the doubt |
| Edge cases | Actively seek boundary conditions | Test only happy paths |
| Evidence | Require specific, observable proof | Accept vague claims |
| Feedback | Provide actionable fixes | Note problems without solutions |
| Severity | Classify accurately, not generously | Downgrade issues to be nice |

### Three Pillars of Evaluation

1. **Objectivity**: Criteria must be testable and measurable
2. **Consistency**: Same work should receive same evaluation
3. **Actionability**: Every issue must have a clear path to resolution

---

## Default Criteria Categories

The framework uses three primary evaluation categories. Each addresses a distinct quality dimension.

### 1. Functionality

**Question**: Does it work?

| Aspect | What It Covers | Example Tests |
|--------|----------------|----------------|
| Features | Core capabilities work as specified | User can log in with valid credentials |
| Behaviors | Expected responses to user actions | Form validation shows error messages |
| Edge Cases | Boundary conditions handled | Empty input, max length, special characters |
| Error Handling | Graceful failure modes | Network error shows retry option |
| Integration | Components work together | API returns data, UI displays correctly |

#### Functionality Grading

| Score | Rating | Characteristics |
|-------|--------|-----------------|
| 10/10 | Perfect | All features work, edge cases handled, polished UX |
| 8-9/10 | Excellent | All features work, minor edge case gaps |
| 6-7/10 | Good | Core features work, some edge cases fail |
| 4-5/10 | Acceptable | Main path works, notable gaps |
| 2-3/10 | Poor | Core features incomplete or buggy |
| 0-1/10 | Fail | Feature broken or missing |

#### Functionality Evaluation Checklist

```markdown
## Happy Path Testing
- [ ] Primary use case works end-to-end
- [ ] Success feedback is clear
- [ ] Data persists correctly

## Edge Case Testing
- [ ] Empty input handled
- [ ] Maximum input handled
- [ ] Special characters handled
- [ ] Unicode/emoji handled
- [ ] Malformed input handled

## Error Case Testing
- [ ] Network errors handled gracefully
- [ ] Timeout errors handled
- [ ] Server errors show user-friendly message
- [ ] User can recover from errors

## Integration Testing
- [ ] Frontend displays backend data correctly
- [ ] State management works across components
- [ ] External services integrate properly
```

---

### 2. Code Quality

**Question**: Is it well-built?

| Aspect | What It Covers | Example Tests |
|--------|----------------|----------------|
| Structure | Organization and architecture | Modules separated, dependencies clear |
| Conventions | Style and naming standards | Consistent naming, proper formatting |
| Maintainability | Ease of future changes | Low complexity, good documentation |
| Duplication | DRY principle adherence | No copy-paste code blocks |
| Security | Vulnerability prevention | No hardcoded secrets, input sanitized |

#### Code Quality Grading

| Score | Rating | Characteristics |
|-------|--------|-----------------|
| 10/10 | Perfect | Clean architecture, documented, no issues |
| 8-9/10 | Excellent | Well-structured, minor improvements possible |
| 6-7/10 | Good | Structured, some complexity or duplication |
| 4-5/10 | Acceptable | Functional but needs refactoring |
| 2-3/10 | Poor | Hard to maintain, significant issues |
| 0-1/10 | Fail | Unmaintainable, critical issues |

#### Code Quality Metrics

| Metric | Threshold | How to Measure |
|--------|-----------|----------------|
| Function length | < 50 lines | Count lines per function |
| File length | < 500 lines | Count lines per file |
| Cyclomatic complexity | < 10 | Use complexity analyzer |
| Duplication percentage | < 5% | Use duplication detector |
| Documentation coverage | > 80% | Public APIs documented |
| Test coverage | > 80% | Critical paths tested |

#### Code Quality Evaluation Checklist

```markdown
## Structure
- [ ] Modules well-separated
- [ ] Responsibilities clear
- [ ] Dependencies explicit
- [ ] Abstractions appropriate

## Conventions
- [ ] Naming consistent and descriptive
- [ ] Formatting consistent
- [ ] Types specified (if applicable)
- [ ] Comments for complex logic

## Maintainability
- [ ] Functions focused (single responsibility)
- [ ] No deep nesting (> 3 levels)
- [ ] No magic numbers
- [ ] Error handling comprehensive

## Security
- [ ] No hardcoded secrets
- [ ] Input validated and sanitized
- [ ] Authentication checked
- [ ] Authorization verified
```

---

### 3. Design Quality

**Question**: Is it usable?

| Aspect | What It Covers | Example Tests |
|--------|----------------|----------------|
| Visual Hierarchy | Clear importance and flow | Primary action prominent |
| Responsiveness | Works across devices | Mobile, tablet, desktop layouts |
| Accessibility | Usable by all users | Screen reader compatible, keyboard navigable |
| Interaction | Predictable behavior | Hover states, loading indicators |
| Consistency | Unified look and feel | Colors, typography, spacing |

#### Design Quality Grading

| Score | Rating | Characteristics |
|-------|--------|-----------------|
| 10/10 | Perfect | Professional, accessible, polished |
| 8-9/10 | Excellent | Minor inconsistencies or polish needed |
| 6-7/10 | Good | Usable, some hierarchy or accessibility issues |
| 4-5/10 | Acceptable | Functional but notable UX issues |
| 2-3/10 | Poor | Difficult to use, accessibility failures |
| 0-1/10 | Fail | Unusable, critical accessibility issues |

#### Design Quality Standards

| Standard | Requirement | Tool to Verify |
|----------|-------------|-----------------|
| Color contrast | 4.5:1 minimum (WCAG AA) | Chrome DevTools, WebAIM |
| Touch targets | 44x44px minimum | Chrome DevTools |
| Font size | 16px minimum body | Browser inspector |
| Focus visible | Clear focus indicator | Keyboard testing |
| Alt text | All images described | Screen reader testing |

#### Design Quality Evaluation Checklist

```markdown
## Visual Hierarchy
- [ ] Primary action prominent
- [ ] Secondary actions de-emphasized
- [ ] Spacing consistent (4px/8px grid)
- [ ] Typography creates hierarchy

## Responsiveness
- [ ] Mobile (375px) works
- [ ] Tablet (768px) works
- [ ] Desktop (1024px+) works
- [ ] No horizontal scroll
- [ ] Touch targets adequate

## Accessibility
- [ ] Keyboard navigation works
- [ ] Focus visible
- [ ] Alt text for images
- [ ] Form labels present
- [ ] Heading hierarchy correct
- [ ] Color contrast sufficient
- [ ] Not relying on color alone

## Interaction
- [ ] Hover states present
- [ ] Loading indicators for async
- [ ] Error messages clear
- [ ] Success feedback provided
```

---

## Defining New Criteria

When teams need custom criteria, follow this structured process.

### Step 1: Start from User-Facing Behavior

Good criteria describe what users experience, not implementation details.

| Bad Criterion | Good Criterion |
|---------------|----------------|
| Uses Redis cache | Page loads within 2 seconds |
| Implements JWT auth | User stays logged in for 24 hours |
| Follows MVC pattern | User can complete task in under 5 clicks |
| Uses TypeScript | No type errors in production |

### Step 2: Make It Testable

Every criterion must have a clear pass/fail test.

```markdown
### Untestable Criterion
ID: UX1
Name: Good user experience
Description: The app should feel fast and intuitive

### Testable Criterion
ID: UX1
Name: Page load performance
Description: Initial page load completes within 2 seconds on 3G connection
Test Method:
  1. Open Chrome DevTools
  2. Set network throttling to "Fast 3G"
  3. Clear cache and reload
  4. Measure time to interactive
Pass Condition: Time to interactive < 2000ms
Fail Condition: Time to interactive >= 2000ms
```

### Step 3: Assign Priority and Weight

| Priority | Meaning | Pass Requirement |
|----------|---------|------------------|
| P1 (Blocker) | Core functionality, security, data integrity | Must pass |
| P2 (Important) | UX quality, performance, edge cases | Should pass (30% threshold) |
| P3 (Nice-to-have) | Polish, refinements, future-proofing | Failure acceptable |

### Step 4: Define Grading Thresholds

| Score | Threshold Description |
|-------|----------------------|
| 10/10 | Exceptional, exceeds requirements |
| 9/10 | Fully meets requirements, minor polish possible |
| 8/10 | Meets requirements, small edge case issues |
| 7/10 | Good, some issues but acceptable |
| 6/10 | Acceptable, notable gaps, minimum pass |
| 5/10 | Marginal, significant improvements needed |
| 4/10 | Below standard, needs rework |
| 3/10 | Poor, major issues |
| 2/10 | Very poor, critical failures |
| 1/10 | Fail, mostly broken |
| 0/10 | No attempt or not addressed |

### Step 5: Write Examples

Include both passing and failing examples for clarity.

```markdown
### PASS Example

CRITERION: P1 - User can log in with valid credentials

Status: PASS
Score: 9/10

Evidence:
- Tested login with 5 valid user accounts
- All logins succeeded within 500ms (requirement: < 2s)
- Session tokens correctly generated
- Redirect to dashboard works correctly
- Minor: Password field could show/hide toggle (P3 enhancement)

Action: None required for PASS

### FAIL Example

CRITERION: P1 - User can log in with valid credentials

Status: FAIL
Score: 4/10

Evidence:
- Login with correct credentials shows "Welcome" message
- However: SQL injection string '<script>alert(1)</script>' causes 500 error
- Password over 256 characters crashes the server
- No rate limiting on failed attempts (security risk)
- Response time exceeds 2s on slow network

Action:
1. Add input validation before database query
2. Implement length limits (max 128 chars)
3. Add rate limiting (max 5 attempts per minute)
4. Return generic error for malformed input
```

### New Criteria Template

```markdown
### [CRITERION ID]: [Criterion Name]

| Field | Value |
|-------|-------|
| **ID** | [Unique identifier, e.g., P1, UX2, SEC3] |
| **Name** | [Clear, specific name] |
| **Description** | [What behavior or outcome to test] |
| **Category** | [Functionality, Code-Quality, Design-Quality, Performance, Security] |
| **Priority** | P1 (Blocker) / P2 (Important) / P3 (Nice-to-have) |
| **Weight** | High / Medium / Low |
| **Threshold** | [Minimum score to pass, typically 6/10] |

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

#### Examples
##### PASS Example
[Specific example of passing evaluation]

##### FAIL Example
[Specific example of failing evaluation]
```

---

## Tuning Evaluator Behavior

Effective evaluation requires careful calibration of the evaluator's behavior.

### Skeptical Prompting

The evaluator should be instructed to find issues, not justify work.

#### System Prompts for Skeptical Evaluation

```markdown
## Bad: Lenient Evaluation Prompt

You are an evaluator. Review the code and provide feedback.
Check if it works and looks good.

## Good: Skeptical Evaluation Prompt

You are a critical evaluator whose job is to find issues.
You did NOT build this feature. Your job is to find problems, not justify shortcuts.

Default assumptions:
- Something is probably wrong until you prove it right
- Edge cases are likely unhandled
- Security vulnerabilities may exist
- Performance may degrade under load

Testing approach:
1. Happy path first (does it work normally?)
2. Edge cases second (what breaks it?)
3. Error handling third (what happens when things go wrong?)
4. Security last (what can be exploited?)

Report every issue found, no matter how small. Better to over-report than under-report.
```

### Few-Shot Examples

Provide examples of good and bad evaluations to calibrate expectations.

#### Good Evaluation Example

```markdown
CRITERION: Form Validation

Status: FAIL
Score: 4/10

Evidence:
Tested with 10 input combinations:

Valid inputs:
- "test@example.com" / "Password123!" -> Success (correct)
- "user@domain.co.uk" / "Pass!234" -> Success (correct)

Invalid inputs:
- Empty email -> "Email required" (correct)
- Invalid format "test@" -> "Invalid email" (correct)
- Empty password -> "Password required" (correct)

Edge cases:
- Email with spaces "test @example.com" -> Accepted (BUG: should trim)
- Password with 1000 characters -> Server 500 error (BUG: no length limit)
- SQL injection "' OR '1'='1" -> Logged in (CRITICAL: SQL injection)
- XSS in email "<script>alert(1)</script>" -> Stored and executed (CRITICAL: XSS)
- Unicode email "test@example.中国" -> Accepted (correct)

Security issues found:
1. SQL injection in email field (CRITICAL)
2. XSS vulnerability in email field (CRITICAL)
3. No password length validation (HIGH)

Action:
1. URGENT: Parameterize SQL queries (use prepared statements)
2. URGENT: Sanitize and validate email before display
3. Add max length validation (128 chars email, 64 chars password)
4. Trim whitespace from email input
```

#### Bad Evaluation Example

```markdown
CRITERION: Form Validation

Status: PASS
Score: 10/10

Evidence:
Tested login form. Works correctly for valid and invalid inputs.
Action: None needed
```

**Why this is bad:**
- No edge cases tested
- No security testing
- No specific evidence
- Assumes everything works without verification

### Calibration Against Human Judgment

Regularly compare evaluator scores with human review.

#### Calibration Process

```markdown
## Step 1: Select Sample
Choose 10-20 recent evaluations representing:
- Different feature types (auth, CRUD, integration)
- Different quality levels (excellent to poor)
- Different evaluators (if applicable)

## Step 2: Human Review
Have senior engineers independently review and score:
- Use same criteria as evaluator
- Document specific evidence
- Provide scores on same scale

## Step 3: Compare Results
For each evaluation:
| Criterion | Evaluator Score | Human Score | Delta | Notes |
|----------|-----------------|-------------|-------|-------|
| [ID] | X/10 | Y/10 | +Z | [Analysis] |

## Step 4: Identify Patterns
- Is evaluator consistently higher/lower?
- Does evaluator miss certain issue types?
- Are there edge cases evaluator doesn't test?

## Step 5: Adjust Prompting
Based on patterns:
- Add instructions for missed issue types
- Include more specific examples
- Adjust scoring guidance
```

#### Calibration Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Score correlation | > 0.85 | Correlation coefficient between evaluator and human |
| Pass/fail accuracy | > 90% | Agreement on pass/fail verdicts |
| Issue detection rate | > 80% | Human issues found by evaluator |
| False positive rate | < 20% | Evaluator issues not confirmed by human |

### Feedback Loops

Learn from cases where evaluator was too harsh or lenient.

#### Feedback Collection

```markdown
## Post-Evaluation Review

After each evaluation, track:

### If evaluator was TOO HARSH:
- What issues were flagged but shouldn't have been?
- What was the actual user/business impact?
- Was the severity classification correct?

### If evaluator was TOO LENIENT:
- What issues were missed?
- What issues were under-classified?
- What problems appeared in production?

### Record as Calibration Data
| Date | Feature | Evaluator | Human | Verdict | Notes |
|------|---------|-----------|-------|---------|-------|
| [Date] | [Feature] | [Score] | [Score] | [Harsh/Lenient] | [Details] |
```

---

## Well-Calibrated Evaluation Examples

### Example 1: Correctly Identifying Missing Edge Cases

```markdown
CRITERION: AC3 - User profile update

Status: FAIL
Score: 5/10

Evidence:
Happy path tests:
- Update display name -> Success (correct)
- Update email -> Success with verification email (correct)
- Update password -> Success with re-auth prompt (correct)

Edge case tests:
- Empty display name -> Cleared successfully (ISSUE: should require minimum length)
- Display name with 1000 characters -> Saved (ISSUE: no max length)
- Email already in use -> "Email already taken" (correct)
- Special characters in name "<script>alert(1)</script>" -> Saved (ISSUE: XSS risk)
- Unicode name "日本語" -> Saved correctly (correct)
- Profile update while offline -> No error, silent failure (ISSUE: should queue or notify)

Issues found:
1. No minimum display name length (could be 1 char)
2. No maximum display name length (performance risk)
3. XSS vulnerability in display name
4. Offline update fails silently

Severity:
- P1: XSS vulnerability (security)
- P2: Silent offline failure (data loss risk)
- P3: No length validation (polish)

Action:
1. Sanitize display name for HTML output
2. Add offline handling with queue or user notification
3. Add length validation (2-50 chars)
```

**Why this is good:**
- Tested beyond happy path
- Found real security and UX issues
- Classified severity appropriately
- Provided specific, actionable fixes

### Example 2: Finding Subtle Integration Issues

```markdown
CRITERION: INT1 - Shopping cart persistence

Status: FAIL
Score: 4/10

Evidence:
Basic functionality:
- Add item to cart -> Appears in cart (correct)
- Remove item from cart -> Removed from cart (correct)
- Refresh page -> Cart persists (correct)

Integration tests:
- Add item, navigate away, return -> Cart preserved (correct)
- Add item in tab A, check tab B -> Cart synchronized (correct)
- Add item, close browser, return -> Cart preserved (correct)
- Add item, checkout, complete order -> Cart cleared (correct)

Edge case tests:
- Add 100 items -> Cart works, but slow (ISSUE: no pagination)
- Add out-of-stock item -> Added but checkout blocked (ISSUE: should prevent add)
- Add item, price changes -> Old price shown at checkout (ISSUE: stale pricing)
- Add item, product deleted -> Checkout shows error (ISSUE: should validate)
- Add item, switch currency -> Prices not converted (ISSUE: currency ignored)

Race condition tests:
- Rapid add/remove in two tabs -> Cart state inconsistent (BUG)
- Add item during checkout -> Item not included but cart shows it (BUG)

Issues found:
1. Cart state race condition between tabs
2. Stale pricing after price change
3. Allows adding out-of-stock items
4. Deleted products cause checkout failure
5. Currency switch not reflected
6. No pagination for large carts

Severity:
- P1: Race condition (data integrity)
- P1: Stale pricing (financial)
- P2: Deleted products crash checkout
- P2: Out-of-stock items allowed
- P3: Currency not reflected
- P3: No pagination

Action:
1. Implement cart locking during checkout
2. Add real-time price validation at checkout
3. Validate product availability before adding
4. Handle deleted products gracefully
5. Recalculate on currency change
6. Add pagination for > 20 items
```

**Why this is good:**
- Tested integration scenarios
- Found race conditions
- Identified financial risk
- Provided comprehensive fixes

### Example 3: Providing Actionable Feedback

```markdown
CRITERION: UX2 - Form error handling

Status: FAIL
Score: 3/10

Evidence:
Error scenarios tested:
1. Submit empty form
   - Expected: Field-level error messages
   - Actual: Generic "Error submitting form" at top
   - Impact: User doesn't know what to fix

2. Submit invalid email format
   - Expected: "Please enter a valid email"
   - Actual: "Invalid input"
   - Impact: Unclear what's wrong

3. Submit weak password
   - Expected: "Password must be at least 8 characters with uppercase, lowercase, and number"
   - Actual: "Password too weak"
   - Impact: User doesn't know requirements

4. Server timeout during submission
   - Expected: "Request timed out. Please try again."
   - Actual: Blank page with spinner forever
   - Impact: User stuck, doesn't know if submission succeeded

5. Duplicate email registration
   - Expected: "An account with this email already exists"
   - Actual: "Error: duplicate key value violates unique constraint"
   - Impact: Exposes database details, confusing to user

6. Network disconnected during submission
   - Expected: "No internet connection. Please check your network."
   - Actual: Generic "Error submitting form"
   - Impact: User blames system, not their connection

Issues found:
1. No field-level validation messages
2. Generic error messages don't help users
3. Loading state has no timeout
4. Server errors expose implementation details
5. No retry mechanism for transient failures

Fix recommendations:
1. src/components/Form.tsx:45 - Add field-level error display
   ```tsx
   {errors.email && <span className="error">{errors.email.message}</span>}
   ```

2. src/utils/validators.ts - Add specific validation messages
   ```ts
   email: "Please enter a valid email address (example@domain.com)"
   password: "Password must be at least 8 characters and include uppercase, lowercase, and a number"
   ```

3. src/hooks/useFormSubmit.ts:23 - Add timeout handling
   ```ts
   const TIMEOUT = 10000; // 10 seconds
   const timeoutId = setTimeout(() => setError("Request timed out"), TIMEOUT);
   ```

4. src/api/client.ts:67 - Sanitize error messages
   ```ts
   if (error.code === '23505') {
     return "An account with this email already exists";
   }
   ```

5. src/components/Form.tsx:78 - Add retry button
   ```tsx
   {error && <button onClick={retry}>Try Again</button>}
   ```
```

**Why this is good:**
- Tested specific error scenarios
- Described expected vs actual behavior
- Explained user impact
- Provided specific file locations
- Gave code examples for fixes

### Example 4: Appropriate Severity Classification

```markdown
CRITERION: SEC1 - Authentication security

Status: FAIL
Score: 3/10

Evidence:
Security tests performed:

PASS:
- Uses bcrypt for password hashing (cost factor 12)
- HTTPS enforced on all pages
- Session tokens are cryptographically random
- Logout clears session server-side

FAIL - CRITICAL:
1. No rate limiting on login endpoint
   - Tested: 100 requests/second succeeded
   - Risk: Brute force password attacks
   - Severity: CRITICAL (security)
   - Fix: Add rate limiting (5 attempts per minute per IP)

2. JWT tokens never expire
   - Tested: Week-old token still valid
   - Risk: Stolen tokens usable forever
   - Severity: CRITICAL (security)
   - Fix: Set token expiry (15 minutes access, 7 days refresh)

3. Password reset token single-use not enforced
   - Tested: Used same reset link twice
   - Risk: Link reuse after account recovery
   - Severity: HIGH (security)
   - Fix: Invalidate token after first use

FAIL - HIGH:
4. Session not invalidated on password change
   - Tested: Changed password, old session still valid
   - Risk: Compromised accounts stay compromised
   - Severity: HIGH (security)
   - Fix: Invalidate all sessions on password change

5. No password strength validation
   - Tested: "password" accepted as password
   - Risk: Weak passwords easily compromised
   - Severity: HIGH (security)
   - Fix: Enforce minimum strength (8 chars, mixed case, number)

FAIL - MEDIUM:
6. Error messages reveal user existence
   - Tested: "User not found" vs "Invalid password"
   - Risk: Username enumeration
   - Severity: MEDIUM (security)
   - Fix: Use generic "Invalid credentials" for both

Summary:
- 2 CRITICAL issues (blocks any deployment)
- 2 HIGH issues (blocks production)
- 1 MEDIUM issue (should fix)
- Overall: FAIL - critical security vulnerabilities

Action:
CRITICAL issues must be fixed before any deployment:
1. Add rate limiting to /auth/login endpoint
2. Configure JWT token expiration

HIGH issues must be fixed before production:
3. Implement token invalidation after use
4. Invalidate sessions on password change
5. Add password strength requirements
```

**Why this is good:**
- Clear severity classification
- Distinguished critical from medium
- Prioritized fixes appropriately
- Explained security impact
- Blocked deployment for critical issues

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Rubber Stamp Evaluation

```markdown
## BAD: Rubber Stamp

Status: PASS
Score: 10/10
Evidence: Everything looks good. Good job!
```

**Problems:**
- No specific evidence
- No edge case testing
- No actionable feedback
- Assumes perfection

**Fix:** Always test edge cases, provide specific evidence, find at least minor issues.

### Anti-Pattern 2: Vague Feedback

```markdown
## BAD: Vague Feedback

Status: FAIL
Score: 5/10
Evidence: The code has some issues with structure and could be cleaner.
Action: Refactor and improve.
```

**Problems:**
- No specific issues identified
- No file/line references
- No actionable fixes
- Developer doesn't know what to change

**Fix:** Every issue needs specific location, description, and fix.

### Anti-Pattern 3: Testing Only Happy Path

```markdown
## BAD: Only Happy Path

Status: PASS
Score: 9/10
Evidence:
- Login works with valid credentials
- Logout works
- Session persists across refresh
Action: None needed
```

**Problems:**
- No edge case testing
- No security testing
- No error scenario testing
- Issues missed

**Fix:** Always test: happy path, edge cases, error cases, security.

### Anti-Pattern 4: Downgrading Severity

```markdown
## BAD: Severity Downgrade

Issue: SQL injection vulnerability in login form
Severity: LOW (it's behind login, probably fine)
Action: Fix when convenient
```

**Problems:**
- SQL injection is always critical
- "Behind login" is not a valid defense
- Should block deployment

**Fix:** Classify severity accurately regardless of context.

### Anti-Pattern 5: Accepting "Good Enough"

```markdown
## BAD: Good Enough

Status: PASS
Score: 6/10
Evidence: Works most of the time. Edge cases fail but users probably won't hit them.
Action: None
```

**Problems:**
- Assumes user behavior
- Ignores real issues
- False confidence

**Fix:** If edge cases fail, score should reflect that. Users will find every edge case.

---

## Calibration Process

### Regular Calibration Routine

```markdown
## Weekly Calibration (15 minutes)

1. Review 3 evaluations from this week
2. For each, ask:
   - Did I find issues the generator might have missed?
   - Was I skeptical enough?
   - Was my feedback actionable?
   - Were my severity classifications accurate?

3. Adjust approach based on findings

## Monthly Calibration (1 hour)

1. Select 5 evaluations for human review
2. Have senior engineer review same work independently
3. Compare scores and findings
4. Identify patterns:
   - Consistently missing certain issue types?
   - Scoring too high/low?
   - Missing edge cases?

5. Update evaluation prompts based on learnings

## Quarterly Review (2 hours)

1. Analyze all evaluation trends
2. Identify systematic issues
3. Update criteria definitions
4. Retrain on new examples
5. Document calibration changes
```

### Calibration Checklist

```markdown
## Before Each Evaluation
- [ ] Remember: You did NOT build this. Be skeptical.
- [ ] Plan to test: happy path, edge cases, errors, security
- [ ] Assume something is wrong until proven right

## During Evaluation
- [ ] Record specific evidence (files, lines, values)
- [ ] Classify severity accurately
- [ ] Provide actionable fixes
- [ ] Consider user impact, not just code quality

## After Evaluation
- [ ] Would a human reviewer agree with this?
- [ ] Did I test enough edge cases?
- [ ] Is my feedback actionable?
- [ ] Did I miss anything obvious?
```

---

## Summary

Effective evaluation requires:

| Principle | Practice |
|-----------|----------|
| Skeptical mindset | Assume issues exist until proven otherwise |
| Testable criteria | Every criterion must have clear pass/fail test |
| Specific evidence | File, line, input, output, expected, actual |
| Actionable feedback | Every issue needs a fix, not just identification |
| Accurate severity | Classify by impact, not by likelihood of being found |
| Regular calibration | Compare with human judgment, adjust prompts |

The goal of evaluation is to catch issues before they reach production, not to approve work. A strict evaluator saves time and prevents bugs.