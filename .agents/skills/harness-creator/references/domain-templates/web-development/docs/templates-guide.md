# Templates Guide

> Guide for using web development domain templates.

---

## Available Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `api-spec.md` | API endpoint documentation | Designing new API |
| `service-spec.md` | Service layer documentation | Creating new service |
| `db-schema.md` | Database schema documentation | Adding new table |
| `adr.md` | Architecture decision record | Making architectural decision |

---

## API Specification Template

### Purpose

Document API endpoints, requests, responses, and errors.

### When to Use

- Designing new API endpoints
- Documenting existing API
- Negotiating API contract between frontend and backend

### Who Uses It

- backend-lead: Creates and owns API specs
- frontend-lead: Reviews and approves frontend impact
- api-dev: Implements against spec

### Location

```
docs/api/[resource]-api.md
```

### Example

```
docs/api/
├── users-api.md        # User endpoints
├── orders-api.md       # Order endpoints
├── auth-api.md         # Authentication endpoints
```

### Key Sections

1. **Overview**: What the API provides
2. **Authentication**: Auth requirements
3. **Endpoints**: Each endpoint documented
4. **Data Models**: Request/response schemas
5. **Errors**: Error codes and messages

### Workflow

```
backend-lead creates draft
    -> frontend-lead reviews for frontend needs
    -> Negotiation if needed
    -> Both sign off
    -> api-dev implements
    -> backend-lead verifies implementation matches spec
```

---

## Service Specification Template

### Purpose

Document service layer business logic and methods.

### When to Use

- Creating new service
- Documenting existing service
- Reviewing service design

### Who Uses It

- backend-lead: Reviews and approves
- api-dev: Creates and owns service specs
- database-dev: Reviews repository usage

### Location

```
docs/services/[service]-spec.md
```

OR inline in service file docstring (for smaller services).

### Key Sections

1. **Overview**: What the service does
2. **Responsibilities**: Clear boundaries
3. **Dependencies**: What it needs
4. **Methods**: Each method documented
5. **Business Rules**: Logic rules enforced
6. **Error Handling**: Exceptions raised

### Workflow

```
api-dev creates draft spec
    -> backend-lead reviews architecture
    -> database-dev reviews repository usage
    -> backend-lead approves
    -> api-dev implements
```

---

## Database Schema Template

### Purpose

Document database tables, columns, indexes, and relationships.

### When to Use

- Adding new table
- Modifying existing schema
- Planning migrations

### Who Uses It

- backend-lead: Reviews and approves schema
- database-dev: Creates and owns schema docs

### Location

```
docs/architecture/schema/[table]-schema.md
```

### Key Sections

1. **Overview**: What the table stores
2. **Columns**: Each column documented
3. **Constraints**: PK, FK, unique
4. **Indexes**: Performance indexes
5. **Relationships**: Related tables
6. **Migration**: Alembic migration code

### Workflow

```
database-dev creates schema proposal
    -> backend-lead reviews for API impact
    -> architect-lead reviews if cross-domain
    -> backend-lead approves
    -> database-dev creates migration
    -> Migration tested
    -> Applied
```

---

## Architecture Decision Record Template

### Purpose

Document significant architectural decisions with rationale.

### When to Use

- Choosing technology
- Making architectural change
- Changing design patterns
- Any decision affecting multiple domains

### Who Uses It

- architect-lead: Creates and owns ADRs
- All leads: Consulted on cross-domain ADRs

### Location

```
docs/architecture/adr/ADR-[number]-[title].md
```

### Example

```
docs/architecture/adr/
├── ADR-001-postgres.md      # Database choice
├── ADR-002-redis.md         # Caching choice
├── ADR-003-rest-api.md      # API style choice
├── ADR-004-monorepo.md      # Repo structure
```

### Key Sections

1. **Context**: Why decision needed
2. **Decision**: What was decided
3. **Alternatives**: Options considered
4. **Rationale**: Why this choice
5. **Consequences**: Impact
6. **Implementation**: How to implement

### Workflow

```
architect-lead identifies decision needed
    -> Consults affected leads
    -> Creates ADR proposal
    -> Leads review
    -> architect-lead finalizes
    -> Document approved decision
```

---

## Template Usage Patterns

### Pattern 1: New Feature

```
1. architect-lead creates feature plan
2. backend-lead creates API spec
3. frontend-lead reviews API spec
4. database-dev creates schema doc
5. All specs approved
6. Implementation begins
```

### Pattern 2: Architecture Change

```
1. architect-lead creates ADR proposal
2. All leads consulted
3. ADR finalized
4. Implementation plan created
5. Changes implemented
```

### Pattern 3: Bug Fix

```
1. Bug identified
2. Root cause found
3. Fix designed (may need mini-spec)
4. Fix implemented
5. Tests verify fix
```

---

## Template Quality Checklist

### API Spec Checklist

- [ ] All endpoints documented
- [ ] Request schemas defined
- [ ] Response schemas defined
- [ ] Error responses documented
- [ ] Authentication noted
- [ ] Examples provided

### Service Spec Checklist

- [ ] Clear responsibilities
- [ ] Methods documented
- [ ] Dependencies listed
- [ ] Errors documented
- [ ] Business rules noted

### Schema Doc Checklist

- [ ] All columns documented
- [ ] Constraints listed
- [ ] Indexes justified
- [ ] Relationships mapped
- [ ] Migration reversible

### ADR Checklist

- [ ] Context clear
- [ ] Alternatives considered
- [ ] Rationale explained
- [ ] Consequences documented
- [ ] Implementation planned

---

## Integration with Skills

Templates are used by skills:

| Skill | Template Used |
|-------|---------------|
| `feature-plan` | All templates (coordinated) |
| `api-design` | api-spec.md |
| `refactor` | ADR if significant |
| `code-review` | Template as reference |

---

## Template Maintenance

### Review Schedule

| Template | Review Frequency |
|----------|-----------------|
| API specs | With each API change |
| Service specs | With each service change |
| Schema docs | With each migration |
| ADRs | Never (historical) |

### Update Responsibility

| Template | Owner |
|----------|-------|
| API spec | backend-lead |
| Service spec | api-dev |
| Schema doc | database-dev |
| ADR | architect-lead |

---

## Best Practices

1. **Create before code**: Document before implementing
2. **Review before approve**: Peer review on all specs
3. **Keep updated**: Update docs with code changes
4. **Archive ADRs**: Never delete, supersede instead
5. **Version control**: All templates in git