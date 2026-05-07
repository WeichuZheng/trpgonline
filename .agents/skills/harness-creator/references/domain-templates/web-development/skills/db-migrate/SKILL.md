---
name: db-migrate
description: "Guided database migration workflow — from schema design to rollback documentation."
argument-hint: "[migration description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
---

# Database Migration Workflow

Design and document database schema changes with proper rollback support.

---

## Workflow

### Phase 1: Understand the Change

1. Ask the user:
   - "What schema change do you need? (new table, add column, modify data, etc.)"
   - "Is this for a new feature or fixing an existing schema?"
   - "What's the expected data volume?"

2. Check existing schema:
   - Read `models/` for current table definitions
   - Read `migrations/` for recent changes
   - Check for related migrations that might conflict

---

### Phase 2: Design the Migration

1. Propose the migration approach:
   - New table: Show table structure with columns, types, constraints
   - Add column: Show column definition, default value strategy
   - Modify data: Show transformation logic and rollback

2. Ask critical questions:
   - "Should this column be nullable or have a default?"
   - "Do we need an index on this column?"
   - "How should foreign keys behave on delete?"

3. Design rollback:
   - What needs to be reversed?
   - Are there data transformations that can't be rolled back?
   - Document rollback procedure

---

### Phase 3: Create Migration File

Generate migration with proper naming: `YYYYMMDD_HHMM_description.py`

```python
"""
Migration: [Description]

Rollback:
    [Exact commands to reverse this migration]

Performance Impact:
    - [Document any index changes and expected query impact]

Data Migration Notes:
    - [Any data transformation that occurs]
"""

def up(connection):
    """Apply the migration."""
    connection.execute("""
        [SQL commands to apply migration]
    """)

def down(connection):
    """Rollback the migration."""
    connection.execute("""
        [SQL commands to reverse migration]
    """)
```

---

### Phase 4: Review Checklist

Before finalizing, verify:

- [ ] Migration file follows naming convention
- [ ] Rollback function is implemented and tested
- [ ] Foreign keys have documented cascade behavior
- [ ] Indexes documented with query rationale
- [ ] Large table considerations addressed
- [ ] Default values provided for new NOT NULL columns

---

### Phase 5: User Approval

Present the migration and ask:
> "Here's the migration file. Should I write it to `migrations/[filename]`?"

**Important**: Do NOT execute the migration. Only create the file.
User executes: `alembic upgrade head` or equivalent.

---

### Phase 6: Redis Changes (if applicable)

If Redis schema changes are needed:

1. Document key patterns:
   ```
   Key Pattern: app:module:entity:{id}
   Purpose: [What this key stores]
   TTL: [Expiration time]
   ```

2. Document migration strategy:
   - Can old keys coexist with new keys?
   - Do we need a migration script for existing data?

---

## Output

- Migration file in `migrations/`
- Rollback documentation in migration file
- Redis key pattern documentation (if applicable)
- No automatic execution — user must run migration command