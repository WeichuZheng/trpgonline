# Active Session State

## Session Info
- Session ID: session-[TIMESTAMP]
- Started: [START_TIME]
- Source: [fresh/checkpoint/handoff]

## Context Source
- [ ] Handoff (context reset)
- [ ] Checkpoint (manual save)
- [ ] Fresh start (new session)

## Current Work
- Task: [active task description]
- Status: [initializing/in_progress/blocked/complete]
- Started: [task start time]
- Priority: [high/medium/low]

## Sprint Contract
- File: .claude/sprint-contract.md
- Status: [none/draft/active/complete]
- Feature: [feature name if applicable]

## Files in Progress
| File | Status | Last Modified | Notes |
|------|--------|---------------|-------|
| [path/to/file] | [reading/editing/complete] | [time] | [notes] |

## Work Completed
### Done This Session
- [x] [completed item 1]
- [x] [completed item 2]

### Done Previously (if resuming)
- [x] [previous item 1]

## Work In Progress
### Current
- [ ] [current item] - [status/notes]

### Queued
- [ ] [next item 1]
- [ ] [next item 2]

## Blocked
- [ ] [blocked item] - [blocker description]
  - Resolution: [how to unblock]
  - Owner: [who can help]

## Key Decisions
1. [Decision] - [rationale]
   - Alternatives considered: [options]
   - Impact: [what this affects]

2. [Decision] - [rationale]
   - Made: [timestamp]
   - Reason: [why]

## Open Questions
- [Question 1]?
  - Context: [why this matters]
  - Impact: [what's blocked]
  - Options: [possible answers]

## Dependencies
- [dependency 1]: [status]
- [dependency 2]: [status]

## Notes
### Technical Notes
[Technical decisions, discoveries, learnings]

### Context Notes
[Important context for future reference]

## Git State
- Branch: [current branch]
- Uncommitted: [count] files
- Last commit: [hash] [message]

## Session Log
### [timestamp] - [event]
[Event details]

### [timestamp] - [event]
[Event details]

## Next Steps
1. [Immediate next action]
2. [Following action]
3. [Future consideration]

## Commands to Resume
```bash
# Resume this session
/start

# Or specific resume
/resume session-[TIMESTAMP]
```

---
Last updated: [TIMESTAMP]