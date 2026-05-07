---
name: resume
description: "Load previous checkpoint or handoff artifact to continue work. Prefers handoff (context reset) over checkpoint for better context recovery."
user-invocable: true
argument-hint: "[checkpoint-name|latest]"
allowed-tools: Read, Glob, Grep, Write, Bash
---

# /resume - Load Progress

Load saved progress from checkpoint or handoff artifact.

## Usage

```
/resume              # Load latest handoff/checkpoint
/resume [name]       # Load specific checkpoint
/resume latest       # Explicitly load latest
```

## Priority Order

1. **Handoff artifact** (preferred) - Full context reset document
2. **Checkpoint** (fallback) - Lightweight snapshot

## Behavior

### 1. List Available Progress

```
📦 Available progress:

Handoffs:
  - handoff-2026-04-04-1430.md (latest)
  - handoff-2026-04-03-0900.md

Checkpoints:
  - checkpoint-feature-auth.md
  - checkpoint-2026-04-04-1000.md
```

### 2. Load Selected Progress

```
Loading handoff-2026-04-04-1430.md...

Session: User Authentication Feature
Last activity: 2 hours ago
Status: Database schema designed, API endpoints partially implemented

Next immediate step:
  - Complete /api-design for login endpoint
  - Run tests for password hashing

Ready to continue?
  A) Yes, load context and continue
  B) Show full handoff first
  C) Cancel
```

### 3. Context Restoration

After loading:
- Read key decisions
- Understand open questions
- Execute commands to resume

## Integration with Context Reset

The handoff artifact enables **context reset** - a fresh Evaluator session can objectively grade work without bias from building it.

## Reference

Base implementation: `@references/base/progress/skills/resume/SKILL.md`