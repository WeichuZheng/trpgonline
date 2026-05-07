# Phase 2: Vision

Define project purpose and goals for new (0→1) projects.

## Purpose

Understand what you're building and why before discussing technical details.

## When This Phase Runs

- New project (empty directory)
- User selected "create new project from scratch"
- Skip if existing project with clear detection

## Vision Questions

### 1. Project Identity

```
What are you building? (one sentence)
```

Follow-up if vague:
```
Let me clarify - is this more like:
A) A web application (frontend + backend)
B) A CLI tool
C) A library/package
D) A service/API
E) Something else [describe]
```

### 2. Problem Statement

```
What problem does this solve?
```

Helps shape:
- Architecture decisions
- Feature priorities
- Evaluation criteria

### 3. Target Users

```
Who will use this?
```

Options:
- End users (B2C)
- Businesses (B2B)
- Developers (internal tooling)
- Yourself (personal project)

### 4. Success Criteria

```
How will you know when it's "done" for v1?
```

Gather 3-5 measurable outcomes:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

These become **evaluation criteria** for the Evaluator agent.

### 5. Timeline & Scope

```
What's your timeline expectation?
```

| Timeline | Scope Recommendation |
|----------|---------------------|
| < 1 week | MVP, minimal harness |
| 1-4 weeks | Standard harness |
| 1-3 months | Full harness + CI/CD |
| Ongoing | Full harness + monitoring |

## Decision Flow

```
Vision Questions
       │
       ├─ Web app? → Ask about frontend/backend split
       │
       ├─ API only? → Focus on backend skills
       │
       ├─ CLI? → Focus on testing skills
       │
       └─ Library? → Focus on docs + testing
```

## Context Reset Protocol

Since this is a multi-phase brainstorm, summarize before handoff:

```markdown
## Vision Summary

**Project:** [name]
**Purpose:** [one-liner]
**Users:** [target]
**Success Criteria:**
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]
**Timeline:** [expectation]
```

Show to user:
```
Here's what I understood:
[summary]

Is this accurate? Should I proceed to tech stack?
```

## Output to Next Phase

```yaml
vision:
  name: [project-name]
  type: [web-app|api|cli|library|other]
  purpose: [one-sentence description]
  target_users: [b2c|b2b|developers|personal]
  success_criteria:
    - [criterion 1]
    - [criterion 2]
    - [criterion 3]
  timeline: [duration]
  scope: [minimal|standard|full]
```

## Skip Conditions

This phase is **skipped** when:
- Existing project detected (Phase 1 → Phase 5)
- User explicitly wants quick setup
- Project type already clear from context

## Sprint Contract Checkpoint

```
Before we discuss tech stack, let me confirm:
- You're building: [project type]
- For: [users]
- Success means: [criteria]

Proceed to tech selection? [Yes/Back]
```