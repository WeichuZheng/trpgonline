# Phase 5: Customize

Select harness components and multi-agent architecture features.

## Purpose

Finalize which agents, skills, hooks, and rules to include in the generated harness.

## Input from Previous Phases

```yaml
discovery:
  path: [target-path]
  type: [new|existing]

vision:
  type: [web-app|api|cli|library|other]
  success_criteria: [list]
  scope: [minimal|standard|full]

tech_stack:
  language: [primary]
  frontend: [framework|null]
  backend: [framework|null]

architecture:
  type: [single|monorepo|microservices]
  agents: [configuration]
```

## Component Categories

### Required (All Projects)

| Component | Purpose | Included |
|-----------|---------|----------|
| `planner.md` | Plans implementation | Always |
| `generator.md` | Implements code | Always |
| `evaluator.md` | Grades output | Always |
| `start/SKILL.md` | Session onboarding | Always |
| `checkpoint/SKILL.md` | Save progress | Always |
| `resume/SKILL.md` | Restore context | Always |
| `sprint-contract/SKILL.md` | Define "done" | Always |
| Safety rules | Code safety | Always |

### Optional (User Choice)

| Component | Purpose | Recommend For |
|-----------|---------|---------------|
| Orchestrator agent | Multi-project coord | Monorepo/Microservices |
| Domain agents | Specialized roles | Complex projects |
| `code-review/SKILL.md` | Quality reviews | Teams |
| `feature-plan/SKILL.md` | Full feature planning | Web apps |
| `api-design/SKILL.md` | API workflow | Backend-heavy |
| `deploy-check/SKILL.md` | Pre-deploy validation | Production apps |
| CI hooks | Automated checks | CI/CD pipelines |

### Domain-Specific (Based on Tech)

| Domain | Components |
|--------|------------|
| Web Development | `frontend-design`, `feature-plan`, `code-review` |
| API/Backend | `api-design`, `db-migrate`, `regression-test` |
| CLI/Library | `test-driven-development`, `docs-generation` |

## Customization Questions

### 1. Core Multi-Agent Architecture

```
The base harness uses Planner→Generator→Evaluator.

Would you like to customize the agent roles?
A) Use standard roles (recommended for most projects)
B) Add domain-specific agents (e.g., frontend-specialist, backend-specialist)
C) Configure orchestrator for multi-project coordination
```

**If B selected:**
```
Which specialized agents would help your workflow?
- Frontend specialist (React/Vue focused)
- Backend specialist (API/database focused)
- DevOps specialist (Docker/deployment focused)
- QA specialist (Testing focused)
- [Other - describe]
```

### 2. Skills Selection

```
Which workflow skills do you need?

Essential (included by default):
- /start - Onboarding and context loading
- /checkpoint - Save progress
- /resume - Restore from checkpoint
- /sprint-contract - Define "done" criteria

Optional (select what applies):
□ /feature-plan - Coordinate feature development
□ /code-review - Architecture and quality review
□ /api-design - API specification workflow
□ /db-migrate - Database migration workflow
□ /deploy-check - Pre-deployment validation
□ /hotfix - Emergency fix workflow
□ /refactor - Guided refactoring
□ /release - Release workflow
```

### 3. Hooks and Automation

```
What automated checks should run?

□ Pre-commit: Lint/format validation
□ Pre-push: Test execution
□ Post-merge: Dependency updates
□ Custom: [describe your need]
```

### 4. Rules Configuration

```
Code quality rules by scope:

□ Global rules (apply to all files)
□ Frontend rules (React/Vue patterns)
□ Backend rules (API patterns)
□ Database rules (migration safety)
□ Custom rules for: [specify directories]
```

### 5. Evaluation Criteria

From Phase 2 success criteria, generate evaluation template:

```markdown
## Evaluation Criteria

Generated from your success criteria:

| Criterion | Measurable Standard | Grade |
|-----------|--------------------|-------|
| [criterion 1] | [how to measure] | Pass/Fail |
| [criterion 2] | [how to measure] | Pass/Fail |
| [criterion 3] | [how to measure] | Pass/Fail |

Would you like to adjust these? [Yes/Keep as is]
```

## Component Preview

Show what will be generated:

```
## Harness Preview

### Agents (X total)
- planner.md - [description]
- generator.md - [description]
- evaluator.md - [description]
- [additional agents...]

### Skills (X total)
- start/SKILL.md
- checkpoint/SKILL.md
- [additional skills...]

### Hooks (X total)
- [hook list]

### Rules (X total)
- [rule list]

### Templates (X total)
- sprint-contract.md
- handoff-artifact.md
- [additional templates...]
```

## Output to Next Phase

```yaml
customize:
  agents:
    core: [planner, generator, evaluator]
    specialized: [list of additional agents]
    orchestrator: [true|false]
  skills:
    essential: [start, checkpoint, resume, sprint-contract]
    optional: [list of selected optional skills]
  hooks:
    pre_commit: [true|false]
    pre_push: [true|false]
    custom: [list]
  rules:
    global: [true]
    scopes: [list of scoped rules]
  evaluation:
    criteria: [list of evaluation criteria]
    template: [evaluation-criteria.md]
```

## Quick Setup Path

For existing projects with high confidence detection:

```
Quick setup detected. Recommended configuration:

[Show recommended components based on detected tech]

Customize? [Yes/Use recommended]
```

## Sprint Contract

```
Final harness configuration:
- Agents: [count]
- Skills: [count]
- Hooks: [count]
- Rules: [count]

This will generate the following structure:
[preview structure]

Ready to proceed to final confirmation? [Yes/Back]
```