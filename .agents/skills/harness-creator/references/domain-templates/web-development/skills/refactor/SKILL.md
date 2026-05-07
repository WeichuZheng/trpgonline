---
name: refactor
description: "Guided refactoring workflow for improving existing code without changing behavior. Ensures tests pass before and after changes."
user-invocable: true
---

# Refactor Skill

You are facilitating the Refactoring process. Your role is to guide code improvement while preserving existing behavior.

## Purpose

Refactoring ensures:
- Code quality improves without behavior changes
- Tests verify functionality stays intact
- Changes are incremental and reversible
- Documentation reflects the new structure

## Refactoring Flow

```
IDENTIFY TARGET -> TEST BASELINE -> PLAN CHANGES -> INCREMENTAL REFACTOR -> VERIFY -> COMPLETE
```

## Refactoring Principles

### Key Rules

1. **Test First**: All existing tests must pass before starting
2. **Small Steps**: Each change should be small and reversible
3. **Behavior Preserved**: Functionality must not change
4. **Run Tests Often**: Verify after each step

### Red-Green-Refactor Cycle

```
1. Ensure tests pass (GREEN)
2. Make a small refactor
3. Run tests (should stay GREEN)
4. If tests fail (RED), revert and try smaller change
5. Repeat until refactor complete
```

## Workflow

### Phase 1: Identify Target

1. Parse the refactoring request
2. Identify target files/modules
3. Document current structure
4. List what needs improvement

### Phase 2: Test Baseline

1. Run all existing tests
2. Document test coverage
3. Identify any failing tests (fix first)
4. Create baseline test results

**IMPORTANT**: If tests don't pass, fix them before refactoring.

### Phase 3: Plan Changes

Create refactoring plan with:
- Specific changes to make
- Order of changes (dependencies)
- Risk level for each change
- Rollback points

### Phase 4: Incremental Refactor

For each change:
1. Make the smallest possible change
2. Run tests immediately
3. Commit if tests pass
4. Document the change

### Phase 5: Verify

1. Run full test suite
2. Check coverage hasn't decreased
3. Verify behavior unchanged
4. Check performance impact

### Phase 6: Complete

1. Update documentation
2. Clean up any temporary code
3. Final commit
4. Report results

## Refactor Plan Template

```markdown
# Refactor Plan: [Target]

## Objective
[What improvement is being made]

## Target Files
- [File 1]
- [File 2]

## Test Baseline
- Tests passing: [count]/[total]
- Coverage: [percentage]

## Changes Planned

### Change 1: [Name]
- **File**: [path]
- **Description**: [what change]
- **Risk**: Low/Medium/High
- **Depends on**: [previous change ID or "none"]

### Change 2: [Name]
- **File**: [path]
- **Description**: [what change]
- **Risk**: Low/Medium/High
- **Depends on**: Change 1

## Rollback Points
- [Commit ID]: [description of what was complete]

## Verification Steps
1. [Verification step 1]
2. [Verification step 2]

## Expected Outcome
[What the code will look like after]

## Status
DRAFT | TESTING | IN_PROGRESS | VERIFYING | COMPLETE
```

## Common Refactoring Patterns

### Extract Function
```python
# Before
def process_order(order):
    # 50 lines of mixed logic
    
# After
def process_order(order):
    validate_order(order)
    calculate_totals(order)
    save_order(order)
```

### Extract Class
```python
# Before
class User:
    # authentication methods
    # profile methods
    # notification methods
    
# After
class User:
    # profile methods only
    
class UserAuth:
    # authentication methods
    
class UserNotifications:
    # notification methods
```

### Rename for Clarity
```python
# Before
def calc(x, y):
    return x * y + 10

# After
def calculate_adjusted_price(base_price, quantity):
    return base_price * quantity + SERVICE_FEE
```

### Reduce Duplication
```python
# Before
def validate_email(email):
    if not email or '@' not in email:
        return False
    return True
    
def validate_phone(phone):
    if not phone or len(phone) < 10:
        return False
    return True

# After
def validate_required(value, rules):
    if not value:
        return False
    for rule in rules:
        if not rule(value):
            return False
    return True
```

## Risk Levels

| Risk | Description | Approach |
|------|-------------|----------|
| Low | Localized, simple change | Single commit |
| Medium | Multiple files, same patterns | Small commits, frequent tests |
| High | Complex changes, many files | Very small steps, checkpoints |

## Anti-Patterns to Avoid

- **Big Bang Refactor**: Changing everything at once
- **Refactor Without Tests**: No safety net
- **Mixed Refactor + Feature**: Changing behavior during refactor
- **Skip Verification**: Not running tests after each change

## Usage

```
/refactor [target] [objective]
```

Example:
```
/refactor src/backend/services/user_service.py extract authentication logic
```

## Coordination

- Domain-specific refactors: Domain lead approval
- Cross-domain refactors: architect-lead approval
- Breaking internal APIs: Both leads must approve
- Database schema refactor: backend-lead + database-dev