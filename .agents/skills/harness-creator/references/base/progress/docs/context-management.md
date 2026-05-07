# Context Management: Reset vs Compaction

## Overview

Claude Code has two mechanisms for handling context limits: **Context Compaction** and **Context Reset**. Understanding when to use each is critical for maintaining productivity on long-running tasks.

## Context Compaction

### What It Is

Context compaction is Claude Code's automatic process of compressing conversation history when approaching token limits. It summarizes older exchanges to make room for new content.

### How It Works

```
Full Context
     |
     v [approaching limit]
     |
Compaction
     |
     v
Compressed Context
(older exchanges summarized)
```

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Trigger | Automatic when approaching context limit |
| Speed | Fast, happens in-place |
| Visibility | Often transparent to user |
| Context Loss | Some detail loss in summarized exchanges |
| Session Continuity | Maintains full session flow |

### What Gets Compacted

1. **Older exchanges**: Earlier conversation turns are summarized
2. **Redundant information**: Repeated context is removed
3. **Verbose content**: Long outputs are condensed
4. **Resolved topics**: Completed discussions are abbreviated

### What Gets Preserved

1. **Recent exchanges**: Last N turns remain detailed
2. **Active files**: Currently open file contexts
3. **Critical decisions**: Key choices are retained
4. **Current task context**: Active work remains visible

### Pros

- **Automatic**: No user intervention needed
- **Seamless**: Often undetectable
- **Continuous**: No session break

### Cons

- **Bias carries forward**: Same session assumptions persist
- **Detail loss**: Nuances from early conversation lost
- **Cascade risk**: Early errors propagate through session
- **Limited recovery**: Can't restore compacted context

### Best For

- Short to medium tasks
- Linear work without backtracking
- Sessions where early context is less critical
- Quick iterations and fixes

---

## Context Reset

### What It Is

Context reset is a **structured handoff** where the current session creates a comprehensive artifact for a fresh session. The new session starts with a clean context and loads only the handoff information.

### How It Works

```
Generator Session
     |
     v [approaching complexity limit]
     |
Create Handoff Artifact
     |
     v
Fresh Evaluator Session
     |
     v
Load Handoff
     |
     v
Continue Work
```

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Trigger | Manual or pre-compact hook |
| Speed | Requires setup, then instant load |
| Visibility | Fully transparent |
| Context Freshness | Completely fresh context |
| Session Break | Explicit session boundary |

### Handoff Artifact Contents

```markdown
# Handoff Artifact

## Session Summary
[What was being built]

## Completed Work
[What's done]

## Current State
[Where we stopped]

## Next Immediate Step
[What to do next]

## Key Decisions
[Choices made]

## Open Questions
[Things to resolve]

## Commands to Resume
[How to continue]
```

### Pros

- **Fresh perspective**: New session without accumulated bias
- **Review opportunity**: Natural checkpoint for evaluation
- **Clean context**: No noise from earlier exploration
- **Error isolation**: Fresh start prevents cascade errors

### Cons

- **Manual overhead**: Requires creating handoff
- **Session break**: Interrupts flow
- **Potential gaps**: Risk of missing context in handoff
- **Learning curve**: Team needs to understand process

### Best For

- Complex, multi-session tasks
- Features requiring review gates
- Work spanning multiple days
- Tasks where early assumptions may be wrong

---

## Comparison Matrix

| Factor | Compaction | Reset |
|--------|------------|-------|
| Trigger | Automatic | Manual/Semi-auto |
| Context | Compressed | Fresh |
| Session | Continuous | New |
| Bias | Carries forward | Reset |
| Speed | Instant | Handoff required |
| Best for | Short tasks | Complex tasks |
| Error propagation | Possible | Isolated |
| Review | No | Yes (natural) |

---

## When to Use Each

### Use Compaction When

- Task is straightforward
- Session is under 2 hours
- Early context is not critical
- Quick fix or small feature
- Flow is linear and clear

### Use Reset When

- Task is complex or ambiguous
- Session has been long
- Early decisions may need review
- Building something new
- Assumptions should be validated
- Multiple days of work
- Generator/Evaluator split needed

---

## Implementation Guide

### Setting Up Context Reset

#### 1. Create Checkpoint

```bash
/checkpoint "pre-reset"
```

#### 2. Create Handoff Artifact

```bash
# Use the handoff template
# Fill in all sections comprehensively
```

#### 3. End Session

```bash
# Handoff is ready for fresh session
```

#### 4. Resume in Fresh Session

```bash
/start --handoff
# or
/resume [checkpoint-id]
```

### Automated Reset (via Hooks)

The `pre-compact.sh` hook automatically:

1. Creates checkpoint before compaction
2. Generates handoff draft
3. Preserves session state

Configure in `.claude/settings.json`:

```json
{
  "hooks": {
    "pre-compact": ".claude/hooks/pre-compact.sh"
  }
}
```

---

## Anti-Patterns

### Anti-Pattern: Never Reset

**Problem**: Long-running sessions accumulate bias and errors.

**Solution**: Schedule resets for complex tasks, even if not forced by limits.

### Anti-Pattern: Reset Without Handoff

**Problem**: Fresh session has no context, must start from scratch.

**Solution**: Always create comprehensive handoff artifact before reset.

### Anti-Pattern: Incomplete Handoff

**Problem**: Missing context causes rework or errors.

**Solution**: Use handoff template, fill all sections, verify completeness.

### Anti-Pattern: Resuming Without Review

**Problem**: Blindly continuing without evaluating previous work.

**Solution**: Fresh Evaluator should review Generator's work as part of reset.

---

## Generator/Evaluator Pattern

Context reset enables the Generator/Evaluator pattern from multi-agent architecture:

```
Generator Session          Evaluator Session
       |                         |
       v                         v
Build Feature              Review Work
       |                         |
       v                         v
Create Handoff      <--     Load Handoff
       |                         |
       v                         v
Mark for Review            Validate Work
       |                         |
       v                         v
Wait for Result            Report Findings
       |                         |
       v                         v
Receive Feedback           Send Feedback
```

### Benefits

1. **Objectivity**: Evaluator has no bias from building
2. **Quality**: Fresh eyes catch issues Generator misses
3. **Documentation**: Handoff creates audit trail
4. **Learning**: Team learns from documented decisions

---

## Best Practices

### Compaction Best Practices

1. Don't fight compaction - let it happen
2. Keep recent context relevant
3. Make key decisions explicit
4. Document important context early

### Reset Best Practices

1. Create handoff before forced compaction
2. Use template for consistency
3. Include commands to resume
4. Note all open questions
5. Document key decisions with rationale

### General Best Practices

1. Use `/checkpoint` regularly
2. Document as you go
3. Review handoff before accepting
4. Match reset strategy to task complexity

---

## Summary

| Strategy | Use Case |
|----------|----------|
| Compaction | Short, straightforward tasks |
| Reset | Complex, multi-day, review-needed tasks |
| Hybrid | Start with compaction, reset at natural break points |

The key insight: **Context reset is a feature, not a limitation**. It provides a natural checkpoint for review and enables the Generator/Evaluator pattern that improves quality.

---

## Related Documents

- `skills/start/SKILL.md` - Session initialization
- `skills/checkpoint/SKILL.md` - Creating checkpoints
- `skills/resume/SKILL.md` - Loading checkpoints
- `templates/handoff-artifact.md` - Handoff template
- `templates/checkpoint.md` - Checkpoint template