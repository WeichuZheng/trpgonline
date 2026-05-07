# Coordination Map

> Agent coordination rules and communication patterns for web development domain.

---

## Agent Hierarchy

```
                    [Human Developer]
                           |
                   architect-lead
                           |
           +---------------+---------------+
           |               |               |
     frontend-lead    backend-lead
           |               |
     +-----+-----+   +-----+-----+
     |           |   |           |
  frontend-dev  api-dev    database-dev
       
                    devops-dev
                    (infrastructure)
```

---

## Coordination Rules

### Rule 1: Vertical Delegation

**Definition**: Leads delegate to Specialists. Never skip tiers for complex decisions.

**Example**:
```
architect-lead -> backend-lead -> api-dev (correct)
architect-lead -> api-dev (incorrect - skipped backend-lead)
```

**When to Apply**: All non-trivial tasks must go through proper chain.

---

### Rule 2: Horizontal Consultation

**Definition**: Agents at the same tier may consult each other but must not make binding decisions outside their domain.

**Example**:
```
frontend-lead consults backend-lead about API design
frontend-lead cannot mandate backend changes to backend-lead
```

**When to Apply**: Cross-domain planning, API contracts, integration points.

---

### Rule 3: Conflict Resolution

**Definition**: When two Leads disagree, escalate to architect-lead.

**Escalation Path**:
```
frontend-lead disagrees with backend-lead
    -> Both present arguments
    -> architect-lead decides
    -> Document in ADR
```

**When to Apply**: API contract disputes, architecture disagreements, priority conflicts.

---

### Rule 4: Change Propagation

**Definition**: When a change affects multiple modules, architect-lead coordinates propagation.

**Workflow**:
```
1. architect-lead identifies affected domains
2. architect-lead notifies all affected leads
3. Leads plan changes in their domains
4. architect-lead reviews combined changes
5. Changes deployed in coordinated sequence
```

**When to Apply**: Breaking API changes, schema changes, auth changes.

---

### Rule 5: No Unilateral Cross-Domain Changes

**Definition**: An agent must never modify files outside their designated directories without explicit delegation.

**Domain Boundaries**:
| Agent | Directories |
|-------|-------------|
| frontend-lead/frontend-dev | `src/frontend/`, `tests/frontend/` |
| backend-lead/api-dev | `src/backend/api/`, `src/backend/services/` |
| backend-lead/database-dev | `src/backend/models/`, `src/backend/repository/`, `migrations/` |
| devops-dev | `docker/`, `.github/workflows/`, `scripts/` |
| architect-lead | `docs/architecture/`, ADRs |

**Cross-Domain Requires**: Explicit delegation from owning agent or architect-lead approval.

---

## Communication Patterns

### Pattern 1: Feature Planning

```
User Request -> architect-lead
    -> frontend-lead (UI impact)
    -> backend-lead (API impact)
    -> database-dev (Schema impact)
    -> devops-dev (Infrastructure impact)
    
All report back to architect-lead
architect-lead creates unified plan
```

### Pattern 2: API Contract Negotiation

```
frontend-lead proposes API needs
    -> backend-lead reviews feasibility
    -> Negotiation loop
    -> Agreement
    -> Document in api-spec.md
    -> Both sign off
```

### Pattern 3: Bug Fix Coordination

```
Bug reported
    -> Domain identification
    -> Domain lead assigns to specialist
    -> Fix implemented
    -> Lead reviews
    -> Cross-domain impacts checked
    -> Merge
```

### Pattern 4: Release Coordination

```
architect-lead initiates release
    -> All leads verify domain readiness
    -> devops-dev prepares deployment
    -> Tests run
    -> All leads approve
    -> Deploy
```

---

## Decision Authority

### architect-lead Authority

| Decision | Authority Level |
|----------|-----------------|
| Architecture changes | FINAL |
| Cross-domain conflicts | FINAL |
| Technology choices | FINAL (after consultation) |
| Release timing | FINAL |

### frontend-lead Authority

| Decision | Authority Level |
|----------|-----------------|
| Frontend architecture | FINAL |
| Component design | FINAL |
| UI/UX decisions | FINAL (consult backend for API needs) |
| Frontend dependencies | FINAL |

### backend-lead Authority

| Decision | Authority Level |
|----------|-----------------|
| Backend architecture | FINAL |
| API design | FINAL (consult frontend for needs) |
| Service design | FINAL |
| Backend dependencies | FINAL |
| Database schema | FINAL |

### Specialist Authority

| Decision | Authority Level |
|----------|-----------------|
| Implementation details | FINAL (within spec) |
| Bug fixes | FINAL (lead review) |
| Code refactoring | NEEDS LEAD APPROVAL |
| Adding dependencies | NEEDS LEAD APPROVAL |

---

## Consultation Requirements

### frontend-lead Must Consult backend-lead

- New API endpoints needed
- API contract changes
- Data format changes
- Auth requirements

### backend-lead Must Consult frontend-lead

- Breaking API changes
- Response format changes
- New endpoints proposed
- Error format changes

### backend-lead Must Consult database-dev

- Schema changes
- Migration planning
- Performance optimization

### All Leads Must Consult architect-lead

- Breaking changes
- Cross-domain changes
- Architecture decisions
- Technology additions

---

## Agent Interactions Table

| From | To | Action | Approval |
|------|-----|--------|----------|
| frontend-dev | frontend-lead | Report completion | Required |
| frontend-lead | backend-lead | Propose API need | Consultation |
| backend-lead | frontend-lead | Propose API change | Approval required |
| backend-lead | database-dev | Request schema change | Delegation |
| architect-lead | All leads | Initiate change | Directive |

---

## Anti-Patterns

### Anti-Pattern 1: Skipping Leads

```
frontend-dev directly talks to backend-lead
    -> backend-lead should redirect to frontend-lead
    -> frontend-lead then coordinates with backend-lead
```

### Anti-Pattern 2: Unilateral Cross-Domain

```
frontend-dev modifies backend files
    -> Should be blocked
    -> Requires explicit delegation
```

### Anti-Pattern 3: Silent Changes

```
backend-lead changes API without telling frontend-lead
    -> Should be blocked
    -> Requires coordination
```

---

## Communication Channels

### Primary Channels

| Channel | Use |
|---------|-----|
| Document artifacts | Formal decisions, specs |
| Session messages | Real-time coordination |
| Review requests | Code review, approval |
| Status updates | Progress reports |

### Artifact Types

| Artifact | Created By | Reviewed By |
|----------|------------|-------------|
| Feature plan | architect-lead | All leads |
| API spec | backend-lead | frontend-lead |
| ADR | architect-lead | All leads |
| Service spec | backend-lead | architect-lead |
| Component spec | frontend-lead | architect-lead |