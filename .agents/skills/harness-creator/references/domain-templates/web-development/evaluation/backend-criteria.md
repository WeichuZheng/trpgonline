# Backend Evaluation Criteria

> Objective, testable criteria for evaluating backend implementation quality.

---

## Criterion Categories

### 1. API Design
### 2. Service Quality
### 3. Data Validation
### 4. Security
### 5. Performance
### 6. Testing
### 7. Error Handling

---

## API Design Criteria

### AD1: RESTful Conventions
| Field | Value |
|-------|-------|
| **ID** | AD1 |
| **Name** | RESTful API Conventions |
| **Description** | Endpoints follow RESTful naming and method conventions |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Nouns for resources, correct HTTP methods, consistent URL patterns.

**Fail Condition**: Verbs in URLs, wrong HTTP methods, inconsistent patterns.

**Test Conditions**:
- Happy Path: GET /users, POST /users, PUT /users/{id}
- Edge Cases: Nested resources /users/{id}/orders
- Error Cases: /getUsers endpoint (wrong pattern)

---

### AD2: Response Format
| Field | Value |
|-------|-------|
| **ID** | AD2 |
| **Name** | Response Format Consistency |
| **Description** | All endpoints return consistent response format |
| **Category** | Design |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Standard wrapper (data/meta), consistent timestamps, version info.

**Fail Condition**: Inconsistent formats, missing metadata, varying structures.

---

### AD3: Authentication
| Field | Value |
|-------|-------|
| **ID** | AD3 |
| **Name** | Authentication Implementation |
| **Description** | Protected endpoints properly verify authentication |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: Auth decorator/middleware, token validation, proper 401 responses.

**Fail Condition**: Missing auth checks, bypassable auth, incorrect status codes.

---

## Service Quality Criteria

### SQ1: Service Separation
| Field | Value |
|-------|-------|
| **ID** | SQ1 |
| **Name** | Service Layer Separation |
| **Description** | Business logic is in services, not route handlers |
| **Category** | Architecture |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Routes delegate to services, services handle logic, clear boundaries.

**Fail Condition**: Logic in routes, missing service layer, mixed concerns.

---

### SQ2: Service Testing
| Field | Value |
|-------|-------|
| **ID** | SQ2 |
| **Name** | Service Unit Testing |
| **Description** | Services have adequate unit test coverage |
| **Category** | Testing |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: > 80% coverage, business rules tested, edge cases covered.

**Fail Condition**: < 60% coverage, untested business logic, missing edge cases.

---

### SQ3: Service Documentation
| Field | Value |
|-------|-------|
| **ID** | SQ3 |
| **Name** | Service Documentation |
| **Description** | Service methods are documented with clear descriptions |
| **Category** | Quality |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Docstrings present, parameters documented, return values described.

**Fail Condition**: Missing documentation, unclear method purpose, undocumented parameters.

---

## Data Validation Criteria

### DV1: Input Validation
| Field | Value |
|-------|-------|
| **ID** | DV1 |
| **Name** | Input Validation |
| **Description** | All endpoint inputs are validated before processing |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: Pydantic/schema validation, type checking, constraint validation.

**Fail Condition**: No validation, raw input processed, validation missing on required fields.

---

### DV2: Validation Response
| Field | Value |
|-------|-------|
| **ID** | DV2 |
| **Name** | Validation Error Response |
| **Description** | Validation errors return proper 400 response with details |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 7/10 |

**Pass Condition**: 400 status, field-level errors, actionable messages.

**Fail Condition**: Wrong status code, generic error, missing field details.

---

## Security Criteria

### SC1: SQL Injection Prevention
| Field | Value |
|-------|-------|
| **ID** | SC1 |
| **Name** | SQL Injection Prevention |
| **Description** | No SQL injection vulnerabilities in queries |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 9/10 |

**Pass Condition**: Parameterized queries, ORM usage, no raw SQL with user input.

**Fail Condition**: Raw SQL with input concatenation, injectable queries.

---

### SC2: Authorization
| Field | Value |
|-------|-------|
| **ID** | SC2 |
| **Name** | Authorization Checks |
| **Description** | Proper authorization for resource access |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: Role/permission checks, resource ownership verified, 403 on unauthorized.

**Fail Condition**: Missing authorization, anyone can access any resource.

---

### SC3: Secrets Management
| Field | Value |
|-------|-------|
| **ID** | SC3 |
| **Name** | Secrets Management |
| **Description** | No hardcoded secrets in code |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 10/10 |

**Pass Condition**: Secrets from environment/secret manager, no hardcoded credentials.

**Fail Condition**: Hardcoded passwords, keys, tokens, or database URLs with credentials.

---

## Performance Criteria

### PC1: Response Time
| Field | Value |
|-------|-------|
| **ID** | PC1 |
| **Name** | API Response Time |
| **Description** | API responds within acceptable time limits |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: < 200ms p95 latency, documented slow endpoints, caching where needed.

**Fail Condition**: > 500ms common, undocumented slow endpoints, no caching.

---

### PC2: Query Efficiency
| Field | Value |
|-------|-------|
| **ID** | PC2 |
| **Name** | Query Efficiency |
| **Description** | No N+1 queries, proper indexing |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Single queries for relations, indexes on query columns, query analysis.

**Fail Condition**: N+1 patterns, missing indexes, unoptimized queries.

---

## Testing Criteria

### TC1: Endpoint Testing
| Field | Value |
|-------|-------|
| **ID** | TC1 |
| **Name** | Endpoint Integration Testing |
| **Description** | All endpoints have integration tests |
| **Category** | Testing |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Happy path tested, error cases tested, auth tested.

**Fail Condition**: Untested endpoints, missing error tests, missing auth tests.

---

### TC2: Test Isolation
| Field | Value |
|-------|-------|
| **ID** | TC2 |
| **Name** | Test Isolation |
| **Description** | Tests are isolated and don't depend on each other |
| **Category** | Testing |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Each test runs independently, proper fixtures, no shared state.

**Fail Condition**: Tests depend on order, shared mutable state, fixture leakage.

---

## Error Handling Criteria

### EH1: Error Response Format
| Field | Value |
|-------|-------|
| **ID** | EH1 |
| **Name** | Error Response Format |
| **Description** | Errors return consistent format with actionable info |
| **Category** | UX |
| **Priority** | P1 |
| **Weight** | Medium |
| **Threshold** | 7/10 |

**Pass Condition**: Error code, message, details, proper HTTP status.

**Fail Condition**: Inconsistent format, missing error code, wrong status.

---

### EH2: Exception Handling
| Field | Value |
|-------|-------|
| **ID** | EH2 |
| **Name** | Exception Handling |
| **Description** | Exceptions are caught and handled properly |
| **Category** | Quality |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Try/catch for risky operations, proper error conversion, no uncaught.

**Fail Condition**: Uncaught exceptions, 500 errors from known issues, swallowed errors.

---

### EH3: Logging
| Field | Value |
|-------|-------|
| **ID** | EH3 |
| **Name** | Error Logging |
| **Description** | Errors are logged with sufficient context |
| **Category** | Operations |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Log level appropriate, stack trace, context info, correlation ID.

**Fail Condition**: No logging, missing context, excessive logging.

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