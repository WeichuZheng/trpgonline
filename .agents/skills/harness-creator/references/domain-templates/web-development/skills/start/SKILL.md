---
name: start
description: "Smart session onboarding for web development projects. Checks for saved progress (handoff/checkpoint) and offers to continue or start fresh with sprint contract integration."
user-invocable: true
argument-hint: ""
allowed-tools: Read, Glob, Grep, Write, Bash
---

# /start - Session Onboarding

Smart onboarding for web development projects with progress memory.

## Flow

```
Session start
    │
    ├─ Handoff artifact exists? → Load and continue
    │
    ├─ Checkpoint exists? → Offer to resume
    │
    └─ Fresh start → Sprint contract flow
```

## Usage

```
/start
```

## Behavior

### 1. Check for Saved Progress

Look for:
- `production/session-state/handoffs/latest.md` (Context Reset handoff)
- `production/session-state/checkpoints/` (Manual checkpoints)

### 2. If Progress Found

```
📦 Found saved progress from [date]

Session: [feature name]
Last state: [where we stopped]
Next step: [what to do next]

Continue previous work?
  A) Yes, resume from checkpoint
  B) No, start fresh
```

### 3. Fresh Start Options

```
What would you like to do?
  A) New feature (0→1) - Start with brainstorm
  B) Continue existing work (1→N) - Onboard codebase first
  C) Emergency hotfix - Skip to hotfix workflow
```

## Sprint Contract Integration

For new features, /start integrates with the sprint contract system:

1. **Planner Phase**: Expand user prompt into spec
2. **Contract Negotiation**: Agree on "done" criteria
3. **Implementation Ready**: Clear starting point

## Reference

Base implementation: `@references/base/progress/skills/start/SKILL.md`