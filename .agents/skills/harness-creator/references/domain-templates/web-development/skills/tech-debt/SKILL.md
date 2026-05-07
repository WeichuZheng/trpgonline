---
name: tech-debt
description: "Track, categorize, and prioritize technical debt across the codebase."
argument-hint: "[directory or 'all']"
user-invocable: true
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# Technical Debt Workflow

Scan, categorize, and prioritize technical debt for systematic reduction.

---

## Workflow

### Phase 1: Scan for Debt Indicators

Search for common debt patterns:

1. **TODO/FIXME comments**
   ```
   grep -rn "TODO\|FIXME\|HACK\|XXX" src/
   ```

2. **Deprecated patterns**
   - Old API usage
   - Outdated dependencies
   - Legacy code patterns

3. **Code smells**
   - Large files (>500 lines)
   - Deeply nested code (>4 levels)
   - Duplicate code patterns
   - Magic numbers without constants

4. **Missing tests**
   - Files with no corresponding test file
   - Low coverage areas

5. **Documentation gaps**
   - Missing docstrings
   - Outdated README
   - Missing ADRs for major decisions

---

### Phase 2: Categorize Debt

Group findings by category:

| Category | Examples |
|----------|----------|
| **Architecture** | Circular dependencies, module boundary violations |
| **Code Quality** | Duplicate code, large functions, magic numbers |
| **Testing** | Missing tests, low coverage, flaky tests |
| **Documentation** | Missing docs, outdated comments |
| **Dependencies** | Outdated packages, security vulnerabilities |
| **Performance** | N+1 queries, unindexed columns, memory leaks |
| **Security** | Hardcoded secrets, missing validation |

---

### Phase 3: Assess Severity

Rate each debt item:

| Severity | Criteria | Example |
|----------|----------|---------|
| **CRITICAL** | Blocks development or causes production issues | Security vulnerability, data loss risk |
| **HIGH** | Significantly impacts productivity or quality | Missing tests on critical path, broken CI |
| **MEDIUM** | Causes friction but has workaround | Code duplication, missing documentation |
| **LOW** | Nice to fix, low impact | Cosmetic issues, minor optimizations |

---

### Phase 4: Estimate Effort

Estimate time to resolve:

| Effort | Time | Criteria |
|--------|------|----------|
| **Small** | <2 hours | Localized fix, no dependencies |
| **Medium** | 2-8 hours | Multiple files, some testing needed |
| **Large** | 1-3 days | Architecture change, many files affected |
| **Epic** | >3 days | Major refactor, affects multiple teams |

---

### Phase 5: Prioritize

Calculate priority score:
```
Priority = Severity × Impact / Effort

CRITICAL = 4, HIGH = 3, MEDIUM = 2, LOW = 1
Epic = 4, Large = 3, Medium = 2, Small = 1
```

Higher score = Higher priority to fix.

---

### Phase 6: Generate Report

```markdown
# Technical Debt Report

## Summary

- Total Items: [N]
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

## Priority Queue

### Priority 1: CRITICAL Issues

| ID | Description | Category | Location | Effort |
|----|-------------|----------|----------|--------|
| TD-001 | [Description] | Security | file:line | Medium |

### Priority 2: HIGH Impact / Low Effort

| ID | Description | Category | Location | Effort |
|----|-------------|----------|----------|--------|

### Priority 3: Medium Priority Items

| ID | Description | Category | Location | Effort |
|----|-------------|----------|----------|--------|

## By Category

### Architecture
- [List of architecture debt]

### Code Quality
- [List of code quality debt]

### Testing
- [List of testing debt]

### Documentation
- [List of documentation debt]

### Dependencies
- [List of dependency debt]

## Recommended Sprint Allocation

- **This Sprint**: [Items to tackle now]
- **Next Sprint**: [Items to plan for]
- **Backlog**: [Items to track for later]

## Debt Reduction Strategy

1. [Recommended approach for systematic reduction]
2. [Process improvements to prevent new debt]
```