#!/bin/bash
#
# validate-commit.sh - Pre-commit validation hook
# Blocks commits containing secrets, missing API validation, or unsafe patterns
#
# Usage: ./validate-commit.sh [--staged] [files...]
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

if [ -z "$FILES" ]; then
    echo -e "${GREEN}No files to validate.${NC}"
    exit 0
fi

echo "=== Commit Validation ==="
echo "Checking $(echo "$FILES" | wc -l) file(s)..."
echo ""

# =============================================================================
# Pattern Definitions
# =============================================================================

# Secret patterns (high severity - always block)
SECRET_PATTERNS=(
    # API Keys
    'api[_-]?key\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    'apikey\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    'API[_-]?KEY\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    # AWS Keys
    'AKIA[0-9A-Z]{16}'
    'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["'"'"']?[a-zA-Z0-9/+=]{40}'
    # Passwords
    'password\s*[=:]\s*["'"'"']?[^\s"'"'"']{8,}'
    'passwd\s*[=:]\s*["'"'"']?[^\s"'"'"']{8,}'
    'pwd\s*[=:]\s*["'"'"']?[^\s"'"'"']{8,}'
    # Tokens
    'auth[_-]?token\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-\.]{20,}'
    'access[_-]?token\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-\.]{20,}'
    'refresh[_-]?token\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-\.]{20,}'
    'bearer\s+[a-zA-Z0-9_\-\.]{20,}'
    # Secrets
    'client[_-]?secret\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    'secret[_-]?key\s*[=:]\s*["'"'"']?[a-zA-Z0-9_\-]{20,}'
    # JWT tokens
    'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'
    # Private keys
    '-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----'
    # Database URLs with credentials
    'mongodb(\+srv)?://[^:]+:[^@]+@'
    'postgres(ql)?://[^:]+:[^@]+@'
    'mysql://[^:]+:[^@]+@'
    'redis://[^:]*:[^@]+@'
)

# Docker :latest tag pattern
LATEST_PATTERN='image:\s*[a-zA-Z0-9./_-]+:latest'
FROM_LATEST_PATTERN='FROM\s+[a-zA-Z0-9./_-]+:latest'

# API validation patterns - detect routes without validation
API_ROUTE_PATTERNS=(
    '@app\.route\('
    '@router\.(get|post|put|delete|patch)\('
    'app\.(get|post|put|delete|patch)\('
    'router\.(get|post|put|delete|patch)\('
    '@GetMapping'
    '@PostMapping'
    '@PutMapping'
    '@DeleteMapping'
    '@RequestMapping'
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

    # Check each secret pattern
    for pattern in "${SECRET_PATTERNS[@]}"; do
        if echo "$content" | grep -qiE "$pattern"; then
            echo -e "${RED}BLOCKED: Potential secret detected in $file${NC}"
            echo "  Pattern matched: $pattern"
            echo "  Line: $(echo "$content" | grep -iE "$pattern" | head -1)"
            ((ERRORS++))
            return 1
        fi
    done

    return 0
}

check_docker_latest() {
    local file="$1"

    # Only check Dockerfiles and docker-compose files
    if [[ ! "$file" =~ Dockerfile|docker-compose|\.ya?ml$ ]]; then
        return 0
    fi

    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for :latest tag
    if echo "$content" | grep -qiE "$LATEST_PATTERN|$FROM_LATEST_PATTERN"; then
        echo -e "${YELLOW}WARNING: Docker :latest tag detected in $file${NC}"
        echo "  Using :latest is discouraged - use specific version tags"
        echo "  Line: $(echo "$content" | grep -iE "$LATEST_PATTERN|$FROM_LATEST_PATTERN" | head -1)"
        ((WARNINGS++))
    fi

    return 0
}

check_api_validation() {
    local file="$1"

    # Only check backend files
    if [[ ! "$file" =~ \.py$|\.js$|\.ts$|\.java$|\.go$ ]]; then
        return 0
    fi

    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for API route definitions
    local has_routes=false
    for pattern in "${API_ROUTE_PATTERNS[@]}"; do
        if echo "$content" | grep -qE "$pattern"; then
            has_routes=true
            break
        fi
    done

    if [ "$has_routes" = false ]; then
        return 0
    fi

    # Check for validation patterns
    local has_validation=false
    if echo "$content" | grep -qE "(pydantic|marshmallow|@validate|validator|validation|schema|zod|joi|class-validator)"; then
        has_validation=true
    fi

    # Check for explicit validation decorators/annotations
    if echo "$content" | grep -qE "(Body\(|Query\(|Param\(|@Valid|@Validated|validate_request|validate\(,request\.validate)"; then
        has_validation=true
    fi

    if [ "$has_routes" = true ] && [ "$has_validation" = false ]; then
        echo -e "${YELLOW}WARNING: API route(s) in $file may lack input validation${NC}"
        echo "  Consider adding validation (pydantic, marshmallow, zod, class-validator, etc.)"
        ((WARNINGS++))
    fi

    return 0
}

check_hardcoded_urls() {
    local file="$1"

    # Skip config files
    if [[ "$file" =~ config|settings|\.env ]]; then
        return 0
    fi

    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        return 0
    fi

    # Check for hardcoded URLs in source code (not localhost/example.com)
    if echo "$content" | grep -qE '(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'; then
        local urls
        urls=$(echo "$content" | grep -oE '(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | grep -v 'localhost\|example\.com\|test\.com\|127\.0\.0\.1')

        if [ -n "$urls" ]; then
            echo -e "${YELLOW}WARNING: Hardcoded URL(s) found in $file${NC}"
            echo "  Consider using environment variables for URLs"
            echo "  URLs: $urls"
            ((WARNINGS++))
        fi
    fi

    return 0
}

# =============================================================================
# Main Validation Loop
# =============================================================================

for file in $FILES; do
    # Skip deleted files
    [ ! -f "$file" ] && continue

    # Skip binary files
    if file "$file" 2>/dev/null | grep -q "binary"; then
        continue
    fi

    # Skip lock files and generated files
    if [[ "$file" =~ lock$|\.min\.|dist/|node_modules/|__pycache__|\.pyc$|target/ ]]; then
        continue
    fi

    # Run all checks
    check_secrets "$file"
    check_docker_latest "$file"
    check_api_validation "$file"
    check_hardcoded_urls "$file"
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

echo -e "${GREEN}All checks passed!${NC}"
exit 0