---
name: resume
description: "Load previous checkpoint or session state. Use after context loss, session restart, or to pick up previous work."
user-invocable: true
---

# Resume Skill

You are loading a previous checkpoint to restore session context. This enables continuation of work across sessions or after context loss events.

## Purpose

Resume enables:
- Picking up work after session end
- Recovery from context compaction
- Context reset continuation
- Task switching without lost context

## Resume Flow

```
/resume [checkpoint-id]
     |
     +--[1] No ID provided?
     |       |
     |       +-- List available checkpoints
     |       +-- Prompt user selection
     |
     +--[2] Load checkpoint file
     |       |
     |       +-- Parse checkpoint content
     |       +-- Validate checkpoint integrity
     |       +-- Extract session state
     |
     +--[3] Restore context
             |
             +-- Display session summary
             +-- Show files in progress
             +-- List next steps
             +-- Confirm continuation
```

## Checkpoint Discovery

### List Available Checkpoints

```
RESUME: Available Checkpoints

| ID | Date | Task | Status |
|----|----|------|--------|
| cp-2024-01-15-143052 | Today 14:30 | User auth | In Progress |
| cp-2024-01-14-091523 | Yesterday | API design | Complete |
| cp-2024-01-13-165234 | Jan 13 | Database | Blocked |

Which checkpoint would you like to resume?
Enter ID or number:
```

### Checkpoint Sources

1. **Manual checkpoints**: Created via `/checkpoint`
2. **Auto checkpoints**: Created by pre-compact hook
3. **Session end checkpoints**: Created by session-stop hook
4. **Named checkpoints**: Created with `--named` flag

## Resume Process

### Step 1: Locate Checkpoint

```
Search order:
1. .claude/checkpoints/[checkpoint-id].md
2. .claude/checkpoint.md (latest)
3. .claude/session-state.md
```

### Step 2: Validate Checkpoint

```markdown
CHECKPOINT VALIDATION

File: [checkpoint file]
Age: [time since save]
Integrity: [valid/invalid]

Missing sections: [any missing required sections]
Stale files: [files changed since checkpoint]

Warnings:
- [any warnings about stale context]

Continue with resume? [y/n]
```

### Step 3: Load Context

```
LOADING CHECKPOINT

Session: [session info from checkpoint]
Task: [task description]
Progress: [status from checkpoint]

Files to review:
- [file1] ([status])
- [file2] ([status])

Key decisions made:
1. [decision]
2. [decision]

Open questions:
- [question]

Next steps:
1. [step 1]
2. [step 2]

Restoring context...
```

### Step 4: Confirm State

```
SESSION RESTORED

From: cp-2024-01-15-143052
Saved: Today 14:30 (2 hours ago)

Current Task: Implementing user authentication
Progress: 60% complete

Last action: [last action before checkpoint]
Next step: [immediate next action]

Ready to continue?
[y]es, [r]eview files, [d]ifferent checkpoint
```

## Context Restoration

### What Gets Restored

1. **Task Context**
   - Active task description
   - Progress status
   - Work completed
   - Work in progress

2. **File Context**
   - Files being modified
   - Changes made (summary)
   - Files to review

3. **Decision Context**
   - Key decisions made
   - Rationale for choices
   - Rejected alternatives

4. **Blocker Context**
   - Open questions
   - Blockers encountered
   - Dependencies

### What Requires Refresh

1. **File Contents**: Read files again to see current state
2. **Git State**: Check for external changes
3. **Environment**: Re-validate dependencies
4. **Recent Changes**: Check for commits since checkpoint

## Resume Strategies

### Full Resume

```
/resume cp-2024-01-15-143052 --full

Loads everything:
- Reads all modified files
- Reconstructs conversation context
- Validates current state
- Confirms next action
```

### Quick Resume

```
/resume cp-2024-01-15-143052 --quick

Loads minimal context:
- Task and progress summary
- Next steps only
- Skips detailed review
```

### Selective Resume

```
/resume cp-2024-01-15-143052 --files="auth.py,users.py"

Loads only:
- Specified file contexts
- Related decisions
- Skips unrelated content
```

## Stale Context Handling

When checkpoint context is stale:

```
STALE CHECKPOINT DETECTED

Checkpoint: 2 days ago
Files modified since: 3

Modified files:
- src/auth.py (modified externally)
- tests/test_auth.py (new file)
- docs/api.md (deleted)

Options:
1. Load anyway (may have conflicts)
2. Show diff (checkpoint vs current)
3. Choose different checkpoint
4. Fresh start

How would you like to proceed?
```

## Integration with /start

Resume is automatically invoked by `/start`:

```
/start
    |
    +-- Finds checkpoint
    |
    +-- Calls /resume automatically
    |
    +-- User confirms or chooses different action
```

## Usage

```
/resume                           # List and select checkpoint
/resume cp-2024-01-15-143052      # Resume specific checkpoint
/resume --latest                  # Resume most recent
/resume --named "v1"              # Resume named checkpoint
/resume --list                    # List all without resuming
```

## Output

```
SESSION RESTORED

Checkpoint: cp-2024-01-15-143052
Saved: January 15, 2024 at 14:30

Task: Implement user authentication
Status: In Progress (60%)

Completed:
- Password hashing
- Session management
- Basic login flow

In Progress:
- OAuth integration (blocked on API key)

Next Action: Request OAuth API key from admin

Files to review:
- src/auth.py
- src/models/user.py
- tests/test_auth.py

Ready to continue!
```

## Error Recovery

```
CHECKPOINT NOT FOUND

ID: cp-2024-01-15-143052
Search locations:
- .claude/checkpoints/ (not found)
- .claude/checkpoint.md (not found)

Options:
1. List available checkpoints
2. Start fresh
3. Check different location
```

## Integration Points

- **With /start**: Auto-detected and offered on fresh session
- **With /checkpoint**: Creates checkpoints that /resume can load
- **With handoff-artifact**: Handoff creates checkpoint before context reset