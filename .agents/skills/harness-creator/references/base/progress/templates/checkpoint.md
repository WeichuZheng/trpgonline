# Checkpoint: [TIMESTAMP]

## Session Info
- Session ID: session-[ID]
- Started: [SESSION_START_TIME]
- Saved: [CHECKPOINT_TIMESTAMP]
- Duration: [elapsed time]

## Context
- Source: [fresh/checkpoint/handoff]
- Project: [project name]
- Branch: [git branch]

## Current Task
[Description of active task]

**Status**: [initializing/in_progress/blocked/complete]

**Priority**: [high/medium/low]

## Work Completed
### Done This Session
- [x] [completed item 1] - [timestamp]
- [x] [completed item 2] - [timestamp]

### Done Previously
- [x] [previous item 1]

## Work In Progress
### Current Focus
- [ ] [current item] - [percentage] complete
  - [subtask 1]: done
  - [subtask 2]: in progress
  - [subtask 3]: pending

### Queued
- [ ] [next item 1]
- [ ] [next item 2]

## Blocked
- [ ] [blocked item]
  - Blocker: [what's blocking]
  - Resolution: [how to unblock]
  - Owner: [who can help]
  - ETA: [expected resolution]

## Files Modified
| File | Status | Changes | Lines |
|------|--------|---------|-------|
| path/to/file.py | modified | [summary] | +X/-Y |
| path/to/new.py | created | [summary] | +X |
| path/to/old.py | deleted | [reason] | -Y |

### Files to Review on Resume
1. `path/to/file1.py` - [why important]
2. `path/to/file2.py` - [why important]

## Key Decisions
### Decision 1: [Decision Title]
- **Made**: [timestamp]
- **Decision**: [what was decided]
- **Rationale**: [why]
- **Alternatives**: [what else was considered]
- **Impact**: [what this affects]

### Decision 2: [Decision Title]
- **Made**: [timestamp]
- **Decision**: [what was decided]
- **Rationale**: [why]

## Open Questions
### Question 1: [Question]
- **Context**: [why this matters]
- **Impact**: [what's blocked]
- **Options**:
  1. [option 1] - [pros/cons]
  2. [option 2] - [pros/cons]
- **Owner**: [who should decide]

### Question 2: [Question]
- **Context**: [why this matters]
- **Status**: [unresolved/escalated]

## Technical Context
### Architecture
[Brief architecture context relevant to current work]

### Dependencies
- [dependency 1]: [version] - [status]
- [dependency 2]: [version] - [status]

### Patterns Used
- [pattern 1]: [where/why]
- [pattern 2]: [where/why]

## Git State
- **Branch**: [branch name]
- **Base**: [parent branch or main]
- **Uncommitted**: [count] files
- **Staged**: [count] files
- **Last Commit**: [hash] [message]

### Uncommitted Changes
```
M  path/to/modified/file.py
A  path/to/new/file.py
D  path/to/deleted/file.py
```

## Next Steps
### Immediate (next session)
1. [First action to take]
2. [Second action]

### Short Term
- [ ] [item 1]
- [ ] [item 2]

### Considerations
- [ ] [consideration 1]
- [ ] [consideration 2]

## Context Snapshot
### Recent Conversation Summary
[Key points from recent conversation - 3-5 bullet points]

### Important Context
[Context needed to continue work effectively]

## Commands to Resume
```bash
# Resume this checkpoint
/resume [checkpoint-id]

# Or use start
/start

# View files in progress
cat .claude/session-state.md
```

## Notes
[Any additional notes for future reference]

---
Checkpoint ID: cp-[TIMESTAMP]
Created: [TIMESTAMP]