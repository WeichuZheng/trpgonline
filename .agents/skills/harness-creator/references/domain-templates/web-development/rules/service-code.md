# Service Code Rule

**Path Scope:** `src/backend/services/**/*.py`

**Severity:** STANDARD

---

## Rule: Service Layer Standards

All service code must follow these standards for separation of concerns, maintainability, and testing.

---

## Service Structure

### File Organization

```
src/backend/services/
├── user_service.py      # User business logic
├── order_service.py     # Order business logic
├── auth_service.py      # Authentication logic
├── email_service.py     # Email sending logic
└── __init__.py          # Service exports
```

### Service Template

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from src.backend.models.user import User
from src.backend.repository.user_repository import UserRepository
from src.backend.utils.security import hash_password, verify_password
from src.backend.exceptions import ValidationError, DuplicateError

class UserService:
    """
    Service for user-related business logic.
    
    Responsibilities:
    - User creation and validation
    - Password hashing
    - Duplicate checking
    - User queries
    
    Does NOT:
    - Handle HTTP requests/responses (that's routes)
    - Directly execute raw SQL (that's repository)
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    async def create(self, data: Dict[str, Any]) -> User:
        """
        Create a new user with validation.
        
        Args:
            data: User data dict with email, password, name
        
        Returns:
            Created User instance
        
        Raises:
            ValidationError: Invalid input
            DuplicateError: Email exists
        """
        # Validate input
        self._validate_create_data(data)
        
        # Check for duplicate
        if await self.repository.exists_by_email(data['email']):
            raise DuplicateError("Email already registered")
        
        # Hash password
        data['password'] = hash_password(data['password'])
        
        # Create via repository
        user = await self.repository.create(data)
        
        return user
    
    async def get(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await self.repository.get_by_id(user_id)
    
    async def list(self, page: int = 1, limit: int = 20) -> tuple[List[User], int]:
        """List users with pagination."""
        return await self.repository.list(page=page, limit=limit)
    
    async def update(self, user_id: int, data: Dict[str, Any]) -> User:
        """Update user with validation."""
        self._validate_update_data(data)
        return await self.repository.update(user_id, data)
    
    async def delete(self, user_id: int) -> bool:
        """Delete user."""
        return await self.repository.delete(user_id)
    
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate user creation data."""
        required = ['email', 'password', 'name']
        for field in required:
            if field not in data or not data[field]:
                raise ValidationError(f"{field} is required")
    
    def _validate_update_data(self, data: Dict[str, Any]) -> None:
        """Validate user update data."""
        if 'password' in data:
            raise ValidationError("Use password_change endpoint")
```

---

## Service Principles

### Single Responsibility

Each service handles ONE domain:

```python
# GOOD - Single responsibility
class UserService:
    # Only user operations
    
class OrderService:
    # Only order operations
    
class PaymentService:
    # Only payment operations

# BAD - Mixed responsibilities
class UserOrderService:
    # Users AND orders - violates SRP
```

### Dependency Injection

```python
class UserService:
    def __init__(self, db: Session, email_service: EmailService = None):
        self.db = db
        self.repository = UserRepository(db)
        self.email_service = email_service or EmailService()
```

### No HTTP Details

Services should NOT know about HTTP:

```python
# BAD - HTTP details in service
class UserService:
    def create(self, request: Request):  # Don't pass Request
        data = request.json()            # Don't parse HTTP
    
# GOOD - Pure data
class UserService:
    def create(self, data: Dict[str, Any]):  # Plain dict
        # Business logic only
```

---

## Error Handling

### Custom Exceptions

```python
# exceptions.py
class ServiceException(Exception):
    """Base service exception."""
    pass

class ValidationError(ServiceException):
    """Validation failed."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field

class DuplicateError(ServiceException):
    """Duplicate resource."""
    pass

class NotFoundError(ServiceException):
    """Resource not found."""
    pass

# Usage in service
async def create(self, data: dict):
    if not data.get('email'):
        raise ValidationError("Email required", field="email")
    
    if await self.repository.exists(data['email']):
        raise DuplicateError("Email already registered")
```

---

## Testing Services

### Unit Test Template

```python
# tests/services/user_service_test.py
import pytest
from unittest.mock import Mock, AsyncMock

from src.backend.services.user_service import UserService
from src.backend.exceptions import ValidationError, DuplicateError

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_repository():
    repo = Mock()
    repo.exists_by_email = AsyncMock(return_value=False)
    repo.create = AsyncMock(return_value=Mock(id=1, email="test@example.com"))
    return repo

@pytest.fixture
def user_service(mock_db, mock_repository):
    service = UserService(mock_db)
    service.repository = mock_repository
    return service

@pytest.mark.asyncio
async def test_create_user_success(user_service):
    data = {"email": "test@example.com", "password": "password", "name": "Test"}
    user = await user_service.create(data)
    assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_create_user_validation_error(user_service):
    data = {"email": "", "password": "password", "name": "Test"}
    with pytest.raises(ValidationError):
        await user_service.create(data)

@pytest.mark.asyncio
async def test_create_user_duplicate(user_service, mock_repository):
    mock_repository.exists_by_email = AsyncMock(return_value=True)
    data = {"email": "existing@example.com", "password": "pass", "name": "Test"}
    with pytest.raises(DuplicateError):
        await user_service.create(data)
```

---

## Inter-Service Communication

### Dependency Pattern

```python
class OrderService:
    def __init__(
        self, 
        db: Session,
        user_service: UserService = None,
        payment_service: PaymentService = None
    ):
        self.db = db
        self.repository = OrderRepository(db)
        self.user_service = user_service or UserService(db)
        self.payment_service = payment_service or PaymentService(db)
    
    async def create_order(self, user_id: int, items: List[dict]):
        # Verify user exists
        user = await self.user_service.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Create order
        order = await self.repository.create_order(user_id, items)
        
        # Process payment
        await self.payment_service.process(order)
        
        return order
```

---

## Documentation

### Service Docstrings

```python
class UserService:
    """
    Service for user management operations.
    
    Responsibilities:
    - User CRUD operations
    - Password hashing and verification
    - Email uniqueness validation
    - User profile updates
    
    Dependencies:
    - UserRepository: Data access
    - EmailService: Sending emails (optional)
    - SecurityUtils: Password utilities
    
    Example:
        service = UserService(db)
        user = await service.create({
            "email": "user@example.com",
            "password": "SecurePass123",
            "name": "John Doe"
        })
    """
```

---

## Anti-Patterns to Avoid

1. **HTTP in Service**: Keep HTTP in routes
2. **Raw SQL in Service**: Use repository
3. **Mixed Responsibilities**: One domain per service
4. **Hardcoded Dependencies**: Use injection
5. **No Testing**: Test all business logic
6. **Swallowing Exceptions**: Let them propagate
7. **Missing Documentation**: Document methods
8. **Direct External Calls**: Use dedicated services