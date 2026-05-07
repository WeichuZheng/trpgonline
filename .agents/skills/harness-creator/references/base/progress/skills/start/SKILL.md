---
name: start
description: "Smart session onboarding — checks for handoff artifacts first, then checkpoints, then offers fresh start with sprint contract. No assumptions about session state."
user-invocable: true
---

# Start Skill

You are facilitating smart session onboarding. Your role is to detect any saved progress and offer continuation, or guide a fresh start with proper context setup.

## Purpose

The `/start` skill ensures:
- No lost work between sessions
- Smooth context reset transitions
- Clear session state from the beginning
- Proper sprint contract for fresh starts

## Onboarding Flow

```
Session Start
    |
    +--[1] Handoff artifact exists? (.claude/handoff.md)
    |       |
    |       +-- YES --> Load handoff, continue work
    |       |           Show: Session summary, current state, next step
    |       |           Ask: "Continue from handoff?"
    |       |
    |       +-- NO --> Continue to [2]
    |
    +--[2] Checkpoint exists? (.claude/checkpoint.md)
    |       |
    |       +-- YES --> Load checkpoint, offer resume
    |       |           Show: Last saved state, time since save
    |       |           Ask: "Resume from checkpoint?"
    |       |
    |       +-- NO --> Continue to [3]
    |
    +--[3] Fresh Start
            |
            +-- Check for project context (CLAUDE.md, .claude/)
            +-- Offer: Load project or start sprint contract
            +-- Guide: Set up session with clear goals
```

## Detection Logic

### 1. Handoff Artifact Check

**Location**: `.claude/handoff.md`

Handoff artifacts are created during context reset. They contain:
- Session summary
- Completed work
- Current state
- Next immediate step
- Key decisions
- Open questions
- Resume commands

**If found**:
```
HANDOFF DETECTED: Previous session requested context reset.

Session Summary: [From handoff artifact]
Current State: [From handoff artifact]
Next Step: [From handoff artifact]

Options:
1. Continue from handoff (recommended for context reset)
2. Ignore and check for checkpoint
3. Fresh start (discards handoff context)

What would you like to do?
```

### 2. Checkpoint Check

**Location**: `.claude/checkpoint.md`

Checkpoints are manual saves during sessions. They contain:
- Timestamp
- Work in progress
- Files being modified
- Current task
- Blockers/notes

**If found**:
```
CHECKPOINT DETECTED: Previous session saved progress.

Saved: [timestamp from checkpoint]
Task: [current task from checkpoint]
Files: [modified files list]

Options:
1. Resume from checkpoint
2. Ignore and start fresh
3. View checkpoint details first

What would you like to do?
```

### 3. Fresh Start

**No saved progress found**:
```
FRESH SESSION

Project: [detected from CLAUDE.md or git]
Branch: [current git branch]
Recent commits: [last 3 commits]

Options:
1. Start new feature (sprint contract flow)
2. Load existing project context
3. Continue recent work [show last commit]
4. Custom task

What would you like to work on?
```

## Sprint Contract Flow (Fresh Start)

When starting fresh with new work:

### Step 1: Define Scope
```
What are you building?
- Feature name/description
- Target components (frontend/backend/database)
- Success criteria (what does "done" look like?)
```

### Step 2: Generate Contract
Create a sprint contract with:
- Clear scope boundaries
- Testable behaviors
- Acceptance criteria

### Step 3: Confirm Contract
```
SPRINT CONTRACT GENERATED

Scope: [summary]
Behaviors: [count] testable criteria
Acceptance: [count] pass/fail conditions

1. Accept and begin implementation
2. Modify contract
3. Save for later

Proceed with implementation?
```

## Session State Tracking

After onboarding, maintain session state:

```markdown
# Active Session: [session-id]

## Context Source
- [ ] Handoff (context reset)
- [ ] Checkpoint (manual save)
- [ ] Fresh start (new session)

## Current Work
- Task: [active task]
- Status: [status]
- Started: [timestamp]

## Sprint Contract
- File: .claude/sprint-contract.md
- Status: [DRAFT/ACTIVE/COMPLETE]

## Files in Progress
- [file1]: [status]
- [file2]: [status]

## Notes
- [session notes]
```

## Implementation Checklist

When running `/start`, execute in order:

1. [ ] Check for `.claude/handoff.md`
2. [ ] Check for `.claude/checkpoint.md`
3. [ ] Check for `.claude/session-state.md`
4. [ ] Detect project context (CLAUDE.md, package.json, etc.)
5. [ ] Present appropriate options
6. [ ] Load selected context
7. [ ] Initialize session state file
8. [ ] Confirm ready state with user

## Output Format

```
SESSION READY

Context: [handoff/checkpoint/fresh]
Task: [active task or "awaiting input"]
Contract: [active/draft/none]
Progress: [if resuming, show % complete]

Next action: [suggested first action]

Ready to proceed!
```

## Usage

```
/start                    # Auto-detect saved progress
/start --fresh            # Skip all saved progress
/start --checkpoint       # Force checkpoint resume
/start --handoff          # Force handoff resume
```

## Integration Points

- **With /checkpoint**: Creates checkpoints for future sessions
- **With /resume**: Loads specific checkpoint by ID
- **With sprint-contract**: Initiates contract flow for fresh starts
- **With hooks**: session-start.sh calls this skill automatically