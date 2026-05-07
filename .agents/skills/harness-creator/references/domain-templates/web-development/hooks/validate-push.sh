#!/bin/bash
# Dev Squad PreToolUse hook: Validates git push commands
# Receives JSON on stdin with tool_input.command
# Exit 0 = allow, Exit 2 = block (stderr shown to Claude)

INPUT=$(cat)

# Parse command
if command -v jq >/dev/null 2>&1; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
else
    COMMAND=$(echo "$INPUT" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"command"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

# Only process git push commands
if ! echo "$COMMAND" | grep -qE '^git[[:space:]]+push'; then
    exit 0
fi

# Check for force push
if echo "$COMMAND" | grep -qE '--force|-f'; then
    echo "BLOCKED: Force push detected. Use --force-with-lease if absolutely necessary, but this is generally unsafe." >&2
    exit 2
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

# Check if pushing to main/master
if echo "$COMMAND" | grep -qE "origin[[:space:]]+(main|master)"; then
    echo "WARNING: Pushing directly to main/master branch." >&2
    echo "Consider creating a pull request instead." >&2
    # Not blocking, just warning
fi

# Check if branch has uncommitted changes
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "WARNING: You have uncommitted changes." >&2
    echo "Consider committing or stashing before pushing." >&2
fi

# Check if branch is behind remote
REMOTE_BRANCH="origin/$BRANCH"
if git rev-parse --verify "$REMOTE_BRANCH" >/dev/null 2>&1; then
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse "$REMOTE_BRANCH" 2>/dev/null)
    MERGE_BASE=$(git merge-base "$LOCAL" "$REMOTE" 2>/dev/null)

    if [ "$MERGE_BASE" != "$REMOTE" ]; then
        echo "WARNING: Your branch is behind $REMOTE_BRANCH." >&2
        echo "Consider pulling and merging before pushing." >&2
    fi
fi

exit 0