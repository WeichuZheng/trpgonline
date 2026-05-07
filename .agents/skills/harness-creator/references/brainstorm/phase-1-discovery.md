# Phase 1: Discovery

Analyze target directory to understand project context.

## Purpose

Gather information about the target project to determine the appropriate generation path.

## Auto-Analysis Checklist

When target directory is provided, automatically check:

### Directory State
- [ ] Empty directory (0→1 new project)
- [ ] Has existing code (1→N enhancement)
- [ ] Has existing `.claude/` (migration needed?)

### Project Detection (if code exists)

**Package Managers:**
- `package.json` → Node.js/JavaScript/TypeScript
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `pom.xml` / `build.gradle` → Java
- `Gemfile` → Ruby

**Framework Indicators:**
- `next.config.js` → Next.js
- `nuxt.config.js` → Nuxt
- `vue.config.js` → Vue
- `angular.json` → Angular
- `django/settings.py` → Django
- `fastapi` in deps → FastAPI

**Architecture Indicators:**
- `apps/` + `packages/` → Monorepo
- `services/` → Microservices
- Single `src/` → Single project
- `docker-compose.yml` → Containerized

## Analysis Report Template

After analysis, present to user:

```markdown
## Project Analysis

**Path:** [target-path]
**Type:** [new|existing]

### Detected (if existing)
- **Language:** [detected language]
- **Framework:** [detected framework or "none"]
- **Architecture:** [single|monorepo|microservices]
- **Package Manager:** [npm|yarn|pnpm|pip|poetry|etc]

### Confidence
- [ ] High - Clear detection, proceed to customization
- [ ] Medium - Some ambiguity, ask clarifying questions
- [ ] Low - Manual input needed

### Recommendations
- [Brief recommendation based on analysis]
```

## Questions for User

**If empty directory:**
```
This appears to be a new project. Would you like to:
A) Create a new project from scratch (0→1 flow)
B) Initialize harness for future project planning
```

**If detection confidence is medium:**
```
I detected [X] but want to confirm:
- Is this a [detected-type] project?
- Are you using [detected-framework]?
```

**If detection confidence is low:**
```
I couldn't determine the project type. Please tell me:
- What language/framework are you using?
- Is this a single project, monorepo, or microservices?
```

## Decision Matrix

| Condition | Next Phase |
|-----------|------------|
| Empty directory + new project | Phase 2: Vision |
| Existing project + high confidence | Phase 5: Customize |
| Existing project + medium confidence | Ask questions → Phase 5 |
| Existing project + low confidence | Ask questions → Phase 3 |
| Migration from existing `.claude/` | Phase 6: Confirm (show diff) |

## Output to Next Phase

Pass to Phase 2 (Vision) or Phase 5 (Customize):

```yaml
discovery:
  path: [target-path]
  type: [new|existing]
  detected:
    language: [language|null]
    framework: [framework|null]
    architecture: [single|monorepo|microservices|null]
    package_manager: [manager|null]
  confidence: [high|medium|low]
  user_confirmed: [true|false]
```

## Sprint Contract

Before proceeding, confirm with user:

```
Based on my analysis: [summary]

Does this look correct? I'll use this to customize your harness.
[Yes/No/Adjust]
```

This ensures alignment before investing in generation.