#!/bin/bash
#
# validate-frontend.sh - Pre-commit validation hook for frontend code
# Validates frontend files for design system compliance, accessibility, and patterns
#
# Usage: ./validate-frontend.sh [--staged] [files...]
# Exit codes: 0 = pass, 1 = block, 2 = warning only
#

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Get list of files to check
if [ "$1" = "--staged" ]; then
    shift
    FILES=$(git diff --cached --name-only --diff-filter=ACM "$@")
else
    FILES="$@"
fi

# Filter to frontend files only
FILES=$(echo "$FILES" | grep -E "^src/frontend/.*\.(jsx?|tsx?|css|scss)$" || true)

if [ -z "$FILES" ]; then
    echo -e "${GREEN}No frontend files to validate.${NC}"
    exit 0
fi

echo "=== Frontend Validation ==="
echo "Checking $(echo "$FILES" | wc -l) frontend file(s)..."
echo ""

# =============================================================================
# Pattern Definitions
# =============================================================================

# Inline style patterns (warning)
INLINE_STYLE_PATTERNS=(
    'style=\{'
    'style={{'
)

# Hardcoded color patterns (warning)
HARDCODED_COLOR_PATTERNS=(
    'color:\s*["'"'"']#[0-9a-fA-F]{3,6}'
    'backgroundColor:\s*["'"'"']#[0-9a-fA-F]{3,6}'
    'color:\s*["'"'"']rgb'
    'color:\s*["'"'"']hsl'
)

# Missing accessibility patterns (warning)
ACCESSIBILITY_PATTERNS=(
    # Images without alt
    '<img[^>]*(?![^>]*alt=)[^>]*>'
    # Buttons without aria-label (icon buttons)
    '<button[^>]*>\s*<[^>]*>\s*</button>'
    # Input without label association
    '<input[^>]*(?![^>]*(aria-label|id=))[^>]*>'
)

# Console.log in production code (warning)
CONSOLE_PATTERN='console\.(log|debug|info|warn|error)'

# =============================================================================
# Helper Functions
# =============================================================================

check_inline_styles() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    for pattern in "${INLINE_STYLE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            echo -e "${YELLOW}WARNING: Inline styles detected in $file${NC}"
            echo "  Consider using design system tokens or styled components"
            ((WARNINGS++))
        fi
    done

    return 0
}

check_hardcoded_colors() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    for pattern in "${HARDCODED_COLOR_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            echo -e "${YELLOW}WARNING: Hardcoded color in $file${NC}"
            echo "  Use design system color tokens instead"
            ((WARNINGS++))
        fi
    done

    return 0
}

check_accessibility() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check images without alt
    if echo "$content" | grep -qE '<img[^>]+(?![^>]*alt=)[^>]*/?>'; then
        echo -e "${YELLOW}WARNING: Image without alt attribute in $file${NC}"
        echo "  Add alt attribute for accessibility"
        ((WARNINGS++))
    fi

    return 0
}

check_console_logs() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Skip test files
    if [[ "$file" =~ test|spec|\.test\.|\.spec\. ]]; then
        return 0
    fi

    if echo "$content" | grep -qE "$CONSOLE_PATTERN"; then
        echo -e "${YELLOW}WARNING: console.log detected in $file${NC}"
        echo "  Remove before production or use proper logging"
        ((WARNINGS++))
    fi

    return 0
}

check_import_order() {
    local file="$1"

    # Only check TypeScript/JavaScript files
    if [[ ! "$file" =~ \.(jsx?|tsx?)$ ]]; then
        return 0
    fi

    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for import order: external -> internal -> relative
    # This is a simplified check
    local imports
    imports=$(echo "$content" | grep -E "^import " | head -20)

    # Check if React import is first (common convention)
    if echo "$imports" | grep -qE "^import.*from ['\"]react['\"]"; then
        local first_import
        first_import=$(echo "$imports" | head -1)
        if ! echo "$first_import" | grep -qE "from ['\"]react['\"]"; then
            echo -e "${YELLOW}INFO: React import not first in $file${NC}"
            echo "  Convention: React imports before others"
        fi
    fi

    return 0
}

check_typescript_types() {
    local file="$1"

    # Only check TypeScript files
    if [[ ! "$file" =~ \.tsx?$ ]]; then
        return 0
    fi

    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for explicit 'any' usage (warning)
    if echo "$content" | grep -qE ':\s*any\b'; then
        echo -e "${YELLOW}WARNING: Explicit 'any' type in $file${NC}"
        echo "  Consider using more specific types"
        ((WARNINGS++))
    fi

    return 0
}

# =============================================================================
# Main Validation Loop
# =============================================================================

for file in $FILES; do
    # Skip deleted files
    [ ! -f "$file" ] && continue

    # Skip generated/minified files
    if [[ "$file" =~ \.min\.|dist/|node_modules/ ]]; then
        continue
    fi

    echo "Checking: $file"

    # Run all checks
    check_inline_styles "$file"
    check_hardcoded_colors "$file"
    check_accessibility "$file"
    check_console_logs "$file"
    check_import_order "$file"
    check_typescript_types "$file"
done

# =============================================================================
# Summary
# =============================================================================

echo ""
echo "=== Validation Summary ==="

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}BLOCKED: $ERRORS error(s) found${NC}"
    echo "Please fix the above issues before committing."
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}WARNING: $WARNINGS warning(s) found${NC}"
    echo "Consider addressing these issues, but commit is allowed."
    exit 2
fi

echo -e "${GREEN}All frontend checks passed!${NC}"
exit 0