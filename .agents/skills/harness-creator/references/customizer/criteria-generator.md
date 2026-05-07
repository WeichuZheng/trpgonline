# Criteria Generator Prompt

> Use this prompt template to generate evaluation criteria for the harness framework.

---

## Input Parameters

When generating evaluation criteria, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `criteria_name` | Name of the criteria set | Yes |
| `feature_description` | What feature/area being evaluated | Yes |
| `domain` | Domain context (frontend, backend, api, etc.) | Yes |
| `priority_level` | Overall priority (P1, P2, P3) | Yes |
| `custom_requirements` | Specific requirements to cover | No |
| `existing_criteria` | Criteria to build upon | No |

---

## Prompt Template

```
You are generating evaluation criteria for the harness framework.

## Criteria to Generate

- **Name**: {criteria_name}
- **Feature**: {feature_description}
- **Domain**: {domain}
- **Priority**: {priority_level}
- **Custom Requirements**: {custom_requirements}
- **Existing Criteria**: {existing_criteria}

## Your Task

Create a complete evaluation criteria document following the harness framework conventions.

## Criteria Structure

Each criterion includes:

1. **ID**: Unique identifier (AC1, AC2, etc.)
2. **Name**: Clear, specific name
3. **Description**: What behavior or outcome to test
4. **Category**: Functional, Performance, Security, UX, etc.
5. **Priority**: P1 (Blocker) / P2 (Important) / P3 (Nice-to-have)
6. **Weight**: Impact on overall score
7. **Threshold**: Minimum score to pass

## Design Principles

1. **Specific**: Can a tester understand exactly what to test?
2. **Measurable**: Can results be quantified?
3. **Achievable**: Is it realistic for this sprint?
4. **Relevant**: Does it relate to the sprint goals?
5. **Testable**: Can evidence be gathered objectively?
6. **Unambiguous**: Could two evaluators reach different conclusions?

Generate the evaluation criteria now.
```

---

## Output Format

The generated criteria should follow this structure:

```markdown
# Evaluation Criteria: {Criteria Name}

> Use these criteria to evaluate {feature_description}
> **Key Principle**: If you can't write a test for it, it's not a criterion.

---

## Overview

| Field | Value |
|-------|-------|
| **Criteria Set** | {criteria_name} |
| **Feature** | {feature_description} |
| **Domain** | {domain} |
| **Total Criteria** | {count} |
| **Overall Priority** | {priority_level} |

---

## Grading Scale

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceeds expectations, exceptional quality |
| 9/10 | Excellent | Meets all criteria fully, minor polish possible |
| 8/10 | Very Good | Meets criteria completely, small edge cases |
| 7/10 | Good | Meets criteria well, some minor issues |
| 6/10 | Acceptable | Meets basic criteria, notable gaps |
| 5/10 | Marginal | Partially meets criteria, improvements needed |
| 4/10 | Below Standard | Fails some aspects, needs rework |
| 3/10 | Poor | Major issues, substantial rework required |
| 2/10 | Very Poor | Critical failures, mostly broken |
| 1/10 | Fail | Does not meet criteria at all |
| 0/10 | No Attempt | Criterion not addressed |

---

## Criteria

### {Category 1}

#### {CRITERION_ID}: {Criterion Name}

| Field | Value |
|-------|-------|
| **ID** | {ID} |
| **Name** | {Name} |
| **Description** | {Description} |
| **Category** | {Category} |
| **Priority** | {P1/P2/P3} |
| **Weight** | {High/Medium/Low} |
| **Threshold** | 6/10 |

**Pass Condition**: {Specific, measurable condition for PASS}

**Fail Condition**: {Specific conditions that constitute FAIL}

**Test Conditions**:
- **Happy Path**: {What should work}
- **Edge Cases**: {Boundary conditions}
- **Error Cases**: {How errors should be handled}

**Testing Method**:
- [ ] Manual testing
- [ ] Automated tests
- [ ] Code review
- [ ] Performance testing

---

## Summary Table

| ID | Name | Priority | Threshold | Status |
|----|------|----------|-----------|--------|
| AC1 | {Name} | P1 | 6/10 | PENDING |
| AC2 | {Name} | P1 | 6/10 | PENDING |
| AC3 | {Name} | P2 | 6/10 | PENDING |

---

## Evaluation Template

```markdown
## Evaluation Report: {Feature Name}

### Summary
- **Total Criteria**: {count}
- **Passed**: {count}
- **Failed**: {count}
- **Overall Score**: {score}/10
- **Verdict**: PASS | FAIL

### Detailed Results

#### {CRITERION_ID}: {Criterion Name}
- **Status**: PASS | FAIL
- **Score**: {score}/10
- **Evidence**: {What was tested and found}
- **Action**: {What to do if failed}
```
```

---

## Quality Checklist

Before finalizing criteria, verify:

- [ ] **Specific**: Can a tester understand exactly what to test?
- [ ] **Measurable**: Can results be quantified (pass/fail, score)?
- [ ] **Achievable**: Is it realistic to implement in this sprint?
- [ ] **Relevant**: Does it directly relate to the sprint goals?
- [ ] **Testable**: Can evidence be gathered objectively?
- [ ] **Unambiguous**: No room for interpretation
- [ ] **Priority Assigned**: Each criterion has a priority
- [ ] **Threshold Defined**: Minimum score is clear
- [ ] **Pass/Fail Clear**: Both conditions are explicit
- [ ] **No Overlap**: Criteria don't duplicate each other

---

## Category Reference

### Functional
Core functionality, business logic, data handling

### Performance
Speed, responsiveness, resource usage

### Security
Authentication, authorization, data protection

### UX/UI
User experience, accessibility, visual design

### Reliability
Error handling, edge cases, recovery

### Maintainability
Code quality, documentation, testability

---

## Examples

### Example 1: User Authentication Criteria

**Input:**
```
criteria_name: User Authentication
feature_description: User login and registration functionality
domain: backend
priority_level: P1
custom_requirements: OAuth support, rate limiting, session management
```

**Output:**
```markdown
# Evaluation Criteria: User Authentication

> Use these criteria to evaluate user login and registration functionality
> **Key Principle**: If you can't write a test for it, it's not a criterion.

---

## Overview

| Field | Value |
|-------|-------|
| **Criteria Set** | user-authentication |
| **Feature** | User login and registration functionality |
| **Domain** | backend |
| **Total Criteria** | 8 |
| **Overall Priority** | P1 |

---

## Grading Scale

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceeds expectations, exceptional quality |
| 9/10 | Excellent | Meets all criteria fully, minor polish possible |
| 8/10 | Very Good | Meets criteria completely, small edge cases |
| 7/10 | Good | Meets criteria well, some minor issues |
| 6/10 | Acceptable | Meets basic criteria, notable gaps |
| 5/10 | Marginal | Partially meets criteria, improvements needed |
| 4/10 | Below Standard | Fails some aspects, needs rework |
| 3/10 | Poor | Major issues, substantial rework required |
| 2/10 | Very Poor | Critical failures, mostly broken |
| 1/10 | Fail | Does not meet criteria at all |
| 0/10 | No Attempt | Criterion not addressed |

---

## Criteria

### Functional

#### AC1: User Registration

| Field | Value |
|-------|-------|
| **ID** | AC1 |
| **Name** | User Registration |
| **Description** | User can create a new account with email and password |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: User can register with valid email and password (min 8 chars, 1 uppercase, 1 number) and receives confirmation email within 60 seconds.

**Fail Condition**: Registration fails with valid inputs, no confirmation email, or password requirements not enforced.

**Test Conditions**:
- **Happy Path**: Register with valid email and strong password
- **Edge Cases**: Existing email, invalid email format, weak passwords
- **Error Cases**: Database unavailable, email service down

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC2: User Login

| Field | Value |
|-------|-------|
| **ID** | AC2 |
| **Name** | User Login |
| **Description** | Registered user can authenticate with valid credentials |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: User can log in with valid credentials and receives a valid session token that expires after 24 hours.

**Fail Condition**: Valid credentials rejected, invalid token generated, or session doesn't persist.

**Test Conditions**:
- **Happy Path**: Login with valid email and password
- **Edge Cases**: Wrong password, non-existent user, locked account
- **Error Cases**: Database unavailable, too many attempts

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

### Security

#### AC3: Password Security

| Field | Value |
|-------|-------|
| **ID** | AC3 |
| **Name** | Password Security |
| **Description** | Passwords are securely hashed and validated |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 8/10 |

**Pass Condition**: Passwords are hashed using bcrypt or argon2 with appropriate work factor. Plaintext passwords never appear in logs or responses.

**Fail Condition**: Plaintext passwords stored or logged, weak hashing algorithm used, or password visible in error messages.

**Test Conditions**:
- **Happy Path**: Register and verify hash in database
- **Edge Cases**: Very long passwords, unicode characters
- **Error Cases**: Check all error responses for password leaks

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC4: Rate Limiting

| Field | Value |
|-------|-------|
| **ID** | AC4 |
| **Name** | Rate Limiting |
| **Description** | Authentication endpoints are protected against brute force attacks |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 6/10 |

**Pass Condition**: Login attempts are limited to 5 per minute per IP. After limit, returns 429 status with retry-after header.

**Fail Condition**: No rate limiting, or limit too high (>10 per minute), or incorrect status code.

**Test Conditions**:
- **Happy Path**: Normal login within limits
- **Edge Cases**: Exactly at limit, burst requests
- **Error Cases**: Check response after limit exceeded

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [ ] Code review
- [ ] Performance testing

---

### Performance

#### AC5: Response Time

| Field | Value |
|-------|-------|
| **ID** | AC5 |
| **Name** | Response Time |
| **Description** | Authentication endpoints respond within acceptable time |
| **Category** | Performance |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Login and registration respond in under 500ms (p95) under normal load.

**Fail Condition**: Response time exceeds 500ms for p95, or timeouts occur.

**Test Conditions**:
- **Happy Path**: Measure response times under normal load
- **Edge Cases**: Under high load (100 concurrent requests)
- **Error Cases**: Measure timeout behavior

**Testing Method**:
- [ ] Manual testing
- [x] Automated tests
- [ ] Code review
- [x] Performance testing

---

### Reliability

#### AC6: Session Management

| Field | Value |
|-------|-------|
| **ID** | AC6 |
| **Name** | Session Management |
| **Description** | User sessions are properly created, validated, and terminated |
| **Category** | Reliability |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Sessions expire after 24 hours of inactivity. Logout invalidates session immediately. Concurrent sessions are handled correctly.

**Fail Condition**: Sessions don't expire, logout doesn't invalidate, or concurrent sessions cause errors.

**Test Conditions**:
- **Happy Path**: Login, wait, verify session behavior
- **Edge Cases**: Multiple concurrent sessions, session expiry at boundary
- **Error Cases**: Invalid session token, expired token

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

### Integration

#### AC7: OAuth Integration

| Field | Value |
|-------|-------|
| **ID** | AC7 |
| **Name** | OAuth Integration |
| **Description** | Users can authenticate via OAuth providers (Google, GitHub) |
| **Category** | Functional |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Users can log in via Google or GitHub OAuth. Profile information is correctly retrieved and stored.

**Fail Condition**: OAuth flow fails, profile not retrieved, or user created with wrong information.

**Test Conditions**:
- **Happy Path**: Complete OAuth flow with valid provider
- **Edge Cases**: User already exists with same email, OAuth provider unavailable
- **Error Cases**: Invalid OAuth state, expired tokens

**Testing Method**:
- [x] Manual testing
- [ ] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC8: Error Handling

| Field | Value |
|-------|-------|
| **ID** | AC8 |
| **Name** | Error Handling |
| **Description** | Authentication errors are handled gracefully with appropriate messages |
| **Category** | Reliability |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: All error cases return appropriate HTTP status codes (400, 401, 429, 500) with clear, actionable error messages. No stack traces in responses.

**Fail Condition**: Wrong status codes, vague error messages, or internal errors exposed to users.

**Test Conditions**:
- **Happy Path**: Verify correct status codes for known errors
- **Edge Cases**: Malformed requests, unexpected errors
- **Error Cases**: Database connection failures, external service failures

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

## Summary Table

| ID | Name | Priority | Threshold | Status |
|----|------|----------|-----------|--------|
| AC1 | User Registration | P1 | 7/10 | PENDING |
| AC2 | User Login | P1 | 7/10 | PENDING |
| AC3 | Password Security | P1 | 8/10 | PENDING |
| AC4 | Rate Limiting | P1 | 6/10 | PENDING |
| AC5 | Response Time | P2 | 6/10 | PENDING |
| AC6 | Session Management | P1 | 7/10 | PENDING |
| AC7 | OAuth Integration | P2 | 6/10 | PENDING |
| AC8 | Error Handling | P2 | 6/10 | PENDING |

---

## Evaluation Template

```markdown
## Evaluation Report: User Authentication

### Summary
- **Total Criteria**: 8
- **Passed**: {count}
- **Failed**: {count}
- **Overall Score**: {score}/10
- **Verdict**: PASS | FAIL

### Detailed Results

#### AC1: User Registration
- **Status**: PASS | FAIL
- **Score**: {score}/10
- **Evidence**: {What was tested and found}
- **Action**: {What to do if failed}
```
```

---

### Example 2: API Endpoint Criteria

**Input:**
```
criteria_name: REST API Endpoints
feature_description: CRUD operations for resource endpoints
domain: api
priority_level: P1
custom_requirements: Pagination, filtering, sorting support
```

**Output:**
```markdown
# Evaluation Criteria: REST API Endpoints

> Use these criteria to evaluate CRUD operations for resource endpoints
> **Key Principle**: If you can't write a test for it, it's not a criterion.

---

## Overview

| Field | Value |
|-------|-------|
| **Criteria Set** | rest-api-endpoints |
| **Feature** | CRUD operations for resource endpoints |
| **Domain** | api |
| **Total Criteria** | 10 |
| **Overall Priority** | P1 |

---

## Grading Scale

| Score | Rating | Description |
|-------|--------|-------------|
| 10/10 | Perfect | Exceeds expectations, exceptional quality |
| 9/10 | Excellent | Meets all criteria fully |
| 8/10 | Very Good | Meets criteria with minor edge cases |
| 7/10 | Good | Meets criteria well |
| 6/10 | Acceptable | Meets basic requirements |
| 5/10 | Marginal | Partial implementation |
| 4/10 | Below Standard | Missing key functionality |
| 3/10 | Poor | Major issues present |
| 2/10 | Very Poor | Critical failures |
| 1/10 | Fail | Not functional |
| 0/10 | No Attempt | Not implemented |

---

## Criteria

### CRUD Operations

#### AC1: List Resources

| Field | Value |
|-------|-------|
| **ID** | AC1 |
| **Name** | List Resources |
| **Description** | GET endpoint returns paginated list of resources |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: GET /resources returns 200 with array of resources, pagination metadata, and supports page/limit parameters.

**Fail Condition**: Returns wrong status code, no pagination, or missing metadata.

**Test Conditions**:
- **Happy Path**: GET /resources?page=1&limit=10 returns correct data
- **Edge Cases**: Empty list, large datasets, invalid pagination params
- **Error Cases**: Database unavailable, invalid query params

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC2: Create Resource

| Field | Value |
|-------|-------|
| **ID** | AC2 |
| **Name** | Create Resource |
| **Description** | POST endpoint creates new resource with validation |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: POST /resources with valid data returns 201 with created resource and Location header. Invalid data returns 400 with validation errors.

**Fail Condition**: Wrong status codes, no validation, or missing Location header.

**Test Conditions**:
- **Happy Path**: Create resource with valid JSON
- **Edge Cases**: Missing fields, extra fields, duplicate resources
- **Error Cases**: Invalid JSON, validation failures

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC3: Get Resource

| Field | Value |
|-------|-------|
| **ID** | AC3 |
| **Name** | Get Resource |
| **Description** | GET endpoint returns single resource by ID |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: GET /resources/:id returns 200 with resource for valid ID, 404 for non-existent ID.

**Fail Condition**: Wrong status codes, returns empty object, or exposes internal errors.

**Test Conditions**:
- **Happy Path**: Get existing resource
- **Edge Cases**: Invalid ID format, resource deleted
- **Error Cases**: Database unavailable

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC4: Update Resource

| Field | Value |
|-------|-------|
| **ID** | AC4 |
| **Name** | Update Resource |
| **Description** | PUT/PATCH endpoints update existing resource |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: PUT /resources/:id returns 200 with updated resource. PATCH supports partial updates. Returns 404 for non-existent resource.

**Fail Condition**: Wrong status codes, full update on PATCH, or no validation.

**Test Conditions**:
- **Happy Path**: Update with valid data
- **Edge Cases**: Partial update, no changes, concurrent updates
- **Error Cases**: Invalid data, non-existent resource

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC5: Delete Resource

| Field | Value |
|-------|-------|
| **ID** | AC5 |
| **Name** | Delete Resource |
| **Description** | DELETE endpoint removes resource |
| **Category** | Functional |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: DELETE /resources/:id returns 204 for success, 404 for non-existent resource. Resource is actually removed from database.

**Fail Condition**: Wrong status codes, resource not deleted, or can delete others' resources.

**Test Conditions**:
- **Happy Path**: Delete existing resource
- **Edge Cases**: Delete already deleted resource
- **Error Cases**: Non-existent resource, permission denied

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

### Query Features

#### AC6: Filtering

| Field | Value |
|-------|-------|
| **ID** | AC6 |
| **Name** | Filtering |
| **Description** | List endpoint supports filtering by resource fields |
| **Category** | Functional |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: GET /resources?field=value returns only matching resources. Multiple filters work together.

**Fail Condition**: Filtering doesn't work, SQL injection possible, or wrong results.

**Test Conditions**:
- **Happy Path**: Filter by single field
- **Edge Cases**: Multiple filters, no matches, special characters
- **Error Cases**: Invalid field names, SQL injection attempts

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC7: Sorting

| Field | Value |
|-------|-------|
| **ID** | AC7 |
| **Name** | Sorting |
| **Description** | List endpoint supports sorting by fields |
| **Category** | Functional |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: GET /resources?sort=field returns resources sorted by field. Supports ascending (-field) and descending (+field).

**Fail Condition**: Sorting doesn't work, invalid sort ignored silently, or wrong order.

**Test Conditions**:
- **Happy Path**: Sort by single field ascending
- **Edge Cases**: Sort descending, multiple sort fields, null values
- **Error Cases**: Invalid field name for sorting

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

### Error Handling

#### AC8: Validation Errors

| Field | Value |
|-------|-------|
| **ID** | AC8 |
| **Name** | Validation Errors |
| **Description** | Invalid requests return detailed validation errors |
| **Category** | Reliability |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 6/10 |

**Pass Condition**: Invalid requests return 400 with JSON body containing field-level error messages in consistent format.

**Fail Condition**: Generic errors, missing field info, or HTML error pages.

**Test Conditions**:
- **Happy Path**: Submit invalid data, verify error format
- **Edge Cases**: Multiple validation errors, nested object errors
- **Error Cases**: Malformed JSON, missing required fields

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC9: Authentication

| Field | Value |
|-------|-------|
| **ID** | AC9 |
| **Name** | Authentication |
| **Description** | Endpoints require valid authentication |
| **Category** | Security |
| **Priority** | P1 |
| **Weight** | High |
| **Threshold** | 7/10 |

**Pass Condition**: Requests without valid token return 401. Token can be in Authorization header. Expired tokens return 401 with clear message.

**Fail Condition**: No authentication, wrong status code, or token in URL.

**Test Conditions**:
- **Happy Path**: Valid token in Authorization header
- **Edge Cases**: Expired token, malformed token, no token
- **Error Cases**: Invalid signature, wrong audience

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [x] Code review
- [ ] Performance testing

---

#### AC10: Rate Limiting

| Field | Value |
|-------|-------|
| **ID** | AC10 |
| **Name** | Rate Limiting |
| **Description** | API endpoints are rate limited |
| **Category** | Security |
| **Priority** | P2 |
| **Weight** | Medium |
| **Threshold** | 6/10 |

**Pass Condition**: Requests exceeding rate limit return 429 with Retry-After header. Rate limit headers (X-RateLimit-*) are included in responses.

**Fail Condition**: No rate limiting, wrong status code, or no headers.

**Test Conditions**:
- **Happy Path**: Normal usage within limits
- **Edge Cases**: Exactly at limit, burst requests
- **Error Cases**: Exceed limit, verify retry-after

**Testing Method**:
- [x] Manual testing
- [x] Automated tests
- [ ] Code review
- [x] Performance testing

---

## Summary Table

| ID | Name | Priority | Threshold | Status |
|----|------|----------|-----------|--------|
| AC1 | List Resources | P1 | 7/10 | PENDING |
| AC2 | Create Resource | P1 | 7/10 | PENDING |
| AC3 | Get Resource | P1 | 7/10 | PENDING |
| AC4 | Update Resource | P1 | 7/10 | PENDING |
| AC5 | Delete Resource | P1 | 7/10 | PENDING |
| AC6 | Filtering | P2 | 6/10 | PENDING |
| AC7 | Sorting | P2 | 6/10 | PENDING |
| AC8 | Validation Errors | P1 | 6/10 | PENDING |
| AC9 | Authentication | P1 | 7/10 | PENDING |
| AC10 | Rate Limiting | P2 | 6/10 | PENDING |

---

## Evaluation Template

```markdown
## Evaluation Report: REST API Endpoints

### Summary
- **Total Criteria**: 10
- **Passed**: {count}
- **Failed**: {count}
- **Overall Score**: {score}/10
- **Verdict**: PASS | FAIL

### Detailed Results

#### AC1: List Resources
- **Status**: PASS | FAIL
- **Score**: {score}/10
- **Evidence**: {What was tested and found}
- **Action**: {What to do if failed}
```
```

---

## Anti-Patterns to Avoid

1. **Vague Criteria**: "Good UX" is not testable
2. **Missing Thresholds**: No pass/fail definition
3. **No Priority**: All criteria treated equally
4. **Untestable**: Can't gather objective evidence
5. **Overlap**: Same thing tested multiple times

---

## Integration Notes

After generating evaluation criteria:

1. Save to `.claude/evaluation/{criteria_name}-criteria.md`
2. Reference in sprint contract
3. Use during evaluation phase
4. Update as criteria evolve
5. Track criteria coverage in tests