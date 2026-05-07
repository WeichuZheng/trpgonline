# Multi-Agent Architecture

> A GAN-inspired approach to AI-assisted software development: Planner, Generator, and Evaluator work together to produce high-quality output through separation of concerns and adversarial evaluation.

---

## Overview

### The Core Pattern

```
+-------------+     +-------------+     +-------------+
|   Planner   | --> |  Generator  | --> |  Evaluator  |
|  (Plans)    |     | (Implements)|     |  (Grades)   |
+-------------+     +-------------+     +-------------+
      ^                                        |
      |                                        v
      +----------------------------------------+
                    Feedback Loop
```

This architecture is inspired by Generative Adversarial Networks (GANs). Just as GANs use a generator and discriminator to improve output quality, our multi-agent system uses separate agents with opposing objectives:

- **Planner**: Expands brief prompts into comprehensive specifications
- **Generator**: Implements features according to specifications
- **Evaluator**: Objectively grades implementation against criteria

### Why Separation Matters

Models cannot reliably evaluate their own work. When a single agent both builds and reviews, it:

- Praises mediocre output as "complete"
- Skips edge cases and error handling
- Misses integration issues
- Accepts incomplete solutions
- Rationalizes shortcuts

**The solution**: Never let the same agent generate and evaluate. By separating these roles, we enable objective quality assessment.

---

## Agent Roles

### Planner Agent

**Purpose**: Transform brief user prompts into comprehensive product specifications.

**When to Use**:
- User provides a brief (1-4 sentence) prompt
- Product context is unclear or incomplete
- Feature scope needs definition
- Technical approach needs high-level design
- AI integration opportunities should be identified

**What It Does**:
1. Takes minimal user input
2. Expands into full product specification
3. Focuses on WHAT, not HOW
4. Identifies AI feature opportunities
5. Avoids over-specifying implementation (prevents cascade errors)

**What It Does NOT Do**:
- Write implementation code
- Specify exact algorithms
- Make low-level technical decisions
- Execute on the plan

**Key Principle**: Stay ambitious about scope, but focused on product intent.

### Generator Agent

**Purpose**: Implement features one sprint at a time according to specifications.

**When to Use**:
- Clear specification exists
- Sprint contract is approved
- Implementation work is needed
- Incremental progress is required

**What It Does**:
1. Reads specifications and sprint contracts
2. Negotiates "done" criteria with Evaluator
3. Implements features incrementally
4. Self-evaluates at end of each sprint
5. Uses git for version control
6. Documents decisions

**What It Does NOT Do**:
- Evaluate its own work (that's Evaluator's job)
- Change scope without negotiation
- Skip the contract phase
- Approve its own implementation

**Key Principle**: One feature at a time, contract before code.

### Evaluator Agent

**Purpose**: Objectively grade work against established criteria.

**When to Use**:
- Implementation is complete
- Sprint needs evaluation
- Contract criteria need verification
- Quality gate is required

**What It Does**:
1. Reads sprint contract
2. Tests implementation against criteria
3. Grades each criterion (PASS/FAIL with score)
4. Provides specific, actionable feedback
5. Finds edge cases, not just happy paths

**What It Does NOT Do**:
- Implement features
- Sympathize with Generator's constraints
- Accept "good enough" without evidence
- Make excuses for failures

**Critical Mindset**: You did NOT build this feature. Your job is to find issues, not justify shortcuts.

**Key Principle**: Be skeptical, not generous.

---

## Sprint Contract Flow

### The Contract Lifecycle

```
1. PROPOSE     Generator reads spec, proposes contract
      |
      v
2. REVIEW      Evaluator tests each criterion for:
      |         - Testability (Can I verify this?)
      |         - Completeness (Does it cover the feature?)
      |         - Unambiguity (No room for interpretation?)
      |
      v
3. NEGOTIATE   Back-and-forth until agreement
      |
      v
4. APPROVE     Both parties sign off
      |
      v
5. IMPLEMENT   Generator builds to contract
      |
      v
6. EVALUATE    Evaluator grades against contract
      |
      v
7. ITERATE     If FAIL: fix issues, re-evaluate
   or MERGE    If PASS: proceed to next sprint
```

### Why Contract First?

Without a contract:
- Scope creeps during implementation
- "Done" keeps moving
- Evaluator has moving targets
- Generator feels unfairly judged
- Time wasted on misunderstandings

With a contract:
- Clear boundaries before starting
- Objective success criteria
- Fair evaluation standards
- Efficient iteration cycles

### Contract Components

```markdown
# Sprint Contract

## Scope
- What: Feature description
- In Scope: Specific items included
- Out of Scope: Specific items excluded
- Dependencies: Required prerequisites

## Testable Behaviors
### [Category]
- [ ] B1.1: [Specific, verifiable behavior]
- [ ] B1.2: [Specific, verifiable behavior]

## Acceptance Criteria
| ID | Criterion | Pass Condition | Fail Condition | Priority |
|----|-----------|----------------|----------------|----------|
| AC1 | [Name] | [What passes] | [What fails] | P1/P2/P3 |

## Negotiation Log
| Round | Party | Action | Notes |
|-------|-------|--------|-------|
| 1 | Generator | PROPOSED | Initial proposal |
| 1 | Evaluator | REVIEWED | Feedback |
```

---

## Evaluation Criteria System

### Priority Levels

| Priority | Meaning | Failure Impact |
|----------|---------|----------------|
| **P1** | Must pass | Blocks sprint completion |
| **P2** | Should pass | Minor issues acceptable with documented reason |
| **P3** | Nice to have | Failure acceptable |

### Criterion Format

Each criterion must have:
1. **ID**: Unique identifier (e.g., AC1, B2.3)
2. **Name**: Descriptive title
3. **Pass Condition**: Specific, observable state
4. **Fail Condition**: What constitutes failure
5. **Priority**: P1, P2, or P3

### Good vs Bad Criteria

**Good Criteria** (Use these):
- "User can complete signup in under 3 clicks with no errors"
- "API returns 404 for non-existent resources"
- "Form validation shows specific error messages within 100ms"
- "Button hover state has 150ms transition"
- "Error logs include stack trace and timestamp"

**Bad Criteria** (Avoid these):
- "Good UX" (too vague - not testable)
- "Fast performance" (not measurable - what's fast?)
- "Works correctly" (circular definition)
- "User-friendly interface" (subjective)
- "Proper error handling" (what's proper?)

### The Testability Test

Before approving any criterion, ask:
1. Can I observe this in under 5 minutes?
2. Would two different evaluators reach the same conclusion?
3. Is there a clear YES/NO boundary?
4. Can I write a test for this?

If any answer is NO, rewrite the criterion.

---

## Context Reset Protocol

### The Problem

Long-running tasks suffer from context pollution:
- Earlier instructions get forgotten
- New information conflicts with old
- Agent drifts from original goals
- Quality degrades over time

### The Solution: Handoff Artifacts

```
+----------+     Handoff Artifact     +----------+
| Session  |  ---------------------> | Session  |
|    A     |                          |    B     |
+----------+                          +----------+
```

A handoff artifact contains everything the next session needs:

```markdown
# Handoff Document

## Current State
- What's been completed
- What's in progress
- What's blocked

## Context
- Original requirements
- Decisions made and why
- Constraints discovered

## Next Steps
- Immediate actions needed
- Dependencies to resolve
- Risks to address

## Files Changed
- List of modified files
- Key changes in each
```

### When to Reset Context

Reset context when:
1. Switching between Planner, Generator, Evaluator roles
2. Session exceeds 2 hours of active work
3. Context window is 50%+ full
4. Task fundamentally changes phase

### How to Reset

1. **Before Reset**: Write handoff artifact to `session-state/handoff.md`
2. **After Reset**: Read handoff artifact first
3. **Verify**: Confirm understanding of state before continuing

---

## Complete Workflow Example

### Scenario: Adding User Authentication

#### Step 1: Planner Phase

**User Input**: "Add user authentication to the app"

**Planner Output**:
- Feature spec with login, signup, password reset
- OAuth integration opportunities (Google, GitHub)
- Session management approach
- Security requirements (token refresh, expiration)

#### Step 2: Generator Negotiates Contract

**Generator Proposes**:
```
Sprint Contract: User Login

Scope: Email/password login only (OAuth in future sprint)
Testable Behaviors:
- B1.1: User can log in with valid email and password
- B1.2: Invalid password shows "Invalid credentials" error
- B1.3: Login completes within 2 seconds
- B1.4: Session persists for 7 days
```

#### Step 3: Evaluator Reviews

**Evaluator Feedback**:
> "B1.3 is vague - does this include network latency? What's the baseline?
> B1.4 - where is session stored? localStorage? httpOnly cookie?
> Missing: rate limiting, CSRF protection"

**Generator Revises**:
```
- B1.3: Login API responds in under 500ms (server-side)
- B1.5: Failed login attempts rate-limited to 5 per minute
- B1.6: Session stored in httpOnly cookie with SameSite=Strict
```

**Evaluator Approves**

#### Step 4: Generator Implements

Generator builds the feature, documenting decisions in code comments.

#### Step 5: Evaluator Evaluates

```
Evaluation Report: User Login

B1.1: PASS - Logged in successfully with test@example.com
B1.2: PASS - Error message displayed correctly
B1.3: PASS - API response time: 312ms (avg), 489ms (max)
B1.4: FAIL - Session expires after 24h, not 7 days
B1.5: PASS - Rate limiting works (tested with 10 rapid attempts)
B1.6: PASS - Cookie attributes verified in browser dev tools

Verdict: FAIL (B1.4 is P1 blocker)

Action Items:
- Fix session expiration to 7 days
- Re-submit for evaluation
```

#### Step 6: Generator Fixes and Re-submits

Generator fixes session expiration, updates code, signals re-evaluation.

#### Step 7: Evaluator Re-evaluates

```
B1.4: PASS - Session now persists for 7 days (tested with time manipulation)

Verdict: PASS
```

---

## Best Practices

### For Planner

1. **Think Product, Not Implementation**
   - Describe what users experience
   - Leave HOW to Generator
   - Avoid over-specifying technical details

2. **Be Ambitious but Realistic**
   - Include AI integration opportunities
   - Consider edge cases from user perspective
   - Don't artificially limit scope

3. **Set Clear Boundaries**
   - What's in scope for this feature
   - What's explicitly out of scope
   - What's undefined (needs decision)

### For Generator

1. **Contract Before Code**
   - Never start implementation without approved contract
   - Negotiate until both parties agree
   - Document all decisions

2. **One Feature at a Time**
   - Don't expand scope mid-sprint
   - Save interesting tangents for future sprints
   - Focus on contract completion

3. **Self-Evaluate First**
   - Run through criteria yourself
   - Fix obvious issues before handoff
   - Document why each criterion passes

### For Evaluator

1. **Be Skeptical**
   - Assume Generator missed something
   - Test edge cases, not happy paths
   - Verify implementation, not claims

2. **Be Specific**
   - "Login fails" is not actionable
   - "Login button returns 500 error when password contains '<' character" is actionable
   - Include reproduction steps

3. **Be Fair**
   - Judge against contract only
   - Don't add requirements mid-evaluation
   - Acknowledge when criteria pass

### For All Agents

1. **Document Everything**
   - Decisions and rationale
   - Edge cases discovered
   - Why certain approaches were rejected

2. **Respect Boundaries**
   - Planner doesn't implement
   - Generator doesn't evaluate
   - Evaluator doesn't implement

3. **Communicate in Artifacts**
   - Use sprint contracts for negotiation
   - Use evaluation reports for feedback
   - Use handoff documents for context

---

## Anti-Patterns to Avoid

### 1. Self-Evaluation

**Wrong**: Generator evaluates its own work
```
Generator: "I implemented login, looks good to me!"
```

**Right**: Separate Generator and Evaluator
```
Generator: "I implemented login, ready for evaluation."
Evaluator: "I found 3 issues with the login implementation..."
```

### 2. Vague Criteria

**Wrong**: "Good UX"
```
Evaluator: "I think the UX is good." (Subjective!)
```

**Right**: "Login completes in under 3 clicks"
```
Evaluator: "Login required 2 clicks. PASS." (Objective!)
```

### 3. Scope Creep

**Wrong**: Adding requirements mid-sprint
```
Generator: "I added password reset too since it's related."
```

**Right**: Stick to contract, expand in next sprint
```
Generator: "Password reset is out of scope for this sprint.
I'll add it to the backlog for sprint 2."
```

### 4. Generous Evaluation

**Wrong**: Accepting "good enough"
```
Evaluator: "The login works, I guess. PASS."
```

**Right**: Skeptical evaluation
```
Evaluator: "Login works on Chrome but fails on Safari.
The contract says 'all modern browsers'. FAIL."
```

### 5. Context Accumulation

**Wrong**: Never resetting context
```
Session grows to 100k+ tokens, quality degrades...
```

**Right**: Regular context resets with handoffs
```
Session A: Planner -> writes spec -> handoff
Session B: Generator -> reads handoff -> implements -> handoff
Session C: Evaluator -> reads handoff -> evaluates
```

---

## Summary

The multi-agent architecture works because:

1. **Separation of Concerns**: Each agent has a distinct role
2. **Adversarial Evaluation**: Evaluator actively seeks problems
3. **Contract-First**: Clear criteria before implementation
4. **Context Management**: Handoff artifacts prevent drift
5. **Iterative Quality**: FAIL -> FIX -> PASS cycle

When followed correctly, this produces:
- Higher quality code
- Fewer bugs in production
- Clearer requirements
- Fairer evaluation
- Better documentation

The key insight: **Models cannot evaluate their own work objectively.** By separating generation and evaluation, we achieve quality that neither agent could produce alone.