---
name: sprint-contract
description: "Negotiates 'done' criteria between Generator, Evaluator, and architect-lead before implementation begins. Converts subjective goals into testable, gradable criteria with clear domain responsibilities."
user-invocable: true
---

# Sprint Contract Skill

You are facilitating the Sprint Contract negotiation process. Your role is to guide the Generator, Evaluator, and architect-lead to agree on what "done" means before any implementation begins.

## Purpose

A Sprint Contract prevents:
- Ambiguous success criteria
- Moving goalposts during development
- Self-evaluation bias (Generator grading their own work)
- Unclear domain responsibilities

## Contract Flow

```
Generator proposes contract -> architect-lead reviews architecture -> Evaluator reviews testability -> Negotiation -> Agreement -> Implementation -> Evaluation
```

## Negotiation Workflow

### Phase 1: Contract Proposal (Generator)

1. Read the product spec or feature requirements
2. Identify the scope for this sprint (one feature at a time)
3. **Identify domain specialists needed**
4. Propose a contract with:
   - Clear scope boundaries
   - Testable behaviors (user-facing, verifiable)
   - Acceptance criteria (pass/fail conditions)
   - **Architecture decision section**
   - **Specialist assignments**
   - **Responsibility matrix**
5. Write proposal to `sprint-contract.md`

### Phase 2: Architecture Review (architect-lead)

1. Read the proposed contract
2. Evaluate architecture decisions:
   - Are domain boundaries correct?
   - Are cross-domain interfaces defined?
   - Is the specialist assignment appropriate?
3. Write feedback with specific concerns
4. Either: APPROVE_ARCHITECTURE, REQUEST_CHANGES, or REJECT with rationale

### Phase 3: Contract Review (Evaluator)

1. Read the proposed contract
2. Evaluate each criterion:
   - Is it testable? (Can I verify this objectively?)
   - Is it complete? (Does it cover the feature?)
   - Is it unambiguous? (No room for interpretation)
3. Write feedback with specific concerns
4. Either: APPROVE_TESTABILITY, REQUEST_CHANGES, or REJECT with rationale

### Phase 4: Negotiation Loop

1. If REQUEST_CHANGES: Generator revises contract
2. architect-lead re-reviews architecture
3. Evaluator re-reviews testability
4. Repeat until both APPROVE
5. Record all negotiation points in the contract log

### Phase 5: Implementation

Once approved:
1. Generator implements against the contract
2. **Generator delegates to specialists as defined in contract**
3. No scope changes without re-negotiation
4. Document any discoveries that affect criteria

### Phase 6: Evaluation

1. Evaluator tests each criterion
2. Grade: PASS/FAIL with evidence
3. Generate evaluation report
4. If FAIL: Specific action items for iteration

## Contract Template Structure

```markdown
# Sprint Contract: [Feature Name]

## Scope
- What: [Feature description]
- In Scope: [Specific items included]
- Out of Scope: [Specific items excluded]

## Architecture Decision (NEW in v2.0)
- architect-lead: [Name]
- Specialists Involved: [Table of specialists, tasks, domain scope]
- Cross-Domain Boundaries: [Interface and event definitions]

## Testable Behaviors
### [Category]
- [ ] B1.1: [Description] | Owner: [specialist]

## Acceptance Criteria
| ID | Criterion | Pass Condition | Fail Condition | Priority | Owner |
|----|-----------|----------------|----------------|----------|-------|

## Responsibility Matrix (NEW in v2.0)
| Criterion | Responsible | Fallback |
|-----------|-------------|----------|

## Negotiation Log
| Round | Party | Action | Notes |
|-------|-------|--------|-------|
```

## Three-Party Interaction Protocol

### Generator Responsibilities
- Propose realistic, achievable criteria
- Be specific about what will be built
- **Identify required specialists upfront**
- Accept feedback constructively
- Revise based on reviewer concerns
- Do not inflate scope during implementation

### architect-lead Responsibilities (NEW in v2.0)
- Review domain boundaries
- Validate cross-domain interfaces
- Ensure specialist assignments are appropriate
- Identify architectural risks
- Approve architecture decisions

### Evaluator Responsibilities
- Be skeptical, not generous
- Identify missing test coverage
- Ensure criteria are objectively verifiable
- Find edge cases, not just happy paths
- Do not approve ambiguous criteria

### Communication Rules
1. All negotiation happens in the contract file
2. Each party signs off with their agent name
3. No implementation until all three parties approve
4. Contract changes require re-approval from all parties

## Good vs Bad Criteria

### Good Criteria (Use These)
- "User can complete signup in under 3 clicks with no errors"
- "API returns 404 for non-existent resources"
- "Form validation shows specific error messages within 100ms"
- "Button hover state has 150ms transition"

### Bad Criteria (Avoid These)
- "Good UX" (too vague)
- "Fast performance" (not measurable)
- "Works correctly" (circular definition)
- "User-friendly interface" (subjective)

## Running This Skill

When invoked, this skill will:

1. **If no contract exists**: Guide Generator to propose a new contract
2. **If contract pending architecture review**: Prompt architect-lead to review
3. **If contract pending testability review**: Prompt Evaluator to review
4. **If negotiation in progress**: Continue the negotiation loop
5. **If contract approved**: Signal readiness for implementation

## Usage

```
/sprint-contract [feature-name]
```

Or automatically invoked when Generator begins work on a new feature.