# Phase 3: Tech Stack

Select technologies based on project requirements.

## Purpose

Choose the technology stack that best fits the project vision and constraints.

## Input from Previous Phase

```yaml
vision:
  type: [web-app|api|cli|library|other]
  target_users: [b2c|b2b|developers|personal]
  timeline: [duration]
  scope: [minimal|standard|full]
```

## Recommendation Flow

### For Web Applications

```
Frontend Options:
┌─────────────────────────────────────────────────────────────────┐
│ Option     │ Pros                    │ Cons                    │
├─────────────┼─────────────────────────┼─────────────────────────┤
│ React      │ Ecosystem, jobs, flex   │ Bundle size, decisions │
│ Vue        │ Simple, great DX        │ Smaller ecosystem      │
│ Svelte     │ Fast, simple            │ Newer, smaller ecosystem│
│ Next.js    │ SSR, routing, full-stack│ React dependency       │
│ Nuxt       │ SSR, Vue-based          │ Less resources than Next│
└─────────────────────────────────────────────────────────────────┘

Backend Options:
┌─────────────────────────────────────────────────────────────────┐
│ Option     │ Pros                    │ Cons                    │
├─────────────┼─────────────────────────┼─────────────────────────┤
│ Node.js    │ JS everywhere, fast dev │ CPU-bound perf          │
│ Python     │ AI/ML libs, readable    │ Slower runtime          │
│ FastAPI    │ Fast, async, typed      │ Smaller ecosystem       │
│ Go         │ Fast, simple, typed     │ More boilerplate        │
│ Rust       │ Fastest, safe           │ Steep learning curve    │
└─────────────────────────────────────────────────────────────────┘
```

### For APIs

```
Framework Options:
┌─────────────────────────────────────────────────────────────────┐
│ Option     │ Best For                │ Trade-offs              │
├─────────────┼─────────────────────────┼─────────────────────────┤
│ FastAPI    │ Python, typed APIs      │ Newer framework         │
│ Express    │ Node.js, flexibility    │ More decisions needed  │
│ Django     │ Full-featured, ORM      │ Heavier, slower         │
│ Go Fiber   │ Performance              │ Less ecosystem          │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Questions

### 1. Language Preference

```
Do you have a language preference?
A) TypeScript/JavaScript
B) Python
C) Go
D) Rust
E) Other: [specify]
F) No preference - recommend based on project
```

### 2. Database Needs

```
What are your data requirements?
A) Relational (PostgreSQL, MySQL)
B) Document store (MongoDB)
C) Key-value cache (Redis)
D) Graph (Neo4j)
E) Multiple / Not sure yet
```

### 3. Deployment Target

```
Where will this run?
A) Vercel / Netlify (frontend-focused)
B) AWS / GCP / Azure (full control)
C) Docker containers
D) Bare metal / VPS
E) Not sure yet
```

### 4. Existing Expertise

```
What's your team comfortable with?
[List detected or ask]

This affects:
- Code style rules
- Documentation depth
- Testing approach
```

## Recommendation Engine

Based on inputs, provide recommendation:

```markdown
## Recommended Stack

Based on [vision type] for [users] with [timeline] timeline:

**Frontend:** [recommendation]
- Reason: [why]

**Backend:** [recommendation]
- Reason: [why]

**Database:** [recommendation]
- Reason: [why]

**Deployment:** [recommendation]
- Reason: [why]

Alternatives considered: [list]
```

## Harness Impact

Tech choices determine:

| Choice | Harness Customization |
|--------|----------------------|
| TypeScript | ESLint rules, type checking hooks |
| Python | Black/mypy rules, pytest setup |
| React | Component rules, testing-library |
| FastAPI | Pydantic models, async patterns |
| PostgreSQL | Migration skills, SQL rules |
| Docker | Dockerfile templates, compose setup |

## Output to Next Phase

```yaml
tech_stack:
  language: [primary language]
  frontend:
    framework: [framework|null]
    build_tool: [vite|webpack|next|nuxt|null]
  backend:
    framework: [framework|null]
    style: [rest|graphql|grpc]
  database:
    primary: [type|null]
    cache: [type|null]
  deployment:
    target: [platform]
    containerized: [true|false]
  expertise: [team expertise level]
```

## Sprint Contract

```
Recommended stack:
- Frontend: [choice]
- Backend: [choice]
- Database: [choice]

This affects which agents and skills I'll include.
Does this look right? [Yes/Adjust/Explain options]
```