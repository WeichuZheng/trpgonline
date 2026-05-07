# Coding Standards

> Web Development domain coding standards for consistency and quality.

---

## General Principles

1. **Readability First**: Code should be easy to understand
2. **Consistency**: Follow established patterns
3. **Documentation**: Document public APIs and complex logic
4. **Testing**: Test critical paths and edge cases
5. **Security**: No hardcoded secrets, validate inputs

---

## Frontend Standards (React/Vue)

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Component | PascalCase | `Button.tsx` |
| Hook | camelCase with 'use' | `useApi.ts` |
| Service | camelCase | `apiService.ts` |
| Style | ComponentName + .style | `Button.style.ts` |
| Test | ComponentName + .test | `Button.test.tsx` |

### Component Structure

```typescript
// imports
import React from 'react';

// types
interface Props {
  // ...
}

// component
export function Component({ prop }: Props) {
  // hooks
  const [state, setState] = useState();
  
  // handlers
  const handleClick = () => {};
  
  // render
  return (
    // JSX
  );
}

// styles (if using styled-components)
const StyledElement = styled.div``;
```

### TypeScript Standards

```typescript
// Use explicit types
interface User {
  id: number;
  name: string;
}

// Avoid 'any'
function process(user: User): void {
  // ...
}

// Use const assertions for constants
const ROUTES = {
  home: '/',
  login: '/login',
} as const;
```

### State Management

| State Type | Use |
|------------|-----|
| Local UI state | useState |
| Shared state | Context or Redux |
| Server state | React Query / SWR |
| Form state | Form library |

---

## Backend Standards (Python)

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Module | snake_case | `user_service.py` |
| Class | PascalCase | `UserService` |
| Function | snake_case | `get_user()` |
| Variable | snake_case | `user_data` |
| Constant | UPPER_SNAKE | `MAX_RETRIES` |

### Type Hints

```python
from typing import List, Optional, Dict, Any

def get_user(id: int) -> Optional[User]:
    ...

def list_users(page: int = 1, limit: int = 20) -> List[User]:
    ...

async def create(data: Dict[str, Any]) -> User:
    ...
```

### Docstrings

```python
def create_user(data: dict) -> User:
    """
    Create a new user with validation.
    
    Args:
        data: User data with email, password, name.
    
    Returns:
        Created User instance.
    
    Raises:
        ValidationError: If data is invalid.
        DuplicateError: If email exists.
    
    Example:
        user = service.create({
            "email": "test@example.com",
            "password": "SecurePass123",
            "name": "Test User"
        })
    """
```

### Error Handling

```python
# Use custom exceptions
from src.backend.exceptions import ValidationError

def validate_email(email: str) -> None:
    if not email or '@' not in email:
        raise ValidationError(
            "Invalid email format",
            field="email"
        )
```

---

## Database Standards

### Table Naming

| Type | Pattern | Example |
|------|---------|---------|
| Table | snake_case, plural | `users`, `orders` |
| Column | snake_case | `created_at` |
| Index | ix_table_column | `ix_users_email` |
| Foreign Key | fk_table_column | `fk_orders_user` |

### Column Standards

```python
# Always have these columns
id = Column(Integer, primary_key=True)
created_at = Column(DateTime, default=datetime.utcnow)
updated_at = Column(DateTime, onupdate=datetime.utcnow)

# Use appropriate types
email = Column(String(255))  # Not String() without limit
status = Column(String(20), default='active')
price = Column(Numeric(10, 2))  # Money uses Numeric
```

---

## API Standards

### Endpoint Naming

| Operation | Method | URL |
|-----------|--------|-----|
| List | GET | `/api/v1/users` |
| Create | POST | `/api/v1/users` |
| Get | GET | `/api/v1/users/{id}` |
| Update | PUT | `/api/v1/users/{id}` |
| Delete | DELETE | `/api/v1/users/{id}` |

### Response Format

```json
// Success
{
  "data": { ... },
  "meta": { "timestamp": "...", "version": "1.0" }
}

// List
{
  "data": [ ... ],
  "meta": { "total": 100, "page": 1, "limit": 20 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "...",
    "details": [ ... ]
  }
}
```

---

## Testing Standards

### Test Naming

```python
# Pattern: test_method_scenario_expected
def test_create_user_valid_data_success():
    ...

def test_create_user_missing_email_validation_error():
    ...

def test_list_users_pagination_returns_paginated():
    ...
```

### Test Structure

```python
def test_scenario():
    # Setup
    data = create_test_data()
    
    # Exercise
    result = perform_action(data)
    
    # Verify
    assert result.status == expected_status
    
    # Cleanup (if needed)
    cleanup_test_data()
```

---

## Git Standards

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | feature/description | `feature/user-profile` |
| Fix | fix/description | `fix/login-error` |
| Hotfix | hotfix/description | `hotfix/security-patch` |

### Commit Message Format

```
type(scope): subject

[optional body]

type: feat | fix | docs | style | refactor | test | chore
scope: frontend | backend | database | api | test
```

Examples:
```
feat(api): add user profile endpoint
fix(frontend): resolve login button styling
docs(api): update endpoint documentation
test(backend): add user service tests
```

---

## Security Standards

### Never Do

- Hardcode secrets in code
- Log sensitive data
- Trust user input without validation
- Use :latest Docker tags
- Skip authentication checks

### Always Do

- Validate all input
- Use environment variables for secrets
- Enable HTTPS in production
- Set up rate limiting
- Log security events

---

## Performance Standards

### Targets

| Layer | Target | Metric |
|-------|--------|--------|
| Frontend | < 3s | Page load |
| API | < 200ms | Response time |
| Database | < 50ms | Query time |
| Total | < 5s | User action |

### Optimization

- Use indexes on query columns
- Cache frequently accessed data
- Lazy load components
- Paginate large lists
- Use connection pooling