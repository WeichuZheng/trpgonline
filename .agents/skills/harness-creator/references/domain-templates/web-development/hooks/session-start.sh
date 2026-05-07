#!/bin/bash
# Dev Squad SessionStart hook: Load project context at session start
# Outputs context to stderr (shown to Claude)

echo "=== Dev Squad Session Started ===" >&2

# Show current git status
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$BRANCH" ]; then
    echo "Branch: $BRANCH" >&2
fi

# Show recent commits
echo "" >&2
echo "Recent commits:" >&2
git log --oneline -5 2>/dev/null >&2

# Check for uncommitted changes
CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$CHANGES" -gt 0 ]; then
    echo "" >&2
    echo "Uncommitted changes: $CHANGES files" >&2
fi

# Check for active session state
STATE_FILE="production/session-state/active.md"
if [ -f "$STATE_FILE" ]; then
    echo "" >&2
    echo "=== Active Session State ===" >&2
    head -30 "$STATE_FILE" 2>/dev/null >&2
    echo "" >&2
    echo "Run /resume to load full context" >&2
fi

# Check for recent checkpoints
CHECKPOINT_DIR="production/session-state/checkpoints"
if [ -d "$CHECKPOINT_DIR" ]; then
    LATEST_CHECKPOINT=$(ls -t "$CHECKPOINT_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_CHECKPOINT" ]; then
        echo "" >&2
        echo "Latest checkpoint: $(basename "$LATEST_CHECKPOINT")" >&2
    fi
fi

# Show TODO count
TODO_COUNT=$(find src -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) -exec grep -l "TODO\|FIXME" {} \; 2>/dev/null | wc -l)
if [ "$TODO_COUNT" -gt 0 ]; then
    echo "" >&2
    echo "Files with TODOs: $TODO_COUNT" >&2
fi

echo "" >&2
echo "================================" >&2
echo "Run /start for guided onboarding" >&2
echo "Run /resume to continue previous work" >&2
echo "================================" >&2

exit 0