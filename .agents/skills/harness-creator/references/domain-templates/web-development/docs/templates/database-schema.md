# Database Schema: [Feature/Module Name]

> **Status**: Draft | Review | Approved | Implemented
> **Last Updated**: YYYY-MM-DD

## Overview

[Brief description of the data model and its purpose.]

## Entity Relationship Diagram

```
+-------------+       +-------------+
|   Table1    |       |   Table2    |
+-------------+       +-------------+
| id (PK)     |<----->| id (PK)     |
| field1      |       | table1_id   |
| field2      |       | field1      |
+-------------+       +-------------+
```

## Tables

### [table_name]

**Purpose**: [What this table stores]

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | UUID | No | gen_random_uuid() | Primary key |
| name | VARCHAR(255) | No | - | [Description] |
| status | VARCHAR(50) | No | 'pending' | [Description] |
| created_at | TIMESTAMP | No | NOW() | Creation timestamp |
| updated_at | TIMESTAMP | No | NOW() | Last update timestamp |
| deleted_at | TIMESTAMP | Yes | NULL | Soft delete timestamp |

**Constraints:**

| Name | Type | Columns |
|------|------|---------|
| pk_[table] | PRIMARY KEY | id |
| uq_[table]_name | UNIQUE | name |
| ck_[table]_status | CHECK | status IN ('pending', 'active', 'inactive') |

**Indexes:**

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| idx_[table]_status | status | B-tree | Filter by status |
| idx_[table]_created | created_at | B-tree | Time-based queries |
| idx_[table]_name | name | B-tree | Name lookups |

---

### [related_table]

**Purpose**: [What this table stores]

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | UUID | No | gen_random_uuid() | Primary key |
| [table]_id | UUID | No | - | Foreign key to [table] |
| data | JSONB | Yes | '{}' | Flexible data storage |

**Foreign Keys:**

| Name | Columns | References | On Delete |
|------|---------|------------|-----------|
| fk_[table] | [table]_id | [table](id) | CASCADE |

## Migration Plan

### Step 1: Create Tables

```sql
-- Migration: 20260330_1430_create_[feature]_tables

-- Up
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_[table]_status ON [table_name](status);

-- Down
DROP TABLE IF EXISTS [table_name] CASCADE;
```

### Step 2: Data Migration (if applicable)

```sql
-- Migrate existing data
INSERT INTO [new_table] (id, name, status)
SELECT id, name, 'active'
FROM [old_table];
```

### Step 3: Backfill (if applicable)

```sql
-- Backfill default values
UPDATE [table_name] SET status = 'active' WHERE status IS NULL;
```

## Query Patterns

### Primary Access Patterns

| Pattern | Query | Index Used |
|---------|-------|------------|
| Get by ID | `SELECT * FROM [table] WHERE id = $1` | PRIMARY KEY |
| List by status | `SELECT * FROM [table] WHERE status = $1` | idx_[table]_status |
| Search by name | `SELECT * FROM [table] WHERE name ILIKE $1` | idx_[table]_name |

### Performance Considerations

- **High-cardinality columns**: [Columns good for indexing]
- **Low-cardinality columns**: [Columns poor for indexing]
- **Write-heavy tables**: [Tables with many writes - consider index strategy]

## Redis Cache Strategy

### Cache Keys

| Key Pattern | TTL | Purpose |
|-------------|-----|---------|
| `app:[module]:item:{id}` | 1 hour | Single item cache |
| `app:[module]:list:status:{status}` | 5 minutes | List by status |

### Cache Invalidation

| Event | Action |
|-------|--------|
| Item created | Invalidate list caches |
| Item updated | Invalidate item cache |
| Item deleted | Invalidate item and list caches |

## Backup and Recovery

- **Backup frequency**: Daily full backup, hourly incremental
- **Retention**: 30 days
- **Recovery time objective**: 1 hour
- **Recovery point objective**: 1 hour

## Security Considerations

- **Sensitive columns**: [List any columns with sensitive data]
- **Encryption**: [Encryption strategy for sensitive data]
- **Access control**: [Row-level security if applicable]