# API Code Rule

**Path Scope:** `src/backend/api/**/*.py`

**Severity:** STANDARD

---

## Rule: API Code Standards

All API endpoint code must follow these standards for consistency, security, and maintainability.

---

## Endpoint Structure

### File Organization

```
src/backend/api/
├── routes/              # Route definitions
│   ├── users.py         # User endpoints
│   ├── orders.py        # Order endpoints
│   └── auth.py          # Authentication endpoints
├── dependencies.py      # Shared dependencies (auth, etc.)
└── __init__.py          # Router aggregation
```

### Endpoint Template (FastAPI)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

from src.backend.services.user_service import UserService
from src.backend.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Request/Response Models
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

class UserList(BaseModel):
    data: List[UserResponse]
    meta: dict

# Endpoints
@router.get("/", response_model=UserList)
async def list_users(
    page: int = 1,
    limit: int = 20,
    user = Depends(get_current_user)
):
    """
    List all users with pagination.
    
    Requires authentication.
    """
    service = UserService()
    users = await service.list(page=page, limit=limit)
    return {
        "data": users,
        "meta": {"page": page, "limit": limit}
    }

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate):
    """
    Create a new user.
    """
    service = UserService()
    user = await service.create(request.dict())
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user = Depends(get_current_user)
):
    """
    Get a specific user by ID.
    """
    service = UserService()
    user = await service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

---

## Request Validation

### Pydantic Models

```python
from pydantic import BaseModel, EmailStr, validator, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
```

---

## Response Format

### Standard Response Wrapper

```python
# Success response
{
    "data": {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe"
    },
    "meta": {
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0"
    }
}

# List response
{
    "data": [...],
    "meta": {
        "total": 100,
        "page": 1,
        "limit": 20
    }
}

# Error response
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": [
            {"field": "email", "message": "Invalid email format"}
        ]
    }
}
```

---

## Error Handling

### HTTPException Usage

```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# Validation error
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": "VALIDATION_ERROR", "message": "Invalid input"}
)

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"}
)

# Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this resource"
)
```

---

## Authentication

### Dependency Pattern

```python
# api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Validate token and return current user.
    """
    token = credentials.credentials
    user = await validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user

# Usage in routes
@router.get("/protected")
async protected_endpoint(user = Depends(get_current_user)):
    # user is authenticated
    return {"user": user}
```

---

## Service Separation

### Keep Logic in Services

```python
# BAD - Logic in route
@router.post("/users")
async def create_user(request: UserCreate):
    # Validate
    if not request.email:
        raise HTTPException(400, "Email required")
    
    # Check duplicate
    existing = await db.query(User).filter(email=request.email).first()
    if existing:
        raise HTTPException(409, "Email exists")
    
    # Hash password
    hashed = bcrypt.hash(request.password)
    
    # Create
    user = User(email=request.email, password=hashed, name=request.name)
    db.add(user)
    await db.commit()
    
    return user

# GOOD - Logic in service
@router.post("/users")
async def create_user(request: UserCreate):
    service = UserService()
    user = await service.create(request.dict())
    return user

# services/user_service.py
class UserService:
    async def create(self, data: dict):
        # All logic here
        self._validate(data)
        await self._check_duplicate(data['email'])
        data['password'] = self._hash_password(data['password'])
        return await self._save(data)
```

---

## Pagination

### Standard Pagination

```python
@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    service = UserService()
    users, total = await service.list(page=page, limit=limit)
    return {
        "data": users,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": ceil(total / limit)
        }
    }
```

---

## Documentation

### Endpoint Docstrings

```python
@router.post("/users", response_model=UserResponse)
async def create_user(request: UserCreate):
    """
    Create a new user account.
    
    Args:
        request: User creation data including email, password, and name.
    
    Returns:
        UserResponse: The created user with ID and profile data.
    
    Raises:
        400 Bad Request: Invalid input data.
        409 Conflict: Email already exists.
    
    Example:
        POST /users
        {
            "email": "user@example.com",
            "password": "SecurePass123",
            "name": "John Doe"
        }
    """
```

---

## Security Checklist

- [ ] Authentication on protected endpoints
- [ ] Authorization for resource access
- [ ] Input validation with Pydantic
- [ ] No hardcoded secrets
- [ ] SQL injection prevention (use ORM)
- [ ] Rate limiting on sensitive endpoints
- [ ] CORS configured
- [ ] Error messages don't leak info

---

## Anti-Patterns to Avoid

1. **Logic in Routes**: Move to services
2. **No Validation**: Always use Pydantic
3. **Missing Auth**: Check authentication
4. **Raw SQL**: Use ORM/parameterized
5. **Hardcoded Secrets**: Use environment
6. **Wrong Status Codes**: Use correct HTTP codes
7. **No Documentation**: Add docstrings
8. **No Error Handling**: Handle exceptions