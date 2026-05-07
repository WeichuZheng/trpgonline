---
name: checkpoint
description: "Save current progress to a checkpoint file. Use before context-heavy operations or as regular backup."
user-invocable: true
---

# Checkpoint Skill

You are saving session progress to a checkpoint file. This enables resumption after context compaction, session end, or context reset.

## Purpose

Checkpoints provide:
- Work continuity across sessions
- Recovery from context loss
- Progress backup before risky operations
- Handoff preparation for context reset

## When to Checkpoint

**Automatic Triggers:**
- Before major refactoring
- After completing significant work
- Before context-heavy operations
- Pre-compact hook (automatic)

**Manual Triggers:**
- User calls `/checkpoint`
- Before ending a session
- When switching tasks mid-stream

## Checkpoint Process

```
/checkpoint [message]
     |
     +--[1] Gather session state
     |       - Current task
     |       - Files modified
     |       - Decisions made
     |       - Open questions
     |
     +--[2] Write checkpoint file
     |       - .claude/checkpoint.md
     |       - Timestamp
     |       - Full context dump
     |
     +--[3] Confirm save
             - Show summary
             - Offer to continue or exit
```

## Checkpoint File Structure

```markdown
# Checkpoint: [timestamp]

## Session Info
- Started: [session start time]
- Saved: [checkpoint timestamp]
- Duration: [elapsed time]

## Current Task
[Description of active task]

## Work Completed
### Done
- [item 1]
- [item 2]

### In Progress
- [item 3] - [status/notes]

### Blocked
- [item 4] - [blocker description]

## Files Modified
| File | Status | Changes |
|------|--------|---------|
| path/to/file.py | modified | [summary] |
| path/to/other.py | created | [summary] |

## Key Decisions
1. [Decision] - [rationale]
2. [Decision] - [rationale]

## Open Questions
- [question 1] - [context/impact]
- [question 2] - [context/impact]

## Next Steps
1. [immediate next action]
2. [following action]
3. [future consideration]

## Commands to Resume
```bash
# To resume this checkpoint:
/resume [checkpoint-id]

# Or run:
/start
```

## Context Snapshot
```
[Recent conversation summary - key points only]
```

## Git State
- Branch: [current branch]
- Uncommitted: [yes/no - count of files]
- Last commit: [hash] [message]
```

## Implementation Steps

### Step 1: Collect Context

```
1. Read conversation history (last N exchanges)
2. Identify active task from context
3. List all files read/modified this session
4. Capture key decisions and rationale
5. Note open questions and blockers
```

### Step 2: Generate Checkpoint

```
1. Create checkpoint directory if needed
2. Write checkpoint file with timestamp
3. Include all sections from template
4. Add git status if in repo
```

### Step 3: Confirm

```
CHECKPOINT SAVED

ID: checkpoint-[timestamp]
File: .claude/checkpoint.md

Summary:
- Task: [active task]
- Files: [count] modified
- Duration: [session duration]

Options:
1. Continue working
2. End session (checkpoint preserved)
3. Create handoff artifact (for context reset)
```

## Checkpoint Management

### Checkpoint Rotation

Keep last N checkpoints (configurable, default 5):
```
.claude/
  checkpoints/
    checkpoint-2024-01-15-001.md
    checkpoint-2024-01-15-002.md
    checkpoint-2024-01-15-003.md  (newest)
```

### Checkpoint Cleanup

- Auto-delete checkpoints older than 7 days
- Keep named checkpoints indefinitely
- Archive checkpoints when handoff created

## Integration with Context Reset

Before context reset, checkpoint automatically:
```
1. /checkpoint "pre-context-reset"
2. Create handoff artifact from checkpoint
3. Fresh session loads handoff
4. Continue without lost context
```

## Usage

```
/checkpoint                    # Save with auto-message
/checkpoint "pre-refactor"     # Save with description
/checkpoint --named "v1"       # Save named checkpoint
/checkpoint --list             # List all checkpoints
```

## Output

```
CHECKPOINT CREATED

ID: cp-2024-01-15-143052
File: .claude/checkpoints/cp-2024-01-15-143052.md

Task: Implementing user authentication
Progress: 60% complete
Files: 4 modified, 2 created

Resume with: /resume cp-2024-01-15-143052
```

## Error Handling

```
CHECKPOINT FAILED

Error: [error description]
Recovery: [suggested fix]

Partial save available at: .claude/checkpoint-partial.md
Manual intervention may be needed.
```

## Integration Points

- **With /start**: Loads checkpoints on session start
- **With /resume**: Loads specific checkpoint by ID
- **With pre-compact hook**: Called automatically before context compaction
- **With session-stop hook**: Saves final checkpoint on session end