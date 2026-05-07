#!/bin/bash
#
# validate-api.sh - Pre-commit validation hook for API code
# Validates backend API files for validation, security, and patterns
#
# Usage: ./validate-api.sh [--staged] [files...]
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

# Filter to backend API files only
FILES=$(echo "$FILES" | grep -E "^src/backend/.*\.py$" || true)

if [ -z "$FILES" ]; then
    echo -e "${GREEN}No backend API files to validate.${NC}"
    exit 0
fi

echo "=== API Validation ==="
echo "Checking $(echo "$FILES" | wc -l) backend file(s)..."
echo ""

# =============================================================================
# Pattern Definitions
# =============================================================================

# Secret patterns (critical - always block)
SECRET_PATTERNS=(
    'api[_-]?key\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    'password\s*[=:]\s*["'"'"']?[^\s"'"'"']{8,}'
    'secret[_-]?key\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    'token\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-\.]{20,}'
    'DATABASE_URL\s*[=:]\s*["'"'"']?.*:.+@'
)

# Route patterns
ROUTE_PATTERNS=(
    '@app\.route\('
    '@router\.(get|post|put|delete|patch)\('
    'app\.(get|post|put|delete|patch)\('
    'router\.(get|post|put|delete|patch)\('
)

# Validation patterns
VALIDATION_PATTERNS=(
    'pydantic'
    'BaseModel'
    '@validate'
    'validator'
    'marshmallow'
    'Schema'
)

# Auth patterns
AUTH_PATTERNS=(
    'Depends\(get_current_user\)'
    'Depends\(auth\)'
    '@login_required'
    'authentication'
    'Authorization'
)

# =============================================================================
# Helper Functions
# =============================================================================

check_secrets() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    for pattern in "${SECRET_PATTERNS[@]}"; do
        if echo "$content" | grep -qiE "$pattern"; then
            echo -e "${RED}BLOCKED: Potential secret detected in $file${NC}"
            echo "  Pattern matched: $pattern"
            echo "  Use environment variables instead"
            ((ERRORS++))
            return 1
        fi
    done

    return 0
}

check_validation() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for route definitions
    local has_routes=false
    for pattern in "${ROUTE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            has_routes=true
            break
        fi
    done

    if [ "$has_routes" = false ]; then
        return 0
    fi

    # Check for validation
    local has_validation=false
    for pattern in "${VALIDATION_PATTERNS[@]}"; do
        if echo "$content" | grep -qiE "$pattern"; then
            has_validation=true
            break
        fi
    done

    if [ "$has_routes" = true ] && [ "$has_validation" = false ]; then
        echo -e "${YELLOW}WARNING: Route(s) in $file may lack input validation${NC}"
        echo "  Add Pydantic models or validation decorators"
        ((WARNINGS++))
    fi

    return 0
}

check_auth() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for route definitions
    local has_routes=false
    for pattern in "${ROUTE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            has_routes=true
            break
        fi
    done

    if [ "$has_routes" = false ]; then
        return 0
    fi

    # Check if routes handle auth (or if file is explicitly public)
    local has_auth=false
    local is_public=false

    for pattern in "${AUTH_PATTERNS[@]}"; do
        if echo "$content" | grep -qiE "$pattern"; then
            has_auth=true
            break
        fi
    done

    # Check if file indicates public endpoints
    if echo "$content" | grep -qiE 'public|allow_anonymous|skip_auth|no_auth'; then
        is_public=true
    fi

    if [ "$has_routes" = true ] && [ "$has_auth" = false ] && [ "$is_public" = false ]; then
        echo -e "${YELLOW}WARNING: Routes in $file may lack authentication${NC}"
        echo "  Add authentication dependency or mark as public"
        ((WARNINGS++))
    fi

    return 0
}

check_error_handling() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for HTTPException or error handling
    if echo "$content" | grep -qE 'HTTPException|raise_http|error_response'; then
        return 0
    fi

    # Check for routes without error handling
    local has_routes=false
    for pattern in "${ROUTE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            has_routes=true
            break
        fi
    done

    if [ "$has_routes" = true ]; then
        if ! echo "$content" | grep -qE 'try:|except|HTTPException|raise'; then
            echo -e "${YELLOW}INFO: Routes in $file may need error handling${NC}"
            echo "  Consider adding try/except or HTTPException"
        fi
    fi

    return 0
}

check_sql_injection() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for raw SQL with string formatting (dangerous)
    if echo "$content" | grep -qE 'execute\s*\(\s*f["'"'"']|execute\s*\(\s*["'"'"'].*\+|raw\s*sql'; then
        echo -e "${RED}BLOCKED: Potential SQL injection in $file${NC}"
        echo "  Use parameterized queries or ORM instead"
        ((ERRORS++))
        return 1
    fi

    return 0
}

check_docstrings() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for route definitions
    local has_routes=false
    for pattern in "${ROUTE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            has_routes=true
            break
        fi
    done

    if [ "$has_routes" = false ]; then
        return 0
    fi

    # Check for docstrings on routes
    local route_count=$(echo "$content" | grep -cE "${ROUTE_PATTERNS[*]}")
    local docstring_count=$(echo "$content" | grep -cE '"""|\'\'\'' || echo "0")

    if [ "$route_count" -gt 0 ] && [ "$docstring_count" -lt "$route_count" ]; then
        echo -e "${YELLOW}INFO: Some routes in $file lack docstrings${NC}"
        echo "  Add docstrings for API documentation"
    fi

    return 0
}

# =============================================================================
# Main Validation Loop
# =============================================================================

for file in $FILES; do
    # Skip deleted files
    [ ! -f "$file" ] && continue

    # Skip test files for some checks
    if [[ "$file" =~ test|tests ]]; then
        check_secrets "$file"
        continue
    fi

    echo "Checking: $file"

    # Run all checks
    check_secrets "$file" || continue
    check_sql_injection "$file" || continue
    check_validation "$file"
    check_auth "$file"
    check_error_handling "$file"
    check_docstrings "$file"
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

echo -e "${GREEN}All API checks passed!${NC}"
exit 0