# Handoff Artifact

## Purpose

This artifact enables seamless continuation after a **Context Reset** - a structured handoff from a Generator session to a fresh Evaluator session. It captures all essential context needed for a new session to pick up exactly where this one left off.

**Context Reset vs Compaction:**
- **Compaction**: Claude Code compresses conversation history when approaching limits
- **Context Reset**: Structured handoff where Generator creates artifact for fresh Evaluator session

**Why Context Reset Matters:**
- Fresh Evaluator has no bias from building the feature
- Prevents cascade errors from accumulated assumptions
- Enables longer-running tasks than single session allows
- Provides natural review checkpoint

---

## Session Summary

**Task**: [What was being built - 1-2 sentence summary]

**Scope**: [What was in scope for this session]

**Started**: [Session start timestamp]
**Ended**: [Session end timestamp]
**Duration**: [Total time]

---

## Completed Work

### Done
- [x] [Completed item 1] - [brief result]
- [x] [Completed item 2] - [brief result]
- [x] [Completed item 3] - [brief result]

### Verified
- [x] [Verified item with evidence] - [how verified]
- [x] [Test passed] - [test name]

### Committed
- [hash] [commit message]
- [hash] [commit message]

---

## Current State

### Where We Stopped
[Exact point where work stopped - be specific]

**Last Action**: [What was just completed or attempted]

**Current File**: [File being worked on when stopped]

**Line/Function**: [Specific location if applicable]

### Files Modified
| File | Status | Changes Made | Lines |
|------|--------|--------------|-------|
| path/to/file.py | modified | [specific changes] | +X/-Y |
| path/to/new.py | created | [what was added] | +X |

### Files to Review
1. `path/to/file1.py` - [why important for continuation]
2. `path/to/file2.py` - [why important for continuation]

### Test Status
```
[Last test output or summary]
```

### Git State
- Branch: [branch name]
- Uncommitted: [count] files
- Last commit: [hash] [message]

---

## Next Immediate Step

**What to do next**: [Single most important action]

**How to do it**:
```
[Exact commands or steps]
```

**Expected outcome**: [What success looks like]

**Blockers**: [Any known blockers - or "None"]

---

## Key Decisions

### Decision 1: [Decision Title]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice]
- **Alternatives Considered**: [Other options]
- **Impact**: [What this affects]
- **Trade-offs**: [What was given up]

### Decision 2: [Decision Title]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice]
- **Impact**: [What this affects]

---

## Open Questions

### Unresolved
1. **[Question 1]**
   - Context: [Why this matters]
   - Impact: [What's blocked]
   - Suggested approach: [How to resolve]

2. **[Question 2]**
   - Context: [Why this matters]
   - Options: [Possible answers]

### Needs Discussion
- [Item needing team discussion]
- [Item requiring stakeholder input]

---

## Technical Context

### Architecture
[Brief architecture overview relevant to current work]

### Key Patterns
- [Pattern 1]: [where used, why important]
- [Pattern 2]: [where used, why important]

### Dependencies
- [Dependency]: [version] - [status/importance]

### Environment
- [Special setup required]
- [Environment variables or config]

### Known Issues
- [Issue]: [workaround or status]

---

## Commands to Resume

### Quick Resume
```bash
# Resume the work immediately
cd [project-directory]
/start --handoff
```

### Manual Resume
```bash
# Read this handoff
cat .claude/handoff.md

# View current git state
git status

# View modified files
git diff

# Run tests
[command to run tests]

# Continue development
[command to start dev server]
```

### File Commands
```bash
# View key file 1
cat path/to/file1.py

# View key file 2
cat path/to/file2.py

# Check specific function
grep -n "function_name" path/to/file.py
```

---

## Success Criteria

### For This Session
- [x] [Criterion 1 met]
- [ ] [Criterion 2 in progress]
- [ ] [Criterion 3 pending]

### Sprint Contract Reference
- Contract file: `.claude/sprint-contract.md`
- Status: [draft/active/complete]
- Pass criteria: [link to contract]

---

## Warnings & Gotchas

### Be Careful
- **[Warning 1]**: [Why this matters]
- **[Warning 2]**: [How to avoid issue]

### Don't
- **Don't** [action] because [reason]
- **Avoid** [action] because [reason]

### Do
- **Do** [action] because [reason]
- **Remember** [important thing]

---

## Resources

### Documentation
- [Doc 1]: [link or path]
- [Doc 2]: [link or path]

### Related Files
- [File 1]: [purpose]
- [File 2]: [purpose]

### External References
- [Reference 1]: [URL]
- [Reference 2]: [URL]

---

## Checklist for New Session

Before continuing, verify:

- [ ] Read this entire handoff document
- [ ] Reviewed git status and recent commits
- [ ] Understand current state and next step
- [ ] Check sprint contract (if exists)
- [ ] Review key decisions made
- [ ] Note any open questions

---

## Handoff Metadata

- **Created**: [Timestamp]
- **Session ID**: session-[ID]
- **Generator**: [Agent/Session that created this]
- **Checkpoint**: cp-[checkpoint-id] (backup)
- **TTL**: [When this becomes stale]

---

## Notes

[Any additional context for the next session]