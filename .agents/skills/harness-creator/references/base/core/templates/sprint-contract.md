# Sprint Contract: [Feature Name]

> Contract Version: 2.0 (Fusion Architecture)
> Created: [DATE]
> Status: DRAFT | PENDING_REVIEW | APPROVED | IN_PROGRESS | COMPLETED

---

## Scope

### What
[2-3 sentence description of what this sprint delivers]

### In Scope
- [Specific item 1]
- [Specific item 2]
- [Specific item 3]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

### Dependencies
- [Required dependency 1]
- [Required dependency 2]

---

## Architecture Decision

### architect-lead: [Name or "TBD"]

### Specialists Involved

| Specialist | Tasks | Domain Scope |
|------------|-------|--------------|
| [name]-dev | [specific tasks] | [directories] |
| [name]-dev | [specific tasks] | [directories] |

### Cross-Domain Boundaries

| Boundary | Definition |
|----------|------------|
| Interface: [Name] | [Who defines, who implements] |
| Event: [Name] | [Who emits, who handles] |
| Data: [Name] | [Who owns, who reads] |

### Integration Points

- [Integration point 1]: [Description]
- [Integration point 2]: [Description]

---

## Testable Behaviors

### [Category 1: e.g., Core Functionality]
- [ ] **B1.1**: [Specific behavior] | Owner: [specialist-name]
- [ ] **B1.2**: [Specific behavior] | Owner: [specialist-name]
- [ ] **B1.3**: [Specific behavior] | Owner: [specialist-name]

### [Category 2: e.g., Error Handling]
- [ ] **B2.1**: [Specific behavior] | Owner: [specialist-name]
- [ ] **B2.2**: [Specific behavior] | Owner: [specialist-name]

### [Category 3: e.g., Edge Cases]
- [ ] **B3.1**: [Specific behavior] | Owner: [specialist-name]
- [ ] **B3.2**: [Specific behavior] | Owner: [specialist-name]

---

## Acceptance Criteria

| ID | Criterion | Pass Condition | Fail Condition | Priority | Owner |
|----|-----------|----------------|----------------|----------|-------|
| AC1 | [Name] | [What passes] | [What fails] | P1 | [specialist] |
| AC2 | [Name] | [What passes] | [What fails] | P1 | [specialist] |
| AC3 | [Name] | [What passes] | [What fails] | P2 | [specialist] |

### Priority Definitions
- **P1**: Must pass - blocks sprint completion
- **P2**: Should pass - minor issues acceptable with documented reason
- **P3**: Nice to have - failure acceptable

---

## Responsibility Matrix

| Criterion | Responsible Specialist | Fallback |
|-----------|----------------------|----------|
| B1.1 | [specialist-name] | Generator |
| B1.2 | [specialist-name] | Generator |
| B2.1 | [specialist-name] | Generator |

---

## Technical Approach

### Implementation Notes
[Optional: High-level technical direction without over-specifying]

### Files to Create/Modify
- [ ] [File path 1] | Owner: [specialist]
- [ ] [File path 2] | Owner: [specialist]

### Tests Required
- [ ] [Test type and coverage] | Owner: [specialist]
- [ ] [Edge cases to test] | Owner: [specialist]

---

## Negotiation Log

| Round | Party | Action | Notes | Timestamp |
|-------|-------|--------|-------|-----------|
| 1 | Generator | PROPOSED | Initial contract proposal | [TIME] |
| 1 | architect-lead | REVIEWED | Architecture feedback | [TIME] |
| 1 | Evaluator | REVIEWED | Testability feedback | [TIME] |
| 2 | Generator | REVISED | Changes made | [TIME] |
| 2 | All | APPROVED | Contract approved | [TIME] |

---

## Sign-off

### Generator Approval
- [ ] I confirm this contract accurately represents what I will build
- [ ] I understand the acceptance criteria and testable behaviors
- [ ] I commit to implementing exactly what is specified
- [ ] I will coordinate the specialists identified above

**Generator Signature**: `___________________` **Date**: `___________`

### architect-lead Approval
- [ ] I confirm the architecture decisions are sound
- [ ] I confirm domain boundaries are clearly defined
- [ ] I confirm specialist assignments are appropriate

**architect-lead Signature**: `___________________` **Date**: `___________`

### Evaluator Approval
- [ ] I confirm all criteria are testable and unambiguous
- [ ] I understand how I will verify each criterion
- [ ] I commit to objective evaluation against these criteria only

**Evaluator Signature**: `___________________` **Date**: `___________`

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [Author] | Initial version |

---

## Implementation Progress

> Update this section during implementation

| Criterion | Status | Notes | Specialist |
|-----------|--------|-------|------------|
| B1.1 | NOT_STARTED | | [name] |
| B1.2 | NOT_STARTED | | [name] |

---

## Evaluation Reference

> After implementation, link to the evaluation report here

**Evaluation Report**: [Link to evaluation-report.md]

**Verdict**: PENDING | PASS | FAIL

**Action Items**: [To be filled after evaluation]