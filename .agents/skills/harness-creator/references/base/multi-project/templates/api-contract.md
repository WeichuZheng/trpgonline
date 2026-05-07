# API Contract: [API Name]

> API contract specification for [service name]
> Version: [major.minor.patch]
> Status: DRAFT | PROPOSED | APPROVED | DEPRECATED | RETIRED
> Created: [DATE]
> Last Updated: [DATE]

---

## Overview

### Purpose
[2-3 sentences describing what this API provides and why]

### Audience
- Primary consumers: [list consumer types]
- Secondary consumers: [list if applicable]

### Base URL
- Production: `https://api.example.com/v[version]`
- Staging: `https://api-staging.example.com/v[version]`

---

## Authentication

### Methods

| Method | Use Case | Header |
|--------|----------|--------|
| Bearer Token | User requests | `Authorization: Bearer <token>` |
| API Key | Service-to-service | `X-API-Key: <key>` |
| OAuth 2.0 | Third-party access | `Authorization: Bearer <token>` |

### Scopes

| Scope | Description | Endpoints |
|-------|-------------|-----------|
| `read:users` | Read user profiles | GET /users/* |
| `write:users` | Modify user profiles | POST, PUT, DELETE /users/* |
| `admin:users` | Administrative access | All /users/* |

---

## Endpoints

### [Resource Name]

#### List [Resources]

```
GET /api/v[version]/[resource]
```

**Description**: [What this endpoint does]

**Authentication**: Required | Optional | None

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 20 | Maximum items to return |
| `offset` | integer | No | 0 | Number of items to skip |
| `sort` | string | No | `created_at` | Sort field |
| `order` | string | No | `desc` | Sort order (asc/desc) |

**Request Headers**:

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer token |
| `Accept` | No | Response format (application/json) |

**Response**:

```json
{
  "data": [
    {
      "id": "uuid",
      "field1": "value1",
      "field2": "value2",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

**Status Codes**:

| Code | Meaning | When to Expect |
|------|---------|----------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid query parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server error |

---

#### Create [Resource]

```
POST /api/v[version]/[resource]
```

**Description**: [What this endpoint does]

**Authentication**: Required

**Request Body**:

```json
{
  "field1": "required string",
  "field2": "optional string",
  "field3": 123
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `field1` | string | Yes | min: 1, max: 100 | Description |
| `field2` | string | No | min: 0, max: 500 | Description |
| `field3` | integer | No | min: 0, max: 1000 | Description |

**Response**:

```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2",
  "field3": 123,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes**:

| Code | Meaning | When to Expect |
|------|---------|----------------|
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request body |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |

---

#### Get [Resource]

```
GET /api/v[version]/[resource]/{id}
```

**Description**: [What this endpoint does]

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | uuid | Yes | Resource identifier |

**Response**: [Same as Create response]

---

#### Update [Resource]

```
PUT /api/v[version]/[resource]/{id}
PATCH /api/v[version]/[resource]/{id}
```

**Description**: [What this endpoint does]

**Request Body**:

```json
{
  "field1": "updated value",
  "field2": "updated value"
}
```

---

#### Delete [Resource]

```
DELETE /api/v[version]/[resource]/{id}
```

**Description**: [What this endpoint does]

**Status Codes**:

| Code | Meaning | When to Expect |
|------|---------|----------------|
| 204 | No Content | Resource deleted successfully |
| 404 | Not Found | Resource does not exist |

---

## Data Models

### [Model Name]

```json
{
  "id": "uuid",
  "field1": "string",
  "field2": "integer",
  "field3": {
    "nested_field": "string"
  },
  "created_at": "ISO8601 datetime",
  "updated_at": "ISO8601 datetime"
}
```

**Field Definitions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | uuid | Yes | Unique identifier |
| `field1` | string | Yes | Description |
| `field2` | integer | No | Description |
| `field3.nested_field` | string | No | Description |
| `created_at` | datetime | Yes | Creation timestamp |
| `updated_at` | datetime | Yes | Last update timestamp |

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "field_name",
        "message": "Specific error for this field"
      }
    ],
    "request_id": "uuid",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `AUTHENTICATION_REQUIRED` | 401 | Authentication required |
| `INSUFFICIENT_PERMISSIONS` | 403 | Permission denied |
| `RESOURCE_NOT_FOUND` | 404 | Resource does not exist |
| `RESOURCE_CONFLICT` | 409 | Resource already exists |
| `VALIDATION_FAILED` | 422 | Business validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Rate Limiting

### Default Limits

| Scope | Limit | Window |
|-------|-------|--------|
| Anonymous | 100 | 1 minute |
| Authenticated | 1000 | 1 minute |
| Service Account | 10000 | 1 minute |

### Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705315800
```

---

## Versioning

### Version Strategy
URL path versioning (e.g., `/api/v1/`, `/api/v2/`)

### Compatibility Guarantees

| Change Type | Backward Compatible | Requires Version Bump |
|-------------|---------------------|----------------------|
| Add endpoint | Yes | Minor |
| Add optional field | Yes | Minor |
| Add required field | No | Major |
| Remove endpoint | No | Major |
| Remove field | No | Major |
| Change field type | No | Major |

### Deprecation Policy

1. Announce deprecation 6 months in advance
2. Add `Deprecation: true` header in responses
3. Add `Sunset` header with removal date
4. Provide migration guide
5. Support both versions during transition

---

## SDKs and Client Libraries

### Generated SDKs

| Language | Package | Version | Documentation |
|----------|---------|---------|---------------|
| TypeScript | `@example/api-client` | `[version]` | [Link] |
| Python | `example-api` | `[version]` | [Link] |
| Java | `com.example:api-client` | `[version]` | [Link] |
| Go | `github.com/example/api-go` | `[version]` | [Link] |

### SDK Generation

```bash
# Generate TypeScript client
openapi-generator generate \
  -i api-contract.yaml \
  -g typescript-axios \
  -o clients/typescript

# Generate Python client
openapi-generator generate \
  -i api-contract.yaml \
  -g python \
  -o clients/python
```

---

## Testing

### Example Requests

#### cURL

```bash
# List resources
curl -X GET "https://api.example.com/v1/resources" \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json"

# Create resource
curl -X POST "https://api.example.com/v1/resources" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}'
```

#### Postman Collection

[Link to Postman collection]

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | [DATE] | [Author] | Initial API release |

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| API Owner | [Name] | [DATE] | [Signature] |
| Technical Lead | [Name] | [DATE] | [Signature] |
| Security Review | [Name] | [DATE] | [Signature] |