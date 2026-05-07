# Context Management

Context is the most critical resource in a Claude Code session. Manage it actively.

## File-Backed State (Primary Strategy)

**The file is the memory, not the conversation.** Conversations are ephemeral and
will be compacted or lost. Files on disk persist across compactions and session crashes.

### Session State File

Maintain `production/session-state/active.md` as a living checkpoint. Update it
after each significant milestone:

- Design section approved and written to file
- Architecture decision made
- Implementation milestone reached
- Test results obtained
- Feature completed

The state file should contain:
- Current task and its status
- Progress checklist
- Key decisions made
- Files being worked on
- Open questions
- Next steps

### Status Block

Include a structured status block in `active.md`:

```markdown
<!-- STATUS -->
Project: [Project Name]
Feature: [Current Feature]
Task: [Current Task]
<!-- /STATUS -->
```

Update this block when switching focus areas. After any disruption (compaction,
crash, `/clear`), read the state file first.

---

## Incremental File Writing

When creating multi-section documents (API specs, design docs, ADRs):

1. Create the file immediately with a skeleton (all section headers, empty bodies)
2. Discuss and draft one section at a time in conversation
3. Write each section to the file as soon as it's approved
4. Update the session state file after each section
5. After writing a section, previous discussion can be safely compacted

This keeps the context window holding only the *current* section's discussion
instead of the entire document's conversation history.

---

## Proactive Compaction

- **Compact proactively** at ~60-70% context usage
- **Use `/clear`** between unrelated tasks
- **Natural compaction points:**
  - After writing a section to file
  - After committing
  - After completing a task
  - Before starting a new topic

---

## Progress Checkpoints

### Automatic Checkpoints

- **Session start**: Load `production/session-state/active.md`
- **Pre-compaction**: State dumped to conversation
- **Session end**: Log accomplishments

### Manual Checkpoints

Run `/checkpoint` to manually save progress:

```
/checkpoint [description]
```

This creates a timestamped checkpoint in `production/session-state/checkpoints/`.

---

## Recovery After Disruption

If context is lost or you start a new session:

1. **Automatic**: `session-start.sh` hook previews `active.md`
2. **Manual**: Run `/resume` to load last checkpoint
3. **Read files**: Load any files being actively worked on

---

## Compaction Instructions

When context is compacted, preserve in the summary:

- Reference to `production/session-state/active.md`
- List of files modified this session
- Architecture decisions and rationale
- Current task and progress
- Test results (pass/fail)
- Unresolved blockers
- Next steps

**After compaction:** Read `production/session-state/active.md` to recover state.