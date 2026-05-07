# Hook Generator Prompt

> Use this prompt template to generate custom hook scripts for the harness framework.

---

## Input Parameters

When generating a custom hook, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `hook_name` | Unique identifier for the hook (lowercase, hyphen-separated) | Yes |
| `hook_type` | When the hook runs (pre-commit, post-commit, session-start, etc.) | Yes |
| `hook_purpose` | What the hook validates or does | Yes |
| `trigger_points` | Specific events that trigger this hook | Yes |
| `failure_behavior` | What happens when hook fails (block, warn, auto-fix) | Yes |
| `dependencies` | Tools or packages the hook needs | No |
| `config_options` | Configurable options for the hook | No |

---

## Prompt Template

```
You are generating a new Claude Code hook script for the harness framework.

## Hook to Generate

- **Name**: {hook_name}
- **Type**: {hook_type}
- **Purpose**: {hook_purpose}
- **Trigger Points**: {trigger_points}
- **Failure Behavior**: {failure_behavior}
- **Dependencies**: {dependencies}
- **Config Options**: {config_options}

## Your Task

Create a complete hook script following the harness framework conventions.

## Hook Script Structure

1. **Shebang and Metadata**:
   - #!/bin/bash (or appropriate interpreter)
   - Comment header with purpose and usage

2. **Configuration Section**:
   - Configurable variables
   - Default values
   - Color codes for output

3. **Utility Functions**:
   - Logging functions (log, warn, error, success)
   - Helper functions

4. **Main Logic**:
   - Detection/check logic
   - Validation steps
   - Error handling

5. **Exit Codes**:
   - 0 for success
   - Non-zero for failure (with meaningful codes)

## Design Principles

1. **Fail Fast**: Check prerequisites early
2. **Clear Output**: User knows exactly what happened
3. **Configurable**: Allow customization via variables
4. **Idempotent**: Running multiple times has same result
5. **Graceful Degradation**: Handle missing dependencies

## Hook Types

| Type | When It Runs | Common Uses |
|------|-------------|-------------|
| pre-commit | Before git commit | Validation, linting |
| post-commit | After git commit | Notifications, logging |
| pre-push | Before git push | Tests, security checks |
| session-start | When Claude starts | Context loading |
| session-stop | When Claude stops | Cleanup, backup |
| pre-compact | Before context reset | Handoff prep |

Generate the hook script now.
```

---

## Output Format

The generated file should follow this structure:

```bash
#!/bin/bash
# {Hook Name} Hook
# {Brief description of what this hook does}
# Usage: Automatically triggered by {trigger}

set -e  # Exit on error

# Configuration
{CONFIGURABLE_VARIABLES}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Utility functions
log() {
    echo -e "${BLUE}[{hook-name}]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[{hook-name}]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[{hook-name}]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[{hook-name}]${NC} $1"
}

# {Main function name}
{main_function}() {
    {Implementation}
}

# Run main
{main_function} "$@"
```

---

## Quality Checklist

Before finalizing the hook script, verify:

- [ ] **Shebang Present**: Correct interpreter specified
- [ ] **Metadata Complete**: Purpose and usage documented
- [ ] **Error Handling**: All error cases handled
- [ ] **Exit Codes**: Meaningful exit codes (0=success, 1=fail, 2=config error)
- [ ] **Output Clear**: User understands what happened
- [ ] **Configurable**: Key values are variables
- [ ] **Dependencies Checked**: Hook verifies prerequisites
- [ ] **Idempotent**: Safe to run multiple times
- [ ] **Cross-platform**: Works on target platforms (Linux, macOS, Windows)
- [ ] **Performance**: Completes in reasonable time

---

## Hook Type Reference

### Git Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `pre-commit` | Before `git commit` | Validate staged changes |
| `post-commit` | After `git commit` | Trigger CI, notify |
| `pre-push` | Before `git push` | Run tests, security |
| `post-merge` | After `git merge` | Update dependencies |

### Session Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `session-start` | Claude session begins | Load context, check state |
| `session-stop` | Claude session ends | Backup, cleanup |
| `pre-compact` | Context limit reached | Prepare handoff |
| `post-compact` | After context reset | Restore context |

---

## Examples

### Example 1: Pre-commit Lint Hook

**Input:**
```
hook_name: lint-check
hook_type: pre-commit
hook_purpose: Run linters on staged files and block commit if issues found
trigger_points: git commit
failure_behavior: block (non-zero exit)
dependencies: eslint, prettier (or project equivalents)
config_options: LINTER_TYPES (file types to lint), AUTO_FIX (attempt fixes)
```

**Output:**
```bash
#!/bin/bash
# Lint Check Hook
# Runs linters on staged files before commit
# Usage: Automatically triggered by git commit

set -e

# Configuration
LINTER_TYPES="js,jsx,ts,tsx,json,css,md"  # File extensions to lint
AUTO_FIX=false  # Set to true to auto-fix issues
BLOCK_ON_ERROR=true  # Block commit on lint errors

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Utility functions
log() {
    echo -e "${BLUE}[lint-check]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[lint-check]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[lint-check]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[lint-check]${NC} $1"
}

# Check dependencies
check_dependencies() {
    local missing=()

    if ! command -v npm &> /dev/null; then
        missing+=("npm")
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        error "Missing dependencies: ${missing[*]}"
        exit 2
    fi
}

# Get staged files
get_staged_files() {
    git diff --cached --name-only --diff-filter=ACM | \
        grep -E "\.($LINTER_TYPES)$" || true
}

# Run linter on files
lint_files() {
    local files=("$@")
    local has_errors=false

    if [ ${#files[@]} -eq 0 ]; then
        log "No staged files match lint patterns"
        return 0
    fi

    log "Linting ${#files[@]} file(s)..."

    # Check for ESLint
    if [ -f "node_modules/.bin/eslint" ] || [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
        log "Running ESLint..."
        if [ "$AUTO_FIX" = true ]; then
            npx eslint --fix "${files[@]}" 2>&1 || has_errors=true
        else
            npx eslint "${files[@]}" 2>&1 || has_errors=true
        fi
    fi

    # Check for Prettier
    if [ -f "node_modules/.bin/prettier" ] || [ -f ".prettierrc" ]; then
        log "Running Prettier..."
        if [ "$AUTO_FIX" = true ]; then
            npx prettier --write "${files[@]}" 2>&1 || has_errors=true
        else
            npx prettier --check "${files[@]}" 2>&1 || has_errors=true
        fi
    fi

    if [ "$has_errors" = true ]; then
        return 1
    fi

    return 0
}

# Main function
main() {
    log "Starting lint check..."
    echo ""

    # Check dependencies
    check_dependencies

    # Get staged files
    local staged_files
    staged_files=$(get_staged_files)

    if [ -z "$staged_files" ]; then
        success "No lintable files staged"
        exit 0
    fi

    # Run linters
    if lint_files $staged_files; then
        echo ""
        success "All lint checks passed!"
        exit 0
    else
        echo ""
        error "Lint errors found!"
        if [ "$AUTO_FIX" = true ]; then
            warn "Some issues may have been auto-fixed. Review and re-stage if needed."
        else
            log "Run with AUTO_FIX=true to attempt automatic fixes"
        fi
        exit 1
    fi
}

# Run main
main "$@"
```

---

### Example 2: Session Context Hook

**Input:**
```
hook_name: context-restore
hook_type: session-start
hook_purpose: Check for and load saved context from previous session
trigger_points: Claude session start
failure_behavior: warn (continue even if restore fails)
dependencies: none
config_options: AUTO_RESTORE (automatically load context), CONTEXT_FILE (file path)
```

**Output:**
```bash
#!/bin/bash
# Context Restore Hook
# Loads saved context from previous Claude session
# Usage: Automatically triggered on session start

set -e

# Configuration
AUTO_RESTORE=true  # Automatically restore context if found
CONTEXT_FILE=".claude/session-state.md"
HANDOFF_FILE=".claude/handoff.md"
CHECKPOINT_FILE=".claude/checkpoint.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Utility functions
log() {
    echo -e "${BLUE}[context-restore]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[context-restore]${NC} WARNING: $1"
}

error() {
    echo -e "${RED}[context-restore]${NC} ERROR: $1"
}

success() {
    echo -e "${GREEN}[context-restore]${NC} $1"
}

# Check for handoff (context reset)
check_handoff() {
    if [ -f "$HANDOFF_FILE" ]; then
        log "Handoff artifact found"
        return 0
    fi
    return 1
}

# Check for checkpoint
check_checkpoint() {
    if [ -f "$CHECKPOINT_FILE" ]; then
        local age_hours=$((($(date +%s) - $(stat -c %Y "$CHECKPOINT_FILE" 2>/dev/null || stat -f %m "$CHECKPOINT_FILE" 2>/dev/null)) / 3600))
        log "Checkpoint found (${age_hours}h old)"
        return 0
    fi
    return 1
}

# Check for session state
check_session_state() {
    if [ -f "$CONTEXT_FILE" ]; then
        log "Session state found"
        return 0
    fi
    return 1
}

# Display restore options
display_options() {
    echo ""
    log "Context recovery options available:"
    echo "  1. Run /start to see restore options"
    echo "  2. Run /resume to continue last session"
    echo "  3. Run /checkpoint to see checkpoint details"
    echo ""
}

# Main function
main() {
    log "Checking for saved context..."
    echo ""

    local has_context=false

    # Check for various context sources
    if check_handoff; then
        has_context=true
        warn "Handoff artifact detected (context reset occurred)"
    fi

    if check_checkpoint; then
        has_context=true
    fi

    if check_session_state; then
        has_context=true
    fi

    if [ "$has_context" = true ]; then
        display_options
    else
        log "No saved context found. Starting fresh session."
    fi

    exit 0
}

# Run main
main "$@"
```

---

## Anti-Patterns to Avoid

1. **Silent Failures**: Hook fails without informing user
2. **Slow Hooks**: Blocking operations for too long
3. **Hardcoded Paths**: Not respecting project structure
4. **Missing Dependencies**: Not checking for required tools
5. **Verbose Output**: Too much noise in output

---

## Integration Notes

After generating a hook:

1. Save to `.claude/hooks/{hook_name}.sh`
2. Make executable: `chmod +x .claude/hooks/{hook_name}.sh`
3. Register in `settings.json` under appropriate hook type
4. Test with dry-run first
5. Document in project's hook registry