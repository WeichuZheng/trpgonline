#!/bin/bash
# Dev Squad PostToolUse hook: Validates database migration files
# Runs after Write/Edit on migrations/
# Exit 0 = OK

# Find the most recently modified migration file
LATEST_MIGRATION=$(find migrations -type f -name "*.py" -o -name "*.sql" 2>/dev/null | xargs ls -t 2>/dev/null | head -1)

if [ -z "$LATEST_MIGRATION" ]; then
    exit 0
fi

WARNINGS=""

# Check for naming convention: YYYYMMDD_HHMM_description.py or V{num}__description.sql
BASENAME=$(basename "$LATEST_MIGRATION")
if ! echo "$BASENAME" | grep -qE '^[0-9]{8}_[0-9]{4}_.+\.py$|^[vV][0-9]+__.*\.sql$'; then
    WARNINGS="$WARNINGS\n- Non-standard naming. Use: YYYYMMDD_HHMM_description.py or V{num}__description.sql"
fi

# Check for rollback function/documentation
if ! grep -qiE '(rollback|down|reverse|def down)' "$LATEST_MIGRATION" 2>/dev/null; then
    WARNINGS="$WARNINGS\n- Missing rollback function or documentation"
fi

# Check for index documentation if creating indexes
if grep -qiE 'CREATE INDEX|create index' "$LATEST_MIGRATION" 2>/dev/null; then
    if ! grep -qiE 'performance|impact|query|purpose' "$LATEST_MIGRATION" 2>/dev/null; then
        WARNINGS="$WARNINGS\n- Index created without performance documentation"
    fi
fi

# Check for foreign key cascade behavior
if grep -qiE 'FOREIGN KEY|REFERENCES' "$LATEST_MIGRATION" 2>/dev/null; then
    if ! grep -qiE 'ON DELETE|on delete' "$LATEST_MIGRATION" 2>/dev/null; then
        WARNINGS="$WARNINGS\n- Foreign key without explicit ON DELETE behavior"
    fi
fi

if [ -n "$WARNINGS" ]; then
    echo "=== Migration Review: $BASENAME ===" >&2
    echo -e "$WARNINGS" >&2
    echo "=====================================" >&2
fi

exit 0