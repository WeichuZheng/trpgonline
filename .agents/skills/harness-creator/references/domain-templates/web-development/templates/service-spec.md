# Service Specification Template

> Template for documenting service layer components.

---

## Service: [Service Name]

**Version**: 1.0
**Last Updated**: [Date]
**Author**: [Author]
**Domain**: [frontend/backend/database]

---

## Overview

[2-3 sentence description of what this service does]

## Responsibilities

| Responsibility | Description |
|----------------|-------------|
| [Task 1] | [Description of what it does] |
| [Task 2] | [Description of what it does] |
| [Task 3] | [Description of what it does] |

## Does NOT Handle

- [What this service does NOT do]
- [Keep clear boundaries]

---

## Dependencies

### Internal Dependencies

| Dependency | Purpose | Required |
|------------|---------|----------|
| [Repository] | Data access | Yes |
| [Other Service] | [Purpose] | No |

### External Dependencies

| Dependency | Purpose | Required |
|------------|---------|----------|
| Database | Data storage | Yes |
| Redis | Caching | No |

---

## Methods

### [MethodName]

**Purpose**: [What this method does]

**Signature**:
```python
async def [method_name](
    self,
    [param1]: [type],
    [param2]: [type] = None
) -> [return_type]
```

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | [type] | Yes | [Description] |
| param2 | [type] | No | [Description] |

**Returns**: [return_type] - [Description of return value]

**Raises**:

| Exception | Condition |
|-----------|-----------|
| ValidationError | Invalid input data |
| NotFoundError | Resource not found |

**Example**:
```python
service = [ServiceName](db)
result = await service.[method_name](
    param1="value",
    param2="optional"
)
```

---

### [MethodName2]

**Purpose**: [What this method does]

**Signature**:
```python
async def [method_name2](
    self,
    [param]: [type]
) -> [return_type]
```

[Same structure as above]

---

## Business Rules

### Rule 1: [Rule Name]

**Description**: [What the rule enforces]

**Implementation**: [How it's enforced]

**Example**: [Concrete example]

### Rule 2: [Rule Name]

[Same structure]

---

## Error Handling

### Error Types

| Error Type | HTTP Status | When Raised |
|------------|-------------|-------------|
| ValidationError | 400 | Invalid input |
| NotFoundError | 404 | Resource missing |
| DuplicateError | 409 | Duplicate resource |
| AuthorizationError | 403 | Unauthorized |

### Error Messages

```python
# Example error messages
ValidationError("Email is required", field="email")
NotFoundError("User not found", resource_id=user_id)
DuplicateError("Email already registered")
```

---

## Testing

### Test Coverage Requirements

| Method | Minimum Coverage |
|--------|------------------|
| create | 80% |
| get | 80% |
| update | 80% |
| delete | 80% |

### Test Cases

| Test Case | Method | Scenario | Expected |
|-----------|--------|----------|----------|
| Create valid | create | Valid data | Success |
| Create invalid | create | Missing required | ValidationError |
| Get existing | get | Valid ID | Return entity |
| Get missing | get | Invalid ID | NotFoundError |

---

## Performance

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Create | < 100ms | Including validation |
| Get | < 50ms | Cached if possible |
| List | < 200ms | Paginated |
| Update | < 100ms | Including validation |

### Caching Strategy

| Data | Cache | TTL |
|------|-------|-----|
| [Entity] | Yes | 5 minutes |
| [List] | No | - |

---

## Security

### Security Requirements

- [ ] Input validation on all methods
- [ ] Authorization checks where needed
- [ ] No secrets in service code
- [ ] Audit logging for sensitive operations

---

## Usage Examples

### Basic Usage

```python
from src.backend.services.[service_name] import [ServiceName]

# Initialize
service = [ServiceName](db)

# Create
entity = await service.create({
    "field1": "value",
    "field2": "value"
})

# Get
entity = await service.get(entity_id)

# Update
entity = await service.update(entity_id, {
    "field1": "new_value"
})

# Delete
await service.delete(entity_id)
```

### With Error Handling

```python
from src.backend.exceptions import ValidationError, NotFoundError

try:
    entity = await service.create(data)
except ValidationError as e:
    # Handle validation error
    logger.warning(f"Validation failed: {e}")
except DuplicateError as e:
    # Handle duplicate
    logger.warning(f"Duplicate: {e}")
```

---

## Notes

[Any additional implementation notes]