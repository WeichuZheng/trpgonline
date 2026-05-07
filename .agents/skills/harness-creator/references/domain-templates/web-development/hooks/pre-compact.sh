#!/bin/bash
# Dev Squad PreCompact hook: Dump session state before context compression
# This output appears in the conversation right before compaction

echo "=== SESSION STATE BEFORE COMPACTION ==="
echo "Timestamp: $(date)"

# --- Active session state file ---
STATE_FILE="production/session-state/active.md"
if [ -f "$STATE_FILE" ]; then
    echo ""
    echo "## Active Session State (from $STATE_FILE)"
    STATE_LINES=$(wc -l < "$STATE_FILE" 2>/dev/null | tr -d ' ')
    if [ "$STATE_LINES" -gt 80 ] 2>/dev/null; then
        head -n 80 "$STATE_FILE"
        echo "... (truncated — $STATE_LINES total lines)"
    else
        cat "$STATE_FILE"
    fi
else
    echo ""
    echo "## No active session state file found"
    echo "Run /checkpoint to create one for better recovery."
fi

# --- Latest checkpoint ---
CHECKPOINT_DIR="production/session-state/checkpoints"
if [ -d "$CHECKPOINT_DIR" ]; then
    LATEST=$(ls -t "$CHECKPOINT_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        echo ""
        echo "## Latest Checkpoint: $(basename "$LATEST")"
        head -n 20 "$LATEST" 2>/dev/null
    fi
fi

# --- Files modified this session ---
echo ""
echo "## Files Modified (git working tree)"

CHANGED=$(git diff --name-only 2>/dev/null)
STAGED=$(git diff --staged --name-only 2>/dev/null)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null)

if [ -n "$CHANGED" ]; then
    echo "Unstaged changes:"
    echo "$CHANGED" | while read -r f; do echo "  - $f"; done
fi
if [ -n "$STAGED" ]; then
    echo "Staged changes:"
    echo "$STAGED" | while read -r f; do echo "  - $f"; done
fi
if [ -n "$UNTRACKED" ]; then
    echo "New untracked files:"
    echo "$UNTRACKED" | while read -r f; do echo "  - $f"; done
fi
if [ -z "$CHANGED" ] && [ -z "$STAGED" ] && [ -z "$UNTRACKED" ]; then
    echo "  (no uncommitted changes)"
fi

# --- Log compaction event ---
SESSION_LOG_DIR="production/session-logs"
mkdir -p "$SESSION_LOG_DIR" 2>/dev/null
echo "Context compaction at $(date)." >> "$SESSION_LOG_DIR/compaction-log.txt" 2>/dev/null

echo ""
echo "## Recovery Instructions"
echo "After compaction, run /resume to recover context."
echo "Or read: $STATE_FILE"
echo "=== END SESSION STATE ==="

exit 0