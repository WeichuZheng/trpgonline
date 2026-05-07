#!/bin/bash
# Pre-Compact Hook
# Called before Claude Code performs context compaction
# Purpose: Dump session state to prevent context loss

set -e

# Configuration
CLAUDE_DIR=".claude"
CHECKPOINT_DIR="$CLAUDE_DIR/checkpoints"
SESSION_FILE="$CLAUDE_DIR/session-state.md"
PRE_COMPACT_FILE="$CLAUDE_DIR/pre-compact-state.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${BLUE}[pre-compact]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[pre-compact]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[pre-compact]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[pre-compact]${NC} $1"
}

# Ensure directories exist
ensure_dirs() {
    mkdir -p "$CHECKPOINT_DIR"
}

# Create pre-compact checkpoint
create_pre_compact_checkpoint() {
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local checkpoint_file="$CHECKPOINT_DIR/cp-precompact-$timestamp.md"

    log "Creating pre-compact checkpoint..."

    # Build checkpoint content
    cat > "$PRE_COMPACT_FILE" << EOF
# Pre-Compact State: $(date -Iseconds)

## Context
This checkpoint was created automatically before context compaction.
Use this to restore context after compaction.

## Timestamp
- Created: $(date -Iseconds)
- Reason: Pre-compact automatic save

## Session State
EOF

    # Append session state if exists
    if [ -f "$SESSION_FILE" ]; then
        echo "" >> "$PRE_COMPACT_FILE"
        cat "$SESSION_FILE" >> "$PRE_COMPACT_FILE"
    else
        echo "No active session state file" >> "$PRE_COMPACT_FILE"
    fi

    # Add git state
    if [ -d ".git" ]; then
        echo "" >> "$PRE_COMPACT_FILE"
        echo "## Git State" >> "$PRE_COMPACT_FILE"
        echo '```' >> "$PRE_COMPACT_FILE"
        git branch --show-current >> "$PRE_COMPACT_FILE" 2>/dev/null || echo "Unknown branch" >> "$PRE_COMPACT_FILE"
        git status --short >> "$PRE_COMPACT_FILE" 2>/dev/null || echo "No changes" >> "$PRE_COMPACT_FILE"
        git log -3 --oneline >> "$PRE_COMPACT_FILE" 2>/dev/null || echo "No commits" >> "$PRE_COMPACT_FILE"
        echo '```' >> "$PRE_COMPACT_FILE"
    fi

    # Copy to checkpoint
    cp "$PRE_COMPACT_FILE" "$checkpoint_file"

    success "Pre-compact checkpoint: $checkpoint_file"
}

# Extract key context from conversation
# Note: This would need to be enhanced with actual conversation access
extract_key_context() {
    log "Extracting key context..."

    # Add context extraction logic here
    # This is a placeholder - actual implementation would need
    # access to conversation history or session context

    echo "" >> "$PRE_COMPACT_FILE"
    echo "## Key Context" >> "$PRE_COMPACT_FILE"
    echo "<!-- Add conversation summary here if accessible -->" >> "$PRE_COMPACT_FILE"
}

# Create handoff-ready summary
create_handoff_summary() {
    local handoff_file="$CLAUDE_DIR/handoff-pending.md"

    if [ -f "$SESSION_FILE" ]; then
        log "Creating handoff-ready summary..."

        cat > "$handoff_file" << EOF
# Handoff Artifact (Auto-Generated)

## Context
This handoff was auto-generated before context compaction.
Review and complete before context reset.

## Session Summary
[Auto-generated - needs review]

## Completed Work
[From session state]

## Current State
[From session state]

## Next Immediate Step
[From session state]

## Key Decisions
[From session state]

## Open Questions
[From session state]

## Commands to Resume
\`\`\`bash
# Resume from pre-compact checkpoint
/resume precompact-$(date +%Y%m%d-%H%M%S)
\`\`\`

---
Generated: $(date -Iseconds)
Status: DRAFT - needs completion
EOF

        warn "Handoff draft created: $handoff_file"
        log "Complete handoff details before context reset"
    fi
}

# Main execution
main() {
    log "Preparing for context compaction..."
    echo ""

    # Ensure directories
    ensure_dirs

    # Create checkpoint
    create_pre_compact_checkpoint

    # Extract context
    extract_key_context

    # Create handoff draft if there's active work
    if [ -f "$SESSION_FILE" ] && grep -q "Status: in_progress" "$SESSION_FILE"; then
        create_handoff_summary
    fi

    echo ""
    success "Pre-compact preparation complete"
    log "After compaction, run: /resume"

    # Return success
    exit 0
}

# Run main
main "$@"