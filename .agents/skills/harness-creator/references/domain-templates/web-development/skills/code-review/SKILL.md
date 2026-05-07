---
name: code-review
description: "Architecture and quality code review for specified files or directories. Checks standards, patterns, security, and maintainability."
user-invocable: true
---

# Code Review Skill

You are facilitating the Code Review process. Your role is to review code for architecture, quality, security, and maintainability issues.

## Purpose

Code review ensures:
- Code follows project standards
- Architecture patterns are consistent
- Security vulnerabilities are caught
- Maintainability is preserved

## Review Flow

```
RECEIVE TARGET -> AUTOMATED CHECKS -> ARCHITECTURE REVIEW -> QUALITY REVIEW -> SECURITY REVIEW -> REPORT
```

## Review Categories

### 1. Architecture Review
- Does code follow established patterns?
- Are dependencies properly managed?
- Is the code in the correct domain?
- Are boundaries respected?

### 2. Quality Review
- Is code readable and maintainable?
- Are functions/classes appropriately sized?
- Is there proper error handling?
- Is there appropriate test coverage?

### 3. Security Review
- Is input validated?
- Are secrets properly managed?
- Is authentication verified?
- Are there injection vulnerabilities?

### 4. Standards Review
- Does code follow language conventions?
- Are naming conventions followed?
- Is documentation present?
- Is formatting consistent?

## Workflow

### Phase 1: Receive Target

1. Parse review request
2. Identify target files/directories
3. Determine domain context
4. Load applicable standards

### Phase 2: Automated Checks

Run automated checks:
- Linting (ESLint for JS, Pylint for Python)
- Formatting (Prettier, Black)
- Static analysis
- Test coverage

### Phase 3: Architecture Review

Check architecture:
- [ ] Code in correct domain directory
- [ ] Proper separation of concerns
- [ ] No circular dependencies
- [ ] API contracts followed
- [ ] State management patterns followed

### Phase 4: Quality Review

Check quality:
- [ ] Functions < 30 lines
- [ ] Files < 300 lines
- [ ] No deep nesting (> 3 levels)
- [ ] Error handling complete
- [ ] Tests cover critical paths

### Phase 5: Security Review

Check security:
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] Authentication verified
- [ ] No SQL injection risk
- [ ] No XSS risk
- [ ] CORS configured correctly

### Phase 6: Generate Report

Create review report with:
- Issues found (severity: Critical, Major, Minor)
- Recommendations
- Action items
- Pass/Fail verdict

## Review Report Template

```markdown
# Code Review: [Target]

**Reviewer**: [Agent name]
**Date**: [Date]
**Domain**: [Frontend/Backend/Database]

---

## Summary

| Category | Issues Found | Status |
|----------|--------------|--------|
| Architecture | [count] | PASS/FAIL |
| Quality | [count] | PASS/FAIL |
| Security | [count] | PASS/FAIL |
| Standards | [count] | PASS/FAIL |

**Overall**: PASS / FAIL

---

## Critical Issues (Must Fix)

### [Issue ID]: [Title]
- **File**: [path]
- **Line**: [number]
- **Category**: [Architecture/Quality/Security]
- **Issue**: [description]
- **Recommendation**: [how to fix]
- **Severity**: CRITICAL

---

## Major Issues (Should Fix)

### [Issue ID]: [Title]
- **File**: [path]
- **Line**: [number]
- **Category**: [Architecture/Quality/Security]
- **Issue**: [description]
- **Recommendation**: [how to fix]
- **Severity**: MAJOR

---

## Minor Issues (Nice to Fix)

### [Issue ID]: [Title]
- **File**: [path]
- **Line**: [number]
- **Category**: [Standards]
- **Issue**: [description]
- **Recommendation**: [how to fix]
- **Severity**: MINOR

---

## Positive Findings

- [Good practice 1]
- [Good practice 2]

---

## Action Items

| Priority | Action | Assignee |
|----------|--------|----------|
| P1 | [Action] | [Agent] |
| P2 | [Action] | [Agent] |

---

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

---

## Follow-up

- Re-review required: Yes/No
- Re-review after: [action items addressed]
```

## Severity Definitions

| Severity | Description | Action |
|----------|-------------|--------|
| CRITICAL | Must fix before merge | Blocks approval |
| MAJOR | Should fix | Requires documented plan to fix |
| MINOR | Nice to fix | Optional, documented |

## Domain-Specific Checks

### Frontend (frontend-lead domain)
- Component follows design system
- Accessibility attributes present
- Responsive design verified
- No inline styles (use design system)
- State management pattern followed

### Backend (backend-lead domain)
- API follows RESTful conventions
- Input validation in all endpoints
- Service layer separation
- Error handling consistent
- No business logic in routes

### Database (database-dev domain)
- Migrations reversible
- Indexes on query columns
- Foreign key constraints
- No N+1 query patterns
- Connection strings from env vars

## Common Issues by Category

### Architecture
- Code in wrong domain directory
- Circular dependencies
- Mixed concerns (UI + logic)
- Missing abstraction layers

### Quality
- Long functions (> 30 lines)
- Deep nesting (> 3 levels)
- Missing error handling
- Hardcoded values
- Missing tests

### Security
- Hardcoded secrets
- Missing input validation
- SQL injection risk
- XSS vulnerabilities
- CORS misconfiguration

### Standards
- Naming convention violations
- Missing documentation
- Formatting inconsistencies
- Unused imports/variables

## Usage

```
/code-review [target]
```

Example:
```
/code-review src/backend/api/user_routes.py
/code-review src/frontend/components/
```

## Coordination

- Domain reviews: Domain lead performs
- Cross-domain reviews: architect-lead performs
- Security focus: All leads review
- Pre-merge review: Required for all PRs