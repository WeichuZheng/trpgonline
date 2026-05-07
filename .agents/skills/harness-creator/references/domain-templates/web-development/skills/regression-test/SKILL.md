---
name: regression-test
description: "Run and validate regression tests after changes to ensure no existing functionality is broken. Creates test execution report."
user-invocable: true
---

# Regression Test Skill

You are facilitating the Regression Testing process. Your role is to run tests after changes and verify no existing functionality is broken.

## Purpose

Regression testing ensures:
- Existing functionality stays intact after changes
- Tests cover critical paths
- Test failures are properly documented
- Changes are validated before merge

## Testing Flow

```
IDENTIFY SCOPE -> PRE-CHECK -> RUN TESTS -> ANALYZE RESULTS -> REPORT -> FIX IF NEEDED
```

## Workflow

### Phase 1: Identify Scope

1. Parse testing request
2. Identify what changed (from git diff)
3. Determine affected test categories:
   - Unit tests
   - Integration tests
   - E2E tests
4. Prioritize tests by affected areas

### Phase 2: Pre-Check

Before running tests:
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Database migrations applied
- [ ] Services running (if integration tests)

### Phase 3: Run Tests

Run test suites in order:

1. **Unit Tests** (fast, isolated)
   - Frontend component tests
   - Backend service tests
   - Database model tests

2. **Integration Tests** (slower, connected)
   - API endpoint tests
   - Frontend + API integration
   - Database integration

3. **E2E Tests** (slowest, full stack)
   - Critical user flows
   - Cross-domain functionality

### Phase 4: Analyze Results

For each test:
- Pass: Document
- Fail: Investigate root cause
- Skip: Document reason

### Phase 5: Report

Generate test report with:
- Summary (pass/fail counts)
- Failed test details
- Coverage metrics
- Recommendations

### Phase 6: Fix If Needed

If tests fail:
1. Analyze failure cause
2. Determine if change broke test or test is wrong
3. Fix code or update test
4. Re-run to verify

## Test Report Template

```markdown
# Regression Test Report

**Date**: [Date]
**Trigger**: [What triggered this test run]
**Scope**: [What tests were run]

---

## Summary

| Category | Total | Passed | Failed | Skipped |
|----------|-------|--------|--------|---------|
| Unit Tests | [n] | [n] | [n] | [n] |
| Integration Tests | [n] | [n] | [n] | [n] |
| E2E Tests | [n] | [n] | [n] | [n] |
| **Total** | [n] | [n] | [n] | [n] |

**Status**: PASS / FAIL

**Coverage**: [percentage]%

---

## Failed Tests

### [Test Name]
- **File**: [test file path]
- **Error**: [error message]
- **Cause**: [root cause analysis]
- **Action**: [Fix code / Update test / Known issue]

### [Test Name 2]
- **File**: [test file path]
- **Error**: [error message]
- **Cause**: [root cause analysis]
- **Action**: [Fix code / Update test / Known issue]

---

## Skipped Tests

| Test | Reason |
|------|--------|
| [Test name] | [Reason for skipping] |

---

## Coverage Metrics

| Domain | Coverage | Target | Status |
|--------|----------|--------|--------|
| Frontend | [%] | 80% | PASS/FAIL |
| Backend | [%] | 80% | PASS/FAIL |
| Database | [%] | 70% | PASS/FAIL |

---

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

---

## Action Items

| Priority | Action | Assignee |
|----------|--------|----------|
| P1 | [Fix failed test] | [Agent] |
| P2 | [Add missing test] | [Agent] |

---

## Next Steps

- [ ] Fix failed tests
- [ ] Re-run regression
- [ ] Merge if all tests pass
```

## Test Categories by Domain

### Frontend Tests
- Component rendering tests
- Hook behavior tests
- Integration tests (API calls)
- Accessibility tests
- Responsive design tests

### Backend Tests
- API endpoint tests
- Service layer tests
- Model/validation tests
- Authentication tests
- Error handling tests

### Database Tests
- Model integrity tests
- Migration tests
- Query performance tests
- Constraint tests

## Test Commands

### Frontend (React/Vue)
```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

### Backend (FastAPI/Flask)
```bash
# Unit tests
pytest tests/unit

# Integration tests
pytest tests/integration

# Coverage
pytest --cov=src --cov-report=html
```

## Failure Analysis Guide

### Test Failure Patterns

| Pattern | Likely Cause | Action |
|---------|--------------|--------|
| Assertion failed | Logic change | Check if change is intentional |
| Timeout | Performance issue | Investigate slow operation |
| Missing element | UI changed | Update selector or fix UI |
| Auth error | Auth change | Update test auth setup |
| DB error | Schema change | Update test fixtures |

### Root Cause Questions

1. Did the change modify the tested behavior?
2. Is the test using outdated data/fixtures?
3. Did environment configuration change?
4. Is there a dependency issue?

## Coverage Targets

| Domain | Minimum Target | Recommended |
|--------|----------------|-------------|
| Frontend | 70% | 80% |
| Backend | 80% | 90% |
| Database | 70% | 75% |
| Critical Paths | 100% | 100% |

## Anti-Patterns to Avoid

- Running tests without analyzing failures
- Skipping failed tests without documentation
- Low coverage on critical paths
- Not testing error scenarios

## Usage

```
/regression-test
/regression-test [scope]
```

Example:
```
/regression-test
/regression-test backend
/regression-test src/frontend/components/
```

## Coordination

- Test failures: Notify domain lead
- Cross-domain failures: Notify architect-lead
- Critical failures: Block merge
- Coverage drops: Require investigation