#!/bin/bash
# Session Stop Hook
# Called when a Claude Code session ends
# Purpose: Log session accomplishments, save state, cleanup

set -e

# Configuration
CLAUDE_DIR=".claude"
CHECKPOINT_DIR="$CLAUDE_DIR/checkpoints"
SESSION_FILE="$CLAUDE_DIR/session-state.md"
SESSION_LOG="$CLAUDE_DIR/session-logs"
FINAL_CHECKPOINT="$CLAUDE_DIR/checkpoint.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${BLUE}[session-stop]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[session-stop]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[session-stop]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[session-stop]${NC} $1"
}

# Ensure directories exist
ensure_dirs() {
    mkdir -p "$CHECKPOINT_DIR"
    mkdir -p "$SESSION_LOG"
}

# Get session info
get_session_info() {
    if [ -f "$SESSION_FILE" ]; then
        # Extract session ID
        SESSION_ID=$(grep "Session ID:" "$SESSION_FILE" | cut -d: -f2 | tr -d ' ' || echo "unknown")
        # Extract start time
        START_TIME=$(grep "Started:" "$SESSION_FILE" | cut -d: -f2- | tr -d ' ' || echo "unknown")
    else
        SESSION_ID="session-$(date +%Y%m%d-%H%M%S)"
        START_TIME=$(date -Iseconds)
    fi
}

# Create session checkpoint
create_checkpoint() {
    log "Creating session checkpoint..."

    local timestamp=$(date +%Y%m%d-%H%M%S)
    local checkpoint_file="$CHECKPOINT_DIR/cp-$timestamp.md"

    # Copy session state to checkpoint
    if [ -f "$SESSION_FILE" ]; then
        cat > "$checkpoint_file" << EOF
# Checkpoint: $(date -Iseconds)

## Session Info
- Session ID: $SESSION_ID
- Started: $START_TIME
- Saved: $(date -Iseconds)

EOF
        # Append session state
        cat "$SESSION_FILE" >> "$checkpoint_file"

        # Add git state
        if [ -d ".git" ]; then
            echo "" >> "$checkpoint_file"
            echo "## Git State" >> "$checkpoint_file"
            echo "\`\`\`" >> "$checkpoint_file"
            git status --short >> "$checkpoint_file" 2>/dev/null || echo "Unable to get git status" >> "$checkpoint_file"
            echo "\`\`\`" >> "$checkpoint_file"
        fi

        # Update main checkpoint
        cp "$checkpoint_file" "$FINAL_CHECKPOINT"

        success "Checkpoint saved: $checkpoint_file"
    else
        warn "No session state file found, creating minimal checkpoint"
        echo "# Checkpoint: $(date -Iseconds)" > "$FINAL_CHECKPOINT"
        echo "No active session state to save" >> "$FINAL_CHECKPOINT"
    fi
}

# Log session summary
log_session() {
    local log_file="$SESSION_LOG/session-$SESSION_ID.log"

    log "Logging session summary..."

    cat > "$log_file" << EOF
# Session Log: $SESSION_ID

## Timestamps
- Started: $START_TIME
- Ended: $(date -Iseconds)

## Session State
EOF

    if [ -f "$SESSION_FILE" ]; then
        echo "" >> "$log_file"
        cat "$SESSION_FILE" >> "$log_file"
    fi

    if [ -d ".git" ]; then
        echo "" >> "$log_file"
        echo "## Git State at End" >> "$log_file"
        echo '```' >> "$log_file"
        git log -1 --oneline >> "$log_file" 2>/dev/null || echo "No commits" >> "$log_file"
        git status --short >> "$log_file" 2>/dev/null || echo "No changes" >> "$log_file"
        echo '```' >> "$log_file"
    fi

    success "Session log: $log_file"
}

# Prompt for handoff if needed
check_handoff_need() {
    # Check if there's active work that might need handoff
    if [ -f "$SESSION_FILE" ]; then
        if grep -q "Status: in_progress\|Status: blocked" "$SESSION_FILE"; then
            warn "Active work detected in session state"
            log "Consider creating a handoff artifact: /checkpoint with handoff option"
        fi
    fi
}

# Cleanup old checkpoints (keep last 5)
cleanup_old_checkpoints() {
    local count=$(ls -1 "$CHECKPOINT_DIR"/cp-*.md 2>/dev/null | wc -l)

    if [ "$count" -gt 5 ]; then
        log "Cleaning up old checkpoints (keeping last 5)..."
        ls -1t "$CHECKPOINT_DIR"/cp-*.md | tail -n +6 | xargs rm -f 2>/dev/null || true
    fi
}

# Main execution
main() {
    log "Session ending..."
    echo ""

    # Ensure directories
    ensure_dirs

    # Get session info
    get_session_info

    log "Session ID: $SESSION_ID"

    # Create checkpoint
    create_checkpoint

    # Log session
    log_session

    # Check for handoff need
    check_handoff_need

    # Cleanup
    cleanup_old_checkpoints

    echo ""
    success "Session cleanup complete"
    log "Session checkpoint available for next session: /resume"
}

# Run main
main "$@"