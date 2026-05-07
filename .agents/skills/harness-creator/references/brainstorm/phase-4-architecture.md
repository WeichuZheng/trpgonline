# Phase 4: Architecture

Decide project structure and multi-agent coordination.

## Purpose

Determine the architectural pattern and how multiple projects/services will coordinate.

## Input from Previous Phases

```yaml
vision:
  type: [web-app|api|cli|library|other]
  scope: [minimal|standard|full]

tech_stack:
  frontend: [framework|null]
  backend: [framework|null]
  database: [type|null]
```

## Architecture Options

### Single Project

```
project/
├── src/
│   ├── frontend/
│   ├── backend/
│   └── shared/
├── tests/
├── .claude/
└── CLAUDE.md
```

**Best for:**
- Small to medium projects
- Single developer or small team
- Quick iteration
- Timeline < 3 months

**Trade-offs:**
- Simpler coordination
- Shared context
- Can become monolithic

### Monorepo

```
project/
├── apps/
│   ├── web/
│   ├── api/
│   └── mobile/
├── packages/
│   ├── shared/
│   └── ui/
├── .claude/
│   ├── agents/
│   └── skills/
└── CLAUDE.md
```

**Best for:**
- Multiple related projects
- Shared components/packages
- Team collaboration
- Timeline 3+ months

**Trade-offs:**
- More complex coordination
- Better code sharing
- Requires multi-project harness

### Microservices

```
services/
├── user-service/
│   ├── src/
│   └── .claude/
├── order-service/
│   ├── src/
│   └── .claude/
├── api-gateway/
├── shared/
│   └── contracts/
└── docker-compose.yml
```

**Best for:**
- Large scale systems
- Independent deployment needs
- Multiple teams
- Clear service boundaries

**Trade-offs:**
- Complex coordination
- Independent harness per service
- Contract management needed

## Decision Questions

### 1. Project Scope

```
How many deployable units will this project have?
A) One (frontend + backend together)
B) 2-5 (monorepo with shared packages)
C) 6+ (microservices architecture)
D) Not sure yet
```

### 2. Team Structure

```
How will development be organized?
A) Single developer (me)
B) Small team (2-5 people)
C) Multiple teams with different focuses
```

### 3. Scaling Needs

```
What are your scaling requirements?
A) Simple deployment (single server)
B) Horizontal scaling (multiple instances)
C) Service isolation (separate scaling per component)
```

### 4. Coordination Needs

```
How much do components need to share?
A) Minimal - standalone components
B) Moderate - shared utilities, types
C) Extensive - shared business logic
```

## Multi-Agent Architecture

Based on architecture choice, configure agent coordination:

### Single Project Agents

```
┌─────────────┐
│   Planner   │
│   (1 agent) │
└──────┬──────┘
       │
┌──────▼──────┐
│  Generator  │
│   (1 agent) │
└──────┬──────┘
       │
┌──────▼──────┐
│  Evaluator  │
│   (1 agent) │
└─────────────┘
```

### Multi-Project Agents

```
┌─────────────┐     ┌─────────────┐
│   Planner   │────►│ Orchestrator│
│  (per proj) │     │  (1 agent)  │
└─────────────┘     └──────┬──────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
         ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
         │Service A│ │Service B│ │Shared   │
         │Generator│ │Generator│ │Generator│
         └────┬────┘ └────┬────┘ └────┬────┘
              │           │           │
         ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
         │Evaluator│ │Evaluator│ │Evaluator│
         └─────────┘ └─────────┘ └─────────┘
```

## Harness Components by Architecture

| Component | Single | Monorepo | Microservices |
|-----------|--------|----------|---------------|
| Core agents | Standard | Standard | Standard |
| Orchestrator | - | Optional | Required |
| Cross-service skills | - | Optional | Required |
| Contract sync | - | Optional | Required |
| Shared context | Single file | Multi-file | Contract files |

## Output to Next Phase

```yaml
architecture:
  type: [single|monorepo|microservices]
  structure:
    apps: [list of app directories]
    packages: [list of shared packages]
    services: [list of services]
  agents:
    core: [planner, generator, evaluator]
    coordination: [orchestrator|null]
    per_project: [list of project-specific agents]
  skills:
    cross_service: [api-contract-sync|null]
    shared_context: [true|false]
```

## Sprint Contract

```
Architecture Decision:
- Type: [single|monorepo|microservices]
- Structure: [description]
- Agents: [count] coordinating agents

This determines:
- Directory structure
- Cross-project coordination skills
- Context management approach

Proceed to customization? [Yes/Back]
```