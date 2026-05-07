---
name: checkpoint
description: "Save current progress with structured handoff artifact. Enables context reset for long-running tasks and session recovery."
user-invocable: true
argument-hint: "[checkpoint-name]"
allowed-tools: Read, Glob, Grep, Write, Bash
---

# /checkpoint - Save Progress

Save current session progress for recovery and context reset.

## Usage

```
/checkpoint [name]
```

- **With name**: Save as named checkpoint
- **Without name**: Save as timestamped checkpoint

## What Gets Saved

### Handoff Artifact (Context Reset)

Located at: `production/session-state/handoffs/handoff-TIMESTAMP.md`

```markdown
# Session Handoff Artifact

## Session Summary
[What was being built]

## Completed Work
- [x] Task 1
- [x] Task 2

## Current State
[Where we stopped]

## Next Immediate Step
[What to do next - specific and actionable]

## Key Decisions
- Decision 1: [choice and reason]
- Decision 2: [choice and reason]

## Open Questions
- Question 1
- Question 2

## Commands to Resume
1. Read handoff artifact
2. Run specific command
```

### Checkpoint File

Located at: `production/session-state/checkpoints/checkpoint-TIMESTAMP.md`

Lightweight snapshot for quick recovery.

## When to Use

- **Before context limit**: Proactively save before compaction
- **After major milestone**: Document completed work
- **Switching contexts**: Save current work to switch tasks
- **End of session**: Log accomplishments for next session

## Reference

Base implementation: `@references/base/progress/skills/checkpoint/SKILL.md`