---
name: feature-plan
description: "Coordinate full feature development across frontend, backend, and database modules. Creates comprehensive plan with task breakdown and agent assignments."
user-invocable: true
---

# Feature Plan Skill

You are facilitating the Feature Planning process. Your role is to coordinate planning across all development domains for a complete feature implementation.

## Purpose

Feature planning ensures:
- All domains (frontend, backend, database) are considered
- Tasks are properly delegated to appropriate agents
- Dependencies between components are identified
- API contracts are established before implementation

## Planning Flow

```
USER REQUEST -> REQUIREMENTS ANALYSIS -> DOMAIN BREAKDOWN -> TASK ASSIGNMENT -> APPROVAL
```

## Planning Workflow

### Phase 1: Requirements Analysis

1. Parse the user's feature request
2. Identify core functionality requirements
3. Document edge cases and error scenarios
4. List acceptance criteria

### Phase 2: Domain Breakdown

For each domain, identify what's needed:

**Frontend (frontend-lead/frontend-dev):**
- New pages or components
- State management changes
- API integration hooks
- UI/UX updates

**Backend (backend-lead/api-dev):**
- New endpoints
- Service layer changes
- Authentication requirements
- Business logic

**Database (backend-lead/database-dev):**
- Schema changes
- New migrations
- Query optimization needs
- Data relationships

**DevOps (devops-dev):**
- Environment changes
- New services/containers
- CI/CD updates

### Phase 3: Task Assignment

Assign tasks to appropriate agents:

| Domain | Lead Agent | Implementer |
|--------|------------|-------------|
| Frontend UI | frontend-lead | frontend-dev |
| Backend API | backend-lead | api-dev |
| Database | backend-lead | database-dev |
| Infrastructure | architect-lead | devops-dev |

### Phase 4: Dependency Mapping

Identify dependencies between tasks:

```
[Task A] -> [Task B] -> [Task C]
```

Common dependency patterns:
- Database schema -> API endpoints -> Frontend components
- Auth changes -> Protected routes -> UI updates

### Phase 5: API Contract Definition

Before implementation, define:
- Endpoint URLs and methods
- Request/response schemas
- Error response formats
- Authentication requirements

### Phase 6: Approval Request

Present plan to user for approval:
- Summary of changes
- Estimated complexity
- Risk areas
- Implementation order

## Plan Template

```markdown
# Feature Plan: [Feature Name]

## Overview
[2-3 sentence description]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Domain Breakdown

### Frontend
- [x] Component: [Name] (frontend-dev)
- [x] Page: [Name] (frontend-dev)
- [x] Hook: [Name] (frontend-dev)

### Backend
- [x] Endpoint: [Method] [Path] (api-dev)
- [x] Service: [Name] (api-dev)

### Database
- [x] Schema: [Table] (database-dev)
- [x] Migration: [Name] (database-dev)

### DevOps
- [x] Container: [Service] (devops-dev)

## API Contracts

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| [Path]   | [M]    | [Schema]| [Schema] |

## Dependencies
```
[Task 1] -> [Task 2] -> [Task 3]
```

## Implementation Order
1. [Step 1 - typically database]
2. [Step 2 - typically backend]
3. [Step 3 - typically frontend]

## Risks
- [Risk 1]
- [Risk 2]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

## Good vs Bad Planning

### Good Planning
- Clear task boundaries
- Explicit agent assignments
- API contracts defined before code
- Dependencies mapped

### Bad Planning
- Vague task descriptions
- Missing agent assignments
- API contracts left undefined
- Dependencies ignored

## Usage

```
/feature-plan [feature description]
```

Example:
```
/feature-plan Add user profile page with avatar upload
```

## Coordination Rules

1. architect-lead reviews plans affecting multiple domains
2. frontend-lead and backend-lead approve domain-specific changes
3. API contracts must be approved by both leads before implementation
4. Database schema changes require backend-lead approval