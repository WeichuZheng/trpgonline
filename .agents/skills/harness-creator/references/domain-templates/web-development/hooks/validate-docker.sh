#!/bin/bash
# Dev Squad PostToolUse hook: Validates Docker configuration files
# Runs after Write/Edit on Docker files
# Exit 0 = OK, Exit 2 = block with error

# This hook receives the file path as environment context
# For simplicity, we just check the most recent Docker file change

LATEST_DOCKER=$(find . -name "Dockerfile*" -o -name "docker-compose*.yml" -o -name "docker-compose*.yaml" 2>/dev/null | head -1)

if [ -z "$LATEST_DOCKER" ]; then
    exit 0
fi

WARNINGS=""

# Check for :latest tag
if grep -qiE 'image:.*:latest|from.*:latest' "$LATEST_DOCKER" 2>/dev/null; then
    WARNINGS="$WARNINGS\n- Uses :latest image tag (should use specific version)"
fi

# Check for HEALTHCHECK in Dockerfiles
if echo "$LATEST_DOCKER" | grep -qi "Dockerfile"; then
    if ! grep -qiE 'HEALTHCHECK' "$LATEST_DOCKER" 2>/dev/null; then
        WARNINGS="$WARNINGS\n- Missing HEALTHCHECK instruction"
    fi
fi

# Check for secrets in ENV
if grep -qiE 'ENV.*password|ENV.*secret|ENV.*api_key|ENV.*token' "$LATEST_DOCKER" 2>/dev/null; then
    WARNINGS="$WARNINGS\n- Possible secrets in ENV variables (use Docker secrets instead)"
fi

# Check for root user
if echo "$LATEST_DOCKER" | grep -qi "Dockerfile"; then
    if ! grep -qiE 'USER[[:space:]]+[a-z]' "$LATEST_DOCKER" 2>/dev/null; then
        WARNINGS="$WARNINGS\n- No USER instruction (runs as root)"
    fi
fi

if [ -n "$WARNINGS" ]; then
    echo "=== Docker Configuration Review ===" >&2
    echo -e "$WARNINGS" >&2
    echo "====================================" >&2
fi

exit 0