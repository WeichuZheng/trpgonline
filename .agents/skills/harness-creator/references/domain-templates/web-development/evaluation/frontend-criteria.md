# Frontend Evaluation Criteria

> Objective, testable criteria for evaluating frontend implementation quality.

---

## Criterion Categories

### 1. Component Quality
### 2. State Management
### 3. Styling & Design System
### 4. Accessibility
### 5. Performance
### 6. Testing
### 7. Integration

---

## Component Quality Criteria

### FQ1: Component Structure
| Field | Value |
|-------|-------|
| **ID** | FQ1 |
| **Name** | Component Structure Quality |
| **Description** | Component follows established structure patterns with clear separation of concerns |
| **Category** | Quality |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Component file under 200 lines, single responsibility, clear props interface.

**Fail Condition**: File > 300 lines, multiple responsibilities, unclear prop types.

**Test Conditions**:
- Happy Path: Well-structured component with TypeScript types
- Edge Cases: Large component needing extraction
- Error Cases: Component with mixed concerns

---

### FQ2: Prop Validation
| Field | Value |
|-------|-------|
| **ID** | FQ2 |
| **Name** | Prop Type Validation |
| **Description** | All component props are properly typed with TypeScript or PropTypes |
| **Category** | Quality |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: All props have explicit types, optional props marked, defaults provided where needed.

**Fail Condition**: Missing prop types, implicit types, runtime errors from wrong types.

---

### FQ3: Error Handling
| Field | Value |
|-------|-------|
| **ID** | FQ3 |
| **Name** | Component Error Handling |
| **Description** | Component handles error states gracefully |
| **Category** | Quality |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 6/10 |

**Pass Condition**: Error state UI exists, fallback rendering works, no uncaught exceptions.

**Fail Condition**: Missing error states, crashes on error, blank screen on failure.

---

## State Management Criteria

### SM1: State Location
| Field | Value |
|-------|-------|
| **ID** | SM1 |
| **Name** | State Management Location |
| **Description** | State is managed in appropriate location (local vs global) |
| **Category** | Architecture |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Local state for UI-only, global state for shared data, clear data flow.

**Fail Condition**: Global state for local concerns, duplicated state, unclear ownership.

---

### SM2: State Updates
| Field | Value |
|-------|-------|
| **ID** | SM2 |
| **Name** | State Update Patterns |
| **Description** | State updates follow established patterns, no direct mutations |
| **Category** | Quality |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Immutable updates, hooks/state library used correctly, no race conditions.

**Fail Condition**: Direct mutations, inconsistent patterns, state race conditions.

---

## Styling Criteria

### ST1: Design System Compliance
| Field | Value |
|-------|-------|
| **ID** | ST1 |
| **Name** | Design System Compliance |
| **Description** | Styles use design system tokens, no inline styles |
| **Category** | Standards |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Uses design tokens, existing components reused, no ad-hoc styles.

**Fail Condition**: Inline styles, hardcoded colors/sizes, custom styles for existing patterns.

---

### ST2: Responsive Design
| Field | Value |
|-------|-------|
| **ID** | ST2 |
| **Name** | Responsive Design Implementation |
| **Description** | Component works on all screen sizes |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Works on mobile, tablet, desktop, no horizontal scroll, proper breakpoints.

**Fail Condition**: Broken on mobile, horizontal scroll, missing breakpoints.

---

## Accessibility Criteria

### AC1: ARIA Attributes
| Field | Value |
|-------|-------|
| **ID** | AC1 |
| **Name** | ARIA Accessibility |
| **Description** | Component has proper ARIA attributes for screen readers |
| **Category** | Accessibility |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Roles, labels, descriptions where needed, screen reader testable.

**Fail Condition**: Missing ARIA, unlabeled buttons, unreadable content.

---

### AC2: Keyboard Navigation
| Field | Value |
|-------|-------|
| **ID** | AC2 |
| **Name** | Keyboard Navigation |
| **Description** | Component is fully keyboard accessible |
| **Category** | Accessibility |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: All actions keyboard accessible, focus management works, tab order logical.

**Fail Condition**: Mouse-only actions, focus trapped, illogical tab order.

---

## Performance Criteria

### PF1: Bundle Size
| Field | Value |
|-------|-------|
| **ID** | PF1 |
| **Name** | Component Bundle Impact |
| **Description** | Component doesn't significantly increase bundle size |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: No new large dependencies, lazy loading for heavy components, code splitting.

**Fail Condition**: Large dependencies added, no lazy loading, bundle size > 50KB increase.

---

### PF2: Render Performance
| Field | Value |
|-------|-------|
| **ID** | PF2 |
| **Name** | Render Performance |
| **Description** | Component renders efficiently without unnecessary re-renders |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Memoization where needed, efficient re-renders, < 16ms render time.

**Fail Condition**: Excessive re-renders, missing memoization, > 100ms render time.

---

## Testing Criteria

### TC1: Unit Test Coverage
| Field | Value |
|-------|-------|
| **ID** | TC1 |
| **Name** | Unit Test Coverage |
| **Description** | Component has adequate unit test coverage |
| **Category** | Testing |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: > 70% coverage, critical paths tested, edge cases covered.

**Fail Condition**: < 50% coverage, untested critical paths, missing edge cases.

---

### TC2: Test Quality
| Field | Value |
|-------|-------|
| **ID** | TC2 |
| **Name** | Test Quality |
| **Description** | Tests are meaningful and not just coverage |
| **Category** | Testing |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Tests verify behavior, not implementation, assertions meaningful.

**Fail Condition**: Empty tests, tests pass when broken, implementation-dependent tests.

---

## Integration Criteria

### IN1: API Integration
| Field | Value |
|-------|-------|
| **ID** | IN1 |
| **Name** | API Integration Quality |
| **Description** | API calls follow established patterns |
| **Category** | Integration |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Uses hooks/services for API calls, loading states, error handling.

**Fail Condition**: Direct fetch in components, missing loading states, unhandled errors.

---

### IN2: Loading States
| Field | Value |
|-------|-------|
| **ID** | IN2 |
| **Name** | Loading State Handling |
| **Description** | Component shows loading state during async operations |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Loading indicator shows, content hidden during load, smooth transition.

**Fail Condition**: No loading indicator, content jumps, blank during load.

---

## Grading Guide

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceptional quality, exceeds requirements |
| 9/10 | Excellent | Fully meets all criteria, minor polish possible |
| 8/10 | Very Good | Meets criteria, small edge case issues |
| 7/10 | Good | Meets criteria well, some minor issues |
| 6/10 | Acceptable | Meets basic criteria, notable gaps |
| 5/10 | Marginal | Partially meets criteria, significant work needed |
| 4/10 | Below Standard | Fails some aspects, rework needed |
| 3/10 | Poor | Major issues, substantial rework |
| 2/10 | Very Poor | Critical failures, mostly broken |
| 1/10 | Fail | Does not meet criteria |
| 0/10 | No Attempt | Criterion not addressed |

---

## Priority Definitions

- **P1**: Must pass - blocks release
- **P2**: Should pass - minor issues acceptable with documentation
- **P3**: Nice to have - failure acceptable