# API Specification Template

> Template for documenting API endpoints and contracts.

---

## API: [Resource Name]

**Version**: 1.0
**Last Updated**: [Date]
**Author**: [Author]

---

## Overview

[2-3 sentence description of what this API provides]

## Base URL

```
/api/v1/[resource]
```

## Authentication

[Describe authentication requirements]

| Endpoint Type | Auth Required |
|---------------|---------------|
| Public endpoints | No |
| User endpoints | Yes (Bearer token) |
| Admin endpoints | Yes (Admin role) |

## Rate Limiting

| Rate Limit | Requests | Window |
|------------|----------|--------|
| Standard | 100 | 1 minute |
| Burst | 20 | 10 seconds |

---

## Endpoints

### List [Resources]

**GET** `/api/v1/[resource]`

**Description**: Retrieve a paginated list of [resources].

**Authentication**: Required

**Query Parameters**:

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| page | int | No | 1 | Page number |
| limit | int | No | 20 | Items per page (max: 100) |
| sort | string | No | created_at | Sort field |
| order | string | No | desc | Sort order (asc/desc) |
| filter | string | No | - | Filter expression |

**Response**: `200 OK`

```json
{
  "data": [
    {
      "id": 1,
      "name": "[Resource Name]",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

**Errors**:

| Status | Code | Description |
|--------|------|-------------|
| 401 | AUTHENTICATION_ERROR | Missing or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |

---

### Create [Resource]

**POST** `/api/v1/[resource]`

**Description**: Create a new [resource].

**Authentication**: Required

**Request Body**:

```json
{
  "name": "[Required: string, max 100 chars]",
  "description": "[Optional: string]",
  "type": "[Required: string, enum: type_a|type_b]"
}
```

**Response**: `201 Created`

```json
{
  "data": {
    "id": 1,
    "name": "New Resource",
    "description": "Description",
    "type": "type_a",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

**Errors**:

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid request body |
| 401 | AUTHENTICATION_ERROR | Missing or invalid token |
| 409 | CONFLICT | Duplicate resource |

---

### Get [Resource]

**GET** `/api/v1/[resource]/{id}`

**Description**: Retrieve a specific [resource] by ID.

**Authentication**: Required

**Path Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | int | Yes | Resource ID |

**Response**: `200 OK`

```json
{
  "data": {
    "id": 1,
    "name": "Resource Name",
    "description": "Description",
    "type": "type_a",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

**Errors**:

| Status | Code | Description |
|--------|------|-------------|
| 401 | AUTHENTICATION_ERROR | Missing or invalid token |
| 404 | NOT_FOUND | Resource not found |

---

### Update [Resource]

**PUT** `/api/v1/[resource]/{id}`

**Description**: Update an existing [resource].

**Authentication**: Required

**Path Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | int | Yes | Resource ID |

**Request Body**:

```json
{
  "name": "[Optional: string]",
  "description": "[Optional: string]",
  "type": "[Optional: string, enum: type_a|type_b]"
}
```

**Response**: `200 OK`

```json
{
  "data": {
    "id": 1,
    "name": "Updated Name",
    "updated_at": "2024-01-02T00:00:00Z"
  }
}
```

**Errors**:

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid request body |
| 401 | AUTHENTICATION_ERROR | Missing or invalid token |
| 403 | FORBIDDEN | Not authorized to update |
| 404 | NOT_FOUND | Resource not found |

---

### Delete [Resource]

**DELETE** `/api/v1/[resource]/{id}`

**Description**: Delete a [resource].

**Authentication**: Required (Admin)

**Path Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | int | Yes | Resource ID |

**Response**: `204 No Content`

**Errors**:

| Status | Code | Description |
|--------|------|-------------|
| 401 | AUTHENTICATION_ERROR | Missing or invalid token |
| 403 | FORBIDDEN | Not authorized to delete |
| 404 | NOT_FOUND | Resource not found |

---

## Data Models

### [Resource] Model

```json
{
  "id": "integer (auto-generated)",
  "name": "string (required, max 100)",
  "description": "string (optional)",
  "type": "string (enum: type_a, type_b)",
  "status": "string (enum: active, inactive)",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | [Date] | Initial API release |

---

## Notes

[Any additional notes or implementation details]