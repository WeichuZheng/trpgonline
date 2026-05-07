# API Evaluation Criteria

> Objective, testable criteria for evaluating API design and implementation quality.

---

## Criterion Categories

### 1. Endpoint Design
### 2. Request/Response Schema
### 3. Error Handling
### 4. Authentication & Authorization
### 5. Performance
### 6. Documentation
### 7. Versioning

---

## Endpoint Design Criteria

### ED1: URL Structure
| Field | Value |
|-------|-------|
| **ID** | ED1 |
| **Name** | URL Structure |
| **Description** | URLs follow RESTful resource naming conventions |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Resource nouns (/users, /orders), hierarchical nesting correct, no verbs.

**Fail Condition**: Verbs in URLs (/getUsers), incorrect nesting, inconsistent naming.

**Examples**:
```
GOOD: GET /users, POST /users, GET /users/{id}/orders
BAD: GET /getUsers, POST /createUser, GET /user_orders
```

---

### ED2: HTTP Methods
| Field | Value |
|-------|-------|
| **ID** | ED2 |
| **Name** | HTTP Method Usage |
| **Description** | Correct HTTP methods for each operation type |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: GET for read, POST for create, PUT/PATCH for update, DELETE for remove.

**Fail Condition**: POST for reads, GET for updates, incorrect methods.

**Method Mapping**:
| Operation | Method | Idempotent |
|-----------|--------|------------|
| List | GET | Yes |
| Get one | GET | Yes |
| Create | POST | No |
| Update full | PUT | Yes |
| Update partial | PATCH | No |
| Delete | DELETE | Yes |

---

### ED3: Path Parameters
| Field | Value |
|-------|-------|
| **ID** | ED3 |
| **Name** | Path Parameters |
| **Description** | Path parameters properly used for resource identification |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: IDs in path, validated, documented.

**Fail Condition**: IDs in query/body, unvalidated, undocumented.

---

## Request/Response Schema Criteria

### RS1: Request Schema
| Field | Value |
|-------|-------|
| **ID** | RS1 |
| **Name** | Request Schema Definition |
| **Description** | Request bodies have defined schema with types and validation |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Pydantic model or equivalent, types defined, required fields marked.

**Fail Condition**: No schema, implicit types, no validation.

---

### RS2: Response Schema
| Field | Value |
|-------|-------|
| **ID** | RS2 |
| **Name** | Response Schema Definition |
| **Description** | Responses have defined schema with consistent structure |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Defined response model, data/meta wrapper, documented fields.

**Fail Condition**: Undefined response, inconsistent structure, undocumented.

---

### RS3: Pagination
| Field | Value |
|-------|-------|
| **ID** | RS3 |
| **Name** | Pagination Implementation |
| **Description** | List endpoints support pagination |
| **Category** | Design |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Page/limit parameters, total count returned, cursor option for large data.

**Fail Condition**: No pagination, returns all results, missing metadata.

---

## Error Handling Criteria

### EH1: Error Response Structure
| Field | Value |
|-------|-------|
| **ID** | EH1 |
| **Name** | Error Response Structure |
| **Description** | Errors return consistent structure with actionable information |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Error object with code, message, details; field-level errors for validation.

**Fail Condition**: Inconsistent structure, missing details, no error code.

**Standard Error Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid format" }
    ]
  }
}
```

---

### EH2: HTTP Status Codes
| Field | Value |
|-------|-------|
| **ID** | EH2 |
| **Name** | HTTP Status Codes |
| **Description** | Correct status codes for each scenario |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: 200/201 for success, 400 for validation, 401 for auth, 404 for missing.

**Fail Condition**: Wrong codes, everything returns 200, 500 for expected errors.

**Status Code Guide**:
| Status | Usage |
|--------|-------|
| 200 OK | Successful GET, PUT |
| 201 Created | Successful POST (resource created) |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Validation error |
| 401 Unauthorized | Missing/invalid auth |
| 403 Forbidden | Authenticated but not allowed |
| 404 Not Found | Resource doesn't exist |
| 409 Conflict | Duplicate/conflict |
| 500 Internal Error | Unexpected server error |

---

## Authentication & Authorization Criteria

### AA1: Authentication Required
| Field | Value |
|-------|-------|
| **ID** | AA1 |
| **Name** | Authentication Requirement |
| **Description** | Protected endpoints require authentication |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 10/10 |

**Pass Condition**: Auth middleware/decorator, token validation, 401 for missing.

**Fail Condition**: No auth check, public access to protected resources.

---

### AA2: Authorization Level
| Field | Value |
|-------|-------|
| **ID** | AA2 |
| **Name** | Authorization Level |
| **Description** | Appropriate authorization for operations |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: Role/permission checks, ownership verification, 403 for unauthorized.

**Fail Condition**: No authorization, any authenticated user can do anything.

---

### AA3: Token Security
| Field | Value |
|-------|-------|
| **ID** | AA3 |
| **Name** | Token Security |
| **Description** | Tokens handled securely |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: HttpOnly cookies or header auth, token expiration, refresh mechanism.

**Fail Condition**: Tokens in URL, no expiration, no refresh.

---

## Performance Criteria

### PF1: Response Latency
| Field | Value |
|-------|-------|
| **ID** | PF1 |
| **Name** | Response Latency |
| **Description** | API responds within acceptable latency |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: p95 < 200ms for standard, documented exceptions for slow operations.

**Fail Condition**: p95 > 500ms common, undocumented slow endpoints.

---

### PF2: Rate Limiting
| Field | Value |
|-------|-------|
| **ID** | PF2 |
| **Name** | Rate Limiting |
| **Description** | Rate limiting protects API from abuse |
| **Category** | Security |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Rate limits defined, 429 response when exceeded, documented limits.

**Fail Condition**: No rate limiting, API abuse possible.

---

## Documentation Criteria

### DC1: Endpoint Documentation
| Field | Value |
|-------|-------|
| **ID** | DC1 |
| **Name** | Endpoint Documentation |
| **Description** | All endpoints documented with OpenAPI/Swagger or equivalent |
| **Category** | Documentation |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: OpenAPI spec, examples, descriptions for all endpoints.

**Fail Condition**: Missing documentation, incomplete spec, no examples.

---

### DC2: Schema Documentation
| Field | Value |
|-------|-------|
| **ID** | DC2 |
| **Name** | Schema Documentation |
| **Description** | Request/response schemas documented with examples |
| **Category** | Documentation |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Field descriptions, examples, type info in documentation.

**Fail Condition**: Undocumented fields, missing examples, unclear types.

---

## Versioning Criteria

### VR1: API Versioning
| Field | Value |
|-------|-------|
| **ID** | VR1 |
| **Name** | API Versioning |
| **Description** | API version in URL or header |
| **Category** | Design |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Version in URL (/api/v1/) or header, documented version strategy.

**Fail Condition**: No versioning, breaking changes without version.

---

### VR2: Backward Compatibility
| Field | Value |
|-------|-------|
| **ID** | VR2 |
| **Name** | Backward Compatibility |
| **Description** | Non-breaking changes maintain compatibility |
| **Category** | Design |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Optional fields added, new endpoints, no removed fields in same version.

**Fail Condition**: Breaking changes in same version, removed fields.

---

## Grading Guide

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceptional quality, exceeds requirements |
| 9/10 | Excellent | Fully meets all criteria, minor polish possible |
| 8/10 | Very Good | Meets criteria, small edge case issues |
| 7/10 | Good | Meets criteria well, some minor issues |
| 6/10 | Acceptable | Meets basic criteria, notable gaps |
| 5/10 | Marginal | Partially meets criteria, significant work needed |
| 4/10 | Below Standard | Fails some aspects, rework needed |
| 3/10 | Poor | Major issues, substantial rework |
| 2/10 | Very Poor | Critical failures, mostly broken |
| 1/10 | Fail | Does not meet criteria |
| 0/10 | No Attempt | Criterion not addressed |

---

## Priority Definitions

- **P1**: Must pass - blocks release
- **P2**: Should pass - minor issues acceptable with documentation
- **P3**: Nice to have - failure acceptable