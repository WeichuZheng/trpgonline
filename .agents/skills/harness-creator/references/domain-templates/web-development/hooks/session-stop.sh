#!/bin/bash
# Dev Squad Stop hook: Log session accomplishments
# Runs when session ends

# Create directories if they don't exist
mkdir -p production/session-state/checkpoints
mkdir -p production/session-logs

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="production/session-logs/session_${TIMESTAMP}.md"

# Get session summary from git
COMMITS=$(git log --oneline --since="1 hour ago" 2>/dev/null | head -10)
CHANGED_FILES=$(git diff --name-only HEAD~5 2>/dev/null | head -20)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

# Write session log
cat > "$LOG_FILE" << EOF
# Session Log: $TIMESTAMP

## Summary
- Branch: ${BRANCH:-unknown}
- Session ended at $(date)

## Commits This Session
\`\`\`
$COMMITS
\`\`\`

## Files Modified
\`\`\`
$CHANGED_FILES
\`\`\`
EOF

# Update active state with session end marker
STATE_FILE="production/session-state/active.md"
if [ -f "$STATE_FILE" ]; then
    # Append session end note
    echo "" >> "$STATE_FILE"
    echo "---" >> "$STATE_FILE"
    echo "**Session ended**: $(date)" >> "$STATE_FILE"
fi

echo "Session logged to $LOG_FILE" >&2

exit 0