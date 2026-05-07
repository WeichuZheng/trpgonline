# Database Schema Template

> Template for documenting database table schemas and migrations.

---

## Schema: [Table Name]

**Version**: 1.0
**Last Updated**: [Date]
**Author**: [Author]
**Migration ID**: [Alembic revision ID]

---

## Overview

[2-3 sentence description of what this table stores]

## Table Definition

### Columns

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTO | Primary key |
| name | VARCHAR(100) | No | - | [Description] |
| email | VARCHAR(255) | No | - | [Description] |
| status | VARCHAR(20) | No | 'active' | [Description] |
| created_at | TIMESTAMP | No | NOW() | Creation timestamp |
| updated_at | TIMESTAMP | No | NOW() | Update timestamp |

### Constraints

| Constraint | Type | Columns | Description |
|------------|------|---------|-------------|
| pk_[table] | PRIMARY KEY | id | Primary key |
| uq_[table]_email | UNIQUE | email | Unique email |
| fk_[table]_user | FOREIGN KEY | user_id | References users.id |

### Indexes

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| ix_[table]_email | email | BTREE | Email lookup |
| ix_[table]_created | created_at | BTREE | Time-based queries |
| ix_[table]_status | status | BTREE | Status filtering |

---

## Relationships

### Related Tables

| Table | Relationship | Foreign Key | Description |
|-------|--------------|-------------|-------------|
| users | Many-to-One | user_id | [Description] |
| orders | One-to-Many | - | [Description] |

### Entity Relationship Diagram

```
[Table A] --< [Table B] >-- [Table C]

[This table] ---< [Child table]
              >--- [Parent table]
```

---

## Migration

### Create Migration

```python
# migrations/versions/[revision]_add_[table].py
"""Add [table_name] table

Revision ID: [revision]
Revises: [previous_revision]
Create Date: [Date]

"""
from alembic import op
import sqlalchemy as sa

revision = '[revision]'
down_revision = '[previous_revision]'

def upgrade():
    op.create_table(
        '[table_name]',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_[table]_email')
    )
    
    op.create_index('ix_[table]_email', '[table_name]', ['email'])
    op.create_index('ix_[table]_created', '[table_name]', ['created_at'])

def downgrade():
    op.drop_index('ix_[table]_created', '[table_name]')
    op.drop_index('ix_[table]_email', '[table_name]')
    op.drop_table('[table_name]')
```

---

## Model Definition

### SQLAlchemy Model

```python
# src/backend/models/[table].py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.backend.models.base import Base

class [ModelName](Base):
    """
    [ModelName] - [Description]
    
    Attributes:
        id: Primary key
        name: [Description]
        email: [Description]
        status: [Description]
        created_at: Creation timestamp
        updated_at: Update timestamp
    """
    __tablename__ = '[table_name]'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    status = Column(String(20), nullable=False, default='active')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="[table]")
    
    # Indexes
    __table_args__ = (
        Index("ix_[table]_email", "email"),
        Index("ix_[table]_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<[ModelName](id={self.id}, name='{self.name}')>"
```

---

## Repository

### Data Access Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| get_by_id | Get by primary key | id |
| get_by_email | Get by email | email |
| list | Paginated list | page, limit, filters |
| create | Insert new row | data dict |
| update | Update existing | id, data dict |
| delete | Delete row | id |

---

## Query Patterns

### Common Queries

```sql
-- Get by ID
SELECT * FROM [table] WHERE id = ?;

-- Get by email
SELECT * FROM [table] WHERE email = ?;

-- List with pagination
SELECT * FROM [table]
ORDER BY created_at DESC
LIMIT ? OFFSET ?;

-- Count total
SELECT COUNT(*) FROM [table];

-- Filter by status
SELECT * FROM [table] WHERE status = ?;

-- Search by name
SELECT * FROM [table] WHERE name LIKE ?;
```

---

## Performance Considerations

### Query Optimization

| Query | Optimization | Notes |
|-------|--------------|-------|
| Get by email | Index ix_[table]_email | O(log n) |
| List by date | Index ix_[table]_created | O(log n) for ORDER BY |
| Filter by status | Index ix_[table]_status | O(log n) |

### Estimated Row Counts

| Scenario | Expected Rows |
|----------|---------------|
| Initial | 0 |
| After 1 year | ~100,000 |
| After 5 years | ~500,000 |

---

## Data Integrity

### Validation Rules

| Field | Validation |
|-------|------------|
| email | Valid email format, unique |
| name | 1-100 characters, no special chars |
| status | Enum: active, inactive, pending |

### Business Rules

- [Rule 1: description]
- [Rule 2: description]

---

## Backup Strategy

| Strategy | Frequency | Retention |
|----------|-----------|-----------|
| Full backup | Daily | 30 days |
| Incremental | Hourly | 7 days |
| Archive | Monthly | 1 year |

---

## Notes

[Any additional schema notes or considerations]