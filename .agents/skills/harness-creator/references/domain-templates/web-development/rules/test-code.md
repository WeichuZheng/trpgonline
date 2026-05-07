# Test Code Rule

**Path Scope:** `tests/**/*.{py,js,ts,tsx,jsx}`

**Severity:** STANDARD

---

## Rule: Test Code Standards

All test code must follow these standards for reliability, coverage, and maintainability.

---

## Test Organization

### Directory Structure

```
tests/
├── frontend/            # Frontend tests
│   ├── components/      # Component tests
│   ├── hooks/           # Hook tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── backend/             # Backend tests
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   ├── services/        # Service tests
│   └── api/             # API endpoint tests
├── fixtures/            # Test fixtures/data
├── helpers/             # Test helpers
└── conftest.py          # Pytest configuration
```

---

## Frontend Tests

### Component Test Template

```typescript
// tests/frontend/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../../../src/frontend/components/common/Button';

describe('Button', () => {
  // Happy path
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  // Interaction
  it('handles click events', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    await userEvent.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // Props variations
  it('applies variant styles', () => {
    render(<Button variant="primary">Primary</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('primary');
  });

  // Disabled state
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  // Accessibility
  it('is accessible', () => {
    render(<Button aria-label="Submit form">Submit</Button>);
    expect(screen.getByRole('button', { name: 'Submit form' })).toBeInTheDocument();
  });
});
```

### Hook Test Template

```typescript
// tests/frontend/hooks/useApi.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useApi } from '../../../src/frontend/hooks/useApi';

describe('useApi', () => {
  it('fetches data successfully', async () => {
    const { result } = renderHook(() => useApi('/api/users'));
    
    // Initially loading
    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBe(null);
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).not.toBe(null);
    });
  });

  it('handles errors', async () => {
    // Mock failed fetch
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));
    
    const { result } = renderHook(() => useApi('/api/error'));
    
    await waitFor(() => {
      expect(result.current.error).not.toBe(null);
      expect(result.current.error.message).toBe('Network error');
    });
  });
});
```

---

## Backend Tests

### Unit Test Template (Python)

```python
# tests/backend/services/user_service_test.py
import pytest
from unittest.mock import Mock, AsyncMock, patch

from src.backend.services.user_service import UserService
from src.backend.exceptions import ValidationError, DuplicateError

class TestUserService:
    """Unit tests for UserService."""
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def mock_repository(self):
        repo = Mock()
        repo.exists_by_email = AsyncMock(return_value=False)
        repo.create = AsyncMock(return_value=Mock(
            id=1, 
            email="test@example.com", 
            name="Test"
        ))
        return repo
    
    @pytest.fixture
    def service(self, mock_db, mock_repository):
        service = UserService(mock_db)
        service.repository = mock_repository
        return service
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, service):
        """Test successful user creation."""
        data = {
            "email": "test@example.com",
            "password": "SecurePass123",
            "name": "Test User"
        }
        user = await service.create(data)
        
        assert user.id == 1
        assert user.email == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_create_user_missing_email(self, service):
        """Test validation error for missing email."""
        data = {"password": "pass", "name": "Test"}
        
        with pytest.raises(ValidationError) as exc:
            await service.create(data)
        
        assert "email" in str(exc.value)
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, service, mock_repository):
        """Test duplicate error for existing email."""
        mock_repository.exists_by_email = AsyncMock(return_value=True)
        data = {
            "email": "existing@example.com",
            "password": "pass",
            "name": "Test"
        }
        
        with pytest.raises(DuplicateError):
            await service.create(data)
```

### API Integration Test Template

```python
# tests/backend/api/users_test.py
import pytest
from httpx import AsyncClient
from src.backend.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

class TestUsersAPI:
    """Integration tests for users API."""
    
    @pytest.mark.asyncio
    async def test_list_users(self, client):
        """Test listing users."""
        response = await client.get("/api/users")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
    
    @pytest.mark.asyncio
    async def test_create_user(self, client):
        """Test creating a user."""
        response = await client.post(
            "/api/users",
            json={
                "email": "new@example.com",
                "password": "SecurePass123",
                "name": "New User"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
    
    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self, client):
        """Test validation error."""
        response = await client.post(
            "/api/users",
            json={
                "email": "invalid",
                "password": "pass",
                "name": "Test"
            }
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client):
        """Test 404 for non-existent user."""
        response = await client.get("/api/users/9999")
        
        assert response.status_code == 404
```

---

## Test Fixtures

### Fixture Organization

```python
# tests/fixtures/users.py
import pytest
from src.backend.models.user import User

@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "password": "hashed_password",
        "name": "Test User"
    }

@pytest.fixture
def sample_user(db, sample_user_data):
    user = User(**sample_user_data)
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def auth_headers(sample_user):
    token = create_token(sample_user.id)
    return {"Authorization": f"Bearer {token}"}
```

---

## Test Naming Conventions

### Test Function Names

```python
# Pattern: test_<method>_<scenario>_<expected>

def test_create_user_valid_data_success():
    # Test creating user with valid data succeeds
    
def test_create_user_missing_email_validation_error():
    # Test creating user without email raises ValidationError
    
def test_create_user_duplicate_email_duplicate_error():
    # Test creating user with existing email raises DuplicateError

def test_list_users_pagination_returns_paginated():
    # Test listing users with pagination returns paginated result
```

---

## Coverage Requirements

### Minimum Coverage Targets

| Domain | Target | Critical Paths |
|--------|--------|----------------|
| Frontend | 80% | 100% |
| Backend Services | 80% | 100% |
| API Endpoints | 70% | 100% |
| Models | 70% | N/A |

### Coverage Commands

```bash
# Python
pytest --cov=src/backend --cov-report=html --cov-report=term

# JavaScript
npm run test:coverage
```

---

## Test Quality Checklist

- [ ] Test isolated (no dependencies on other tests)
- [ ] Test name describes what it tests
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] No test interdependencies
- [ ] Proper fixtures used
- [ ] Cleanup after test

---

## Anti-Patterns to Avoid

1. **Empty Tests**: Tests that don't verify anything
2. **Test Dependencies**: Tests that depend on order/other tests
3. **Magic Values**: Hardcoded values without explanation
4. **Testing Implementation**: Test behavior, not code
5. **Missing Cleanup**: Tests that leave state behind
6. **Large Tests**: One test testing multiple things
7. **No Error Tests**: Only testing happy path
8. **Mock Everything**: Some real integration tests needed