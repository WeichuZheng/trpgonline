---
name: api-contract-sync
description: "Keeps API contracts synchronized between frontend and backend services. Detects contract drift, generates client SDKs, and manages API versioning."
user-invocable: true
---

# API Contract Sync Skill

You are facilitating API contract synchronization between frontend and backend services. Your role is to ensure that API contracts remain consistent across all consumers and producers.

## Purpose

API contract drift causes:
- Runtime errors in production
- Wasted debugging time
- Broken integrations
- Delayed releases

This skill prevents drift by:
- Maintaining a single source of truth for contracts
- Detecting drift between specification and implementation
- Generating client SDKs from contracts
- Managing API versions consistently

## When to Use

- After backend API changes
- Before frontend development starts
- When adding new API consumers
- During API versioning
- When debugging integration issues
- Regular contract health checks

## Contract Sync Workflow

### Phase 1: Contract Discovery

1. **Identify All Contracts**
   - OpenAPI/Swagger specifications
   - gRPC/Protobuf definitions
   - GraphQL schemas
   - Event schemas (JSON Schema, Avro)

2. **Map Contract Sources**
   ```markdown
   ## Contract Registry
   
   | Contract | Producer | Consumers | Version | Location |
   |----------|----------|-----------|---------|----------|
   | User API | user-service | frontend-app, mobile-app | v1.2.0 | /specs/user-api.yaml |
   | Order API | order-service | frontend-app, analytics | v2.0.0 | /specs/order-api.yaml |
   | User Events | user-service | notification, analytics | v1.0.0 | /schemas/user-events.avsc |
   ```

3. **Validate Contract Completeness**
   - All endpoints documented
   - All request/response schemas defined
   - All error responses documented
   - Authentication requirements specified

### Phase 2: Drift Detection

1. **Compare Specification vs Implementation**
   ```markdown
   ## Drift Detection Report
   
   ### User API (user-service)
   
   | Endpoint | Spec | Implementation | Status |
   |----------|------|----------------|--------|
   | GET /users | Documented | Exists | OK |
   | POST /users | Documented | Exists | DRIFT |
   | DELETE /users/{id} | Not documented | Exists | MISSING_IN_SPEC |
   | GET /users/search | Documented | Not found | MISSING_IN_IMPL |
   
   ### DRIFT Details: POST /users
   - Spec: request.body.email (required)
   - Impl: request.body.email (optional)
   - Impact: Frontend validation may be too strict
   ```

2. **Detect Breaking Changes**
   ```markdown
   ## Breaking Change Detection
   
   ### user-service: v1.1.0 -> v1.2.0
   
   | Change | Breaking | Affected Consumers |
   |--------|----------|-------------------|
   | Added required field `phone` to User | YES | frontend-app |
   | Removed endpoint GET /users/legacy | YES | analytics-service |
   | Added optional field `avatar` to User | NO | - |
   | Changed `/users/search` to `/users?q=` | YES | mobile-app |
   
   ### Action Required
   1. Notify frontend-app about required field
   2. Verify analytics-service doesn't use legacy endpoint
   3. Update mobile-app for search endpoint change
   ```

3. **Generate Drift Report**
   ```markdown
   ## Contract Drift Summary
   
   - **Total Contracts**: 5
   - **With Drift**: 2
   - **Breaking Changes**: 3
   - **Missing Documentation**: 4
   
   ### Priority Fixes
   1. [HIGH] user-service: Breaking change affects 2 consumers
   2. [MEDIUM] order-service: Missing documentation for 3 endpoints
   3. [LOW] notification-service: Minor schema drift
   ```

### Phase 3: Contract Alignment

1. **Resolve Drift**
   ```markdown
   ## Resolution Options
   
   ### Option 1: Update Specification (Prefer for Missing Documentation)
   - Update spec to match implementation
   - Notify consumers of documented behavior
   - Update SDKs
   
   ### Option 2: Update Implementation (Prefer for Breaking Changes)
   - Revert breaking changes in implementation
   - Add new endpoint/version instead
   - Maintain backward compatibility
   
   ### Option 3: Version Bump (Prefer for Intentional Changes)
   - Create new API version
   - Support both versions during transition
   - Migrate consumers incrementally
   - Deprecate old version
   ```

2. **Generate Client SDKs**
   ```markdown
   ## SDK Generation
   
   ### Frontend SDK (TypeScript)
   ```bash
   openapi-generator generate \
     -i specs/user-api.yaml \
     -g typescript-axios \
     -o clients/frontend/user-api
   ```
   
   ### Mobile SDK (Swift)
   ```bash
   openapi-generator generate \
     -i specs/user-api.yaml \
     -g swift5 \
     -o clients/ios/user-api
   ```
   
   ### Mobile SDK (Kotlin)
   ```bash
   openapi-generator generate \
     -i specs/user-api.yaml \
     -g kotlin \
     -o clients/android/user-api
   ```
   ```

3. **Validate SDK Compatibility**
   ```markdown
   ## SDK Validation Checklist
   
   - [ ] Generated types match spec
   - [ ] All endpoints callable
   - [ ] Error types correct
   - [ ] Authentication headers included
   - [ ] TypeScript types compile
   - [ ] Example requests work
   ```

### Phase 4: Version Management

1. **Version Strategy**
   ```markdown
   ## API Versioning Strategy
   
   ### URL Path Versioning (Preferred)
   - /api/v1/users
   - /api/v2/users
   
   ### Header Versioning (Alternative)
   - Accept: application/vnd.api+json;version=1
   
   ### Version Lifecycle
   | Phase | Duration | Support Level |
   |-------|----------|---------------|
   | Current | Active | Full support, new features |
   | Deprecated | 6 months | Security fixes only |
   | Retired | N/A | No support |
   ```

2. **Deprecation Process**
   ```markdown
   ## Deprecation Checklist
   
   ### Announce Deprecation
   - [ ] Add `deprecated: true` to spec
   - [ ] Add `Deprecation` header in responses
   - [ ] Add `Sunset` header with removal date
   - [ ] Notify all consumers
   
   ### Migration Period
   - [ ] Provide migration guide
   - [ ] Offer both versions in parallel
   - [ ] Monitor usage of deprecated version
   - [ ] Support consumers during migration
   
   ### Removal
   - [ ] Verify no consumers using deprecated version
   - [ ] Remove deprecated endpoints
   - [ ] Update documentation
   - [ ] Archive old SDKs
   ```

## Contract Template

```yaml
# api-contract.yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.2.0
  description: User management service
  
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api-staging.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
          
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
          
  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## Drift Detection Script

```bash
#!/bin/bash
# drift-check.sh - Check for API drift

CONTRACTS_DIR="specs"
IMPLEMENTATIONS_DIR="src"

for spec in "$CONTRACTS_DIR"/*.yaml; do
  service=$(basename "$spec" .yaml)
  
  echo "Checking $service..."
  
  # Compare spec with implementation
  diff-output=$(diff \
    <(yq eval '.paths | keys' "$spec") \
    <(grep -r "router\." "$IMPLEMENTATIONS_DIR/$service" | grep -oP '(?<=["'"'"']).+(?=["'"'"'])' | sort -u)
  )
  
  if [ -n "$diff-output" ]; then
    echo "DRIFT DETECTED in $service:"
    echo "$diff-output"
  fi
done
```

## Usage

```
/api-contract-sync [service-name]
```

This will:
1. Scan all API specifications
2. Compare with implementations
3. Detect drift and breaking changes
4. Generate drift report
5. Suggest resolution options
6. Generate client SDKs if needed

## Automation Integration

### CI/CD Pipeline

```yaml
# .github/workflows/api-contract-check.yml
name: API Contract Check

on:
  pull_request:
    paths:
      - 'specs/**'
      - 'src/**/routes/**'

jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install tools
        run: npm install -g @apidevtools/swagger-cli
        
      - name: Validate specs
        run: |
          for spec in specs/*.yaml; do
            swagger-cli validate "$spec"
          done
          
      - name: Check for drift
        run: ./scripts/drift-check.sh
        
      - name: Generate SDKs
        run: ./scripts/generate-sdks.sh
        
      - name: Upload SDKs
        uses: actions/upload-artifact@v3
        with:
          name: generated-sdks
          path: clients/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Check for API drift before committing

if git diff --cached --name-only | grep -q "specs/"; then
  echo "API specs changed, running drift check..."
  ./scripts/drift-check.sh
  if [ $? -ne 0 ]; then
    echo "API drift detected. Please resolve before committing."
    exit 1
  fi
fi
```