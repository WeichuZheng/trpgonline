#!/bin/bash
# Session Start Hook
# Called when a new Claude Code session begins
# Purpose: Load project context, check for saved progress

set -e

# Configuration
CLAUDE_DIR=".claude"
CHECKPOINT_FILE="$CLAUDE_DIR/checkpoint.md"
HANDOFF_FILE="$CLAUDE_DIR/handoff.md"
SESSION_FILE="$CLAUDE_DIR/session-state.md"
PROJECT_CONTEXT="CLAUDE.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${BLUE}[session-start]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[session-start]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[session-start]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[session-start]${NC} $1"
}

# Create .claude directory if it doesn't exist
ensure_claude_dir() {
    if [ ! -d "$CLAUDE_DIR" ]; then
        mkdir -p "$CLAUDE_DIR"
        mkdir -p "$CLAUDE_DIR/checkpoints"
        log "Created .claude/ directory structure"
    fi
}

# Check for handoff artifact (context reset)
check_handoff() {
    if [ -f "$HANDOFF_FILE" ]; then
        warn "HANDOFF DETECTED"
        log "Context reset handoff found at: $HANDOFF_FILE"
        log "Run /start to load handoff context"
        echo ""
        # Show handoff summary if available
        if grep -q "## Session Summary" "$HANDOFF_FILE"; then
            log "Handoff Summary:"
            sed -n '/## Session Summary/,/## /p' "$HANDOFF_FILE" | head -5
        fi
        return 0
    fi
    return 1
}

# Check for checkpoint
check_checkpoint() {
    if [ -f "$CHECKPOINT_FILE" ]; then
        local checkpoint_time=$(stat -c %Y "$CHECKPOINT_FILE" 2>/dev/null || stat -f %m "$CHECKPOINT_FILE" 2>/dev/null)
        local current_time=$(date +%s)
        local age_seconds=$((current_time - checkpoint_time))
        local age_hours=$((age_seconds / 3600))
        local age_days=$((age_hours / 24))

        warn "CHECKPOINT DETECTED"
        log "Last checkpoint: $CHECKPOINT_FILE"

        if [ $age_days -gt 0 ]; then
            log "Age: $age_days days old"
        elif [ $age_hours -gt 0 ]; then
            log "Age: $age_hours hours old"
        else
            log "Age: less than 1 hour old"
        fi

        log "Run /start or /resume to restore session"
        return 0
    fi
    return 1
}

# Check for project context
check_project_context() {
    if [ -f "$PROJECT_CONTEXT" ]; then
        success "Project context found: $PROJECT_CONTEXT"
        # Extract project name if possible
        if grep -q "^# " "$PROJECT_CONTEXT"; then
            local project_name=$(head -1 "$PROJECT_CONTEXT" | sed 's/^# //')
            log "Project: $project_name"
        fi
    else
        log "No CLAUDE.md found - consider running /onboard-codebase"
    fi
}

# Check git status
check_git_status() {
    if [ -d ".git" ]; then
        local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        local status=$(git status --porcelain 2>/dev/null | wc -l)
        log "Git branch: $branch"
        if [ "$status" -gt 0 ]; then
            log "Uncommitted changes: $status files"
        fi
    fi
}

# Initialize session state file
init_session_state() {
    local session_id=$(date +%Y%m%d-%H%M%S)
    cat > "$SESSION_FILE" << EOF
# Session State

## Session Info
- Session ID: session-$session_id
- Started: $(date -Iseconds)
- Source: $(if [ -f "$HANDOFF_FILE" ]; then echo "handoff"; elif [ -f "$CHECKPOINT_FILE" ]; then echo "checkpoint"; else echo "fresh"; fi)

## Current Task
- Status: initializing
- Description:

## Files in Progress
<!-- Track files being modified -->

## Notes
<!-- Session notes -->

EOF
    log "Initialized session state: $SESSION_FILE"
}

# Main execution
main() {
    log "Session starting..."
    echo ""

    # Ensure directory structure
    ensure_claude_dir

    # Check for saved progress
    local has_saved_progress=false

    if check_handoff; then
        has_saved_progress=true
    elif check_checkpoint; then
        has_saved_progress=true
    fi

    echo ""

    # Check project context
    check_project_context

    # Check git status
    check_git_status

    # Initialize session state
    init_session_state

    echo ""

    if [ "$has_saved_progress" = true ]; then
        log "Saved progress detected. Run /start to restore context."
    else
        log "Fresh session. Ready for new work."
    fi

    success "Session initialization complete"
}

# Run main
main "$@"