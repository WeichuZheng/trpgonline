# Database Code Rule

**Path Scope:** `src/backend/models/**/*.py`, `src/backend/repository/**/*.py`, `migrations/**/*.py`

**Severity:** STANDARD

---

## Rule: Database Code Standards

All database-related code (models, repositories, migrations) must follow these standards.

---

## Model Structure

### File Organization

```
src/backend/
├── models/              # SQLAlchemy models
│   ├── user.py          # User model
│   ├── order.py         # Order model
│   └── base.py          # Base model class
│   └── __init__.py      # Model exports
├── repository/          # Data access layer
│   ├── user_repository.py
│   ├── order_repository.py
│   └── base_repository.py
│   └── __init__.py
migrations/              # Alembic migrations
├── versions/
│   ├── 001_initial.py
│   ├── 002_add_orders.py
```

### Model Template

```python
# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from src.backend.models.base import Base

class User(Base):
    """
    User model for storing user accounts.
    
    Attributes:
        id: Primary key
        email: Unique email address
        password: Hashed password
        name: User display name
        is_active: Account active status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user", lazy="dynamic")
    
    # Indexes
    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
```

---

## Repository Pattern

### Repository Template

```python
# repository/user_repository.py
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.backend.models.user import User
from src.backend.repository.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    Repository for User data access.
    
    Handles:
    - CRUD operations
    - Query helpers
    - Pagination
    
    Does NOT:
    - Business logic (that's service)
    - HTTP handling (that's routes)
    """
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    async def get_by_id(self, id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == id).first()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    async def exists_by_email(self, email: str) -> bool:
        """Check if email exists."""
        return self.db.query(User).filter(User.email == email).count() > 0
    
    async def list(
        self, 
        page: int = 1, 
        limit: int = 20,
        filters: dict = None
    ) -> Tuple[List[User], int]:
        """
        List users with pagination.
        
        Returns tuple of (users, total_count).
        """
        query = self.db.query(User)
        
        # Apply filters
        if filters:
            if filters.get('is_active'):
                query = query.filter(User.is_active == filters['is_active'])
        
        # Count total
        total = query.count()
        
        # Paginate
        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()
        
        return users, total
    
    async def create(self, data: dict) -> User:
        """Create new user."""
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def update(self, id: int, data: dict) -> Optional[User]:
        """Update user."""
        user = await self.get_by_id(id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def delete(self, id: int) -> bool:
        """Delete user."""
        user = await self.get_by_id(id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
```

---

## Migration Standards

### Migration Template

```python
# migrations/versions/001_initial.py
"""Initial migration

Revision ID: 001
Revises: None
Create Date: 2024-01-01

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])

def downgrade():
    # Drop indexes first
    op.drop_index('ix_users_created_at', 'users')
    op.drop_index('ix_users_email', 'users')
    
    # Drop table
    op.drop_table('users')
```

### Migration Best Practices

1. **Always Reversible**: Every upgrade must have a downgrade
2. **Small Steps**: Each migration should be minimal
3. **No Data Loss**: Downgrade should restore previous state
4. **Test Both Directions**: Run upgrade AND downgrade in staging
5. **Document Changes**: Clear revision description

---

## Query Optimization

### Index Strategy

```python
# Index on query columns
email = Column(String(255), index=True)  # queried often
created_at = Column(DateTime, index=True)  # for sorting

# Composite index for common queries
__table_args__ = (
    Index("ix_users_email_active", "email", "is_active"),
)
```

### Avoid N+1 Queries

```python
# BAD - N+1 query
for order in orders:
    user = db.query(User).filter(User.id == order.user_id).first()
    print(user.name)

# GOOD - Join or eager load
orders = db.query(Order).options(joinedload(Order.user)).all()
for order in orders:
    print(order.user.name)

# GOOD - Bulk fetch
user_ids = [o.user_id for o in orders]
users = db.query(User).filter(User.id.in_(user_ids)).all()
user_map = {u.id: u for u in users}
for order in orders:
    print(user_map[order.user_id].name)
```

---

## Connection Management

### Environment Variables

```python
# GOOD - From environment
import os
DATABASE_URL = os.environ.get("DATABASE_URL")

# BAD - Hardcoded
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### Session Management

```python
# Using dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In route
@router.get("/users")
async def list_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return await service.list()
```

---

## Testing Models

### Model Test Template

```python
# tests/models/user_test.py
import pytest
from src.backend.models.user import User

def test_user_creation():
    user = User(
        email="test@example.com",
        password="hashed",
        name="Test User"
    )
    assert user.email == "test@example.com"
    assert user.is_active == True  # default

def test_user_repr():
    user = User(id=1, email="test@example.com")
    assert "id=1" in repr(user)
    assert "test@example.com" in repr(user)
```

---

## Anti-Patterns to Avoid

1. **Missing Indexes**: Index query columns
2. **N+1 Queries**: Use joins/eager loading
3. **Hardcoded URLs**: Use environment
4. **Non-Reversible Migrations**: Always provide downgrade
5. **Logic in Models**: Keep in services
6. **Missing Constraints**: Add foreign keys, unique
7. **Large Transactions**: Keep small
8. **No Testing**: Test migrations and queries