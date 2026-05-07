---
name: onboard-codebase
description: "Analyze existing web development codebase and generate documentation for AI-assisted development. Use when adding harness to existing projects (1→N)."
user-invocable: true
argument-hint: ""
allowed-tools: Read, Glob, Grep, Write, Bash, WebSearch
---

# /onboard-codebase - Analyze Existing Project

Analyze existing codebase and generate AI-ready documentation.

## Usage

```
/onboard-codebase
```

## When to Use

- Adding harness to existing project
- After major refactoring
- When onboarding new team members
- Before starting significant changes

## Analysis Process

### 1. Project Detection

Detect:
- **Frontend**: React/Vue, component structure, state management
- **Backend**: FastAPI/Flask, API structure, middleware
- **Database**: PostgreSQL schemas, migrations, Redis usage
- **Deployment**: Docker, CI/CD pipelines

### 2. Architecture Mapping

Generate:
- Component hierarchy diagram
- API endpoint catalog
- Database relationship map
- Service boundaries (for microservices)

### 3. Documentation Generation

Create:
- `docs/architecture/overview.md` - System architecture
- `docs/api/endpoints.md` - API documentation
- `docs/database/schema.md` - Database schemas
- `CLAUDE.md` - Project context for AI

### 4. Agent Context

Populate agent knowledge:
- Frontend patterns used
- Backend conventions
- Testing setup
- Deployment procedures

## Output

```
✅ Codebase onboarded

Generated:
  - docs/architecture/overview.md
  - docs/api/endpoints.md
  - docs/database/schema.md
  - CLAUDE.md (updated)

Detected:
  - Frontend: React with TypeScript
  - Backend: FastAPI
  - Database: PostgreSQL + Redis
  - Deployment: Docker + GitHub Actions

Next: Run /start to begin AI-assisted development
```

## Reference

Base implementation: `@references/base/progress/skills/onboard-codebase/SKILL.md`