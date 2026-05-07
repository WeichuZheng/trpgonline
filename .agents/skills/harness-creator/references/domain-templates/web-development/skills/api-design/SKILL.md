---
name: api-design
description: "Guided API design workflow from requirements to documented API specification. Creates OpenAPI-style specs with validation schemas."
user-invocable: true
---

# API Design Skill

You are facilitating the API Design process. Your role is to guide the creation of well-designed, documented API specifications.

## Purpose

API design ensures:
- RESTful conventions are followed
- Request/response schemas are defined
- Error handling is consistent
- Authentication requirements are clear
- Documentation is complete

## Design Flow

```
REQUIREMENTS -> ENDPOINT DESIGN -> SCHEMA DEFINITION -> ERROR DESIGN -> DOCUMENTATION
```

## Design Workflow

### Phase 1: Requirements Analysis

1. Identify what data/operations the API needs to support
2. List required endpoints
3. Determine authentication requirements
4. Identify rate limiting needs

### Phase 2: Endpoint Design

For each endpoint:
- Define URL path (resource-based)
- Choose HTTP method (GET, POST, PUT, DELETE)
- Determine if authentication required
- Plan query parameters and path variables

### RESTful Conventions

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve resource(s) | `GET /users`, `GET /users/{id}` |
| POST | Create resource | `POST /users` |
| PUT | Update resource | `PUT /users/{id}` |
| DELETE | Remove resource | `DELETE /users/{id}` |

### Phase 3: Schema Definition

Define request and response schemas:

**Request Schema:**
```json
{
  "type": "object",
  "properties": {
    "field1": { "type": "string", "required": true },
    "field2": { "type": "integer", "minimum": 0 }
  },
  "required": ["field1"]
}
```

**Response Schema:**
```json
{
  "type": "object",
  "properties": {
    "data": { "type": "object" },
    "meta": {
      "type": "object",
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "version": { "type": "string" }
      }
    }
  }
}
```

### Phase 4: Error Design

Define error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid request data |
| AUTHENTICATION_ERROR | 401 | Missing/invalid auth |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource conflict |
| INTERNAL_ERROR | 500 | Server error |

### Phase 5: Documentation

Create API specification document:
- Endpoint descriptions
- Request/response examples
- Authentication notes
- Rate limiting information

## API Spec Template

```markdown
# API Specification: [Resource Name]

## Overview
[Description of the API resource]

## Base URL
`/api/v1/[resource]`

## Authentication
[Authentication requirements]

## Rate Limiting
[Limits if applicable]

---

## Endpoints

### List [Resources]
**GET** `/api/v1/[resource]`

**Description**: Retrieve list of [resources]

**Query Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | int | No | Page number (default: 1) |
| limit | int | No | Items per page (default: 20) |

**Response**: `200 OK`
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

---

### Create [Resource]
**POST** `/api/v1/[resource]`

**Description**: Create a new [resource]

**Request Body**:
```json
{
  "field1": "value",
  "field2": 123
}
```

**Response**: `201 Created`
```json
{
  "data": { ... },
  "meta": { ... }
}
```

**Errors**:
- 400: Validation failed
- 401: Unauthorized
- 409: Duplicate resource

---

### Get [Resource]
**GET** `/api/v1/[resource]/{id}`

**Description**: Retrieve a specific [resource]

**Path Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | int | Yes | Resource ID |

**Response**: `200 OK`
```json
{
  "data": { ... },
  "meta": { ... }
}
```

**Errors**:
- 404: Resource not found

---

### Update [Resource]
**PUT** `/api/v1/[resource]/{id}`

**Description**: Update a [resource]

**Request Body**:
```json
{
  "field1": "new value"
}
```

**Response**: `200 OK`

**Errors**:
- 400: Validation failed
- 401: Unauthorized
- 404: Resource not found

---

### Delete [Resource]
**DELETE** `/api/v1/[resource]/{id}`

**Description**: Delete a [resource]

**Response**: `204 No Content`

**Errors**:
- 401: Unauthorized
- 404: Resource not found
```

## Design Principles

1. **Consistent Naming**: Use nouns for resources, plural for collections
2. **Versioned APIs**: Include version in URL (`/api/v1/`)
3. **Stateless**: No server-side sessions, use tokens
4. **Documented**: Every endpoint has documentation
5. **Error Consistent**: Same error format across all endpoints

## Anti-Patterns to Avoid

- Verbs in URLs (`/getUsers` instead of `GET /users`)
- Inconsistent error formats
- Missing authentication documentation
- Undocumented endpoints
- Mixed naming conventions

## Usage

```
/api-design [resource description]
```

Example:
```
/api-design User management with CRUD operations
```

## Coordination

- backend-lead reviews API designs
- frontend-lead confirms frontend can consume API
- architect-lead approves cross-service APIs