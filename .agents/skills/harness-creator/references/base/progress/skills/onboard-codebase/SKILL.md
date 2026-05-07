---
name: onboard-codebase
description: "Analyze and document existing codebase for AI-assisted development. Use when adding this framework to an existing project."
user-invocable: true
---

# Onboard Codebase Skill

You are analyzing an existing codebase to create AI-ready documentation. This enables effective AI-assisted development on established projects.

## Purpose

Onboarding enables:
- AI understanding of existing architecture
- Context-aware code generation
- Consistent style adherence
- Safe modifications to existing code

## Onboarding Flow

```
/onboard-codebase
     |
     +--[1] Discovery
     |       - Scan project structure
     |       - Identify technologies
     |       - Detect conventions
     |
     +--[2] Documentation
     |       - Create CLAUDE.md
     |       - Generate architecture docs
     |       - Document patterns
     |
     +--[3] Integration
             - Configure .claude/ directory
             - Set up hooks
             - Create initial checkpoint
```

## Discovery Phase

### Step 1: Project Structure Analysis

```
PROJECT STRUCTURE

Root: [project root]
Type: [web/api/library/cli/etc.]

Directories:
- src/ ([purpose])
- tests/ ([purpose])
- docs/ ([purpose])
- [other directories]

Key files:
- package.json / requirements.txt
- CLAUDE.md (exists/missing)
- README.md
- [config files]
```

### Step 2: Technology Detection

```markdown
TECHNOLOGY STACK

Frontend:
- Framework: [React/Vue/Angular/etc.]
- Language: [TypeScript/JavaScript]
- Styling: [CSS/Tailwind/Styled/etc.]
- State: [Redux/Vuex/Context/etc.]

Backend:
- Framework: [FastAPI/Flask/Express/etc.]
- Language: [Python/Node/etc.]
- Database: [PostgreSQL/Mongo/etc.]
- Cache: [Redis/Memcached/etc.]

Infrastructure:
- Container: [Docker/K8s/etc.]
- CI/CD: [GitHub Actions/Jenkins/etc.]
- Cloud: [AWS/GCP/Azure/etc.]
```

### Step 3: Convention Detection

```markdown
DETECTED CONVENTIONS

Code Style:
- [Language] linter: [detected config]
- Formatter: [Prettier/Black/etc.]
- Import style: [ESM/CommonJS/etc.]

Naming:
- Files: [kebab-case/PascalCase/etc.]
- Components: [PascalCase]
- Functions: [camelCase/snake_case]
- Constants: [UPPER_SNAKE]

Patterns:
- API style: [REST/GraphQL/RPC]
- Auth: [JWT/Session/OAuth/etc.]
- Error handling: [pattern]
- Testing: [Jest/Pytest/etc.]
```

### Step 4: Architecture Mapping

```
ARCHITECTURE OVERVIEW

Entry Points:
- [entry point 1]: [purpose]
- [entry point 2]: [purpose]

Core Modules:
- [module 1]: [purpose]
- [module 2]: [purpose]

Data Flow:
[User] -> [Entry] -> [Handler] -> [Service] -> [Data] -> [Storage]

Key Dependencies:
- [dependency 1]: [purpose]
- [dependency 2]: [purpose]
```

## Documentation Phase

### CLAUDE.md Generation

Create or update `CLAUDE.md`:

```markdown
# [Project Name] - AI Development Guide

## Project Overview

[Brief description from README or analysis]

## Technology Stack

[From technology detection]

## Project Structure

[From structure analysis]

## Key Conventions

[From convention detection]

## Development Workflow

### Getting Started
[detected setup commands]

### Development
[detected dev commands]

### Testing
[detected test commands]

### Build/Deploy
[detected build commands]

## Architecture Notes

[From architecture mapping]

## AI Collaboration Notes

### Code Generation Guidelines
- Follow existing patterns
- Use detected conventions
- Maintain consistency with [detected style]

### Areas of Caution
- [Sensitive areas]
- [Complex modules]
- [Known issues]

## Session State Location
- Checkpoints: .claude/checkpoints/
- Handoffs: .claude/handoff.md
- Session: .claude/session-state.md
```

### Architecture Documentation

Create `docs/architecture/`:

```markdown
# Architecture Decision Records

## ADR-001: [First Major Decision]

### Context
[Why this decision was made]

### Decision
[What was decided]

### Consequences
[Impact of this decision]

## ADR-002: [Second Major Decision]
...
```

### Pattern Documentation

Create `docs/patterns/`:

```markdown
# Code Patterns

## API Pattern
[Detected API pattern with examples]

## Error Handling Pattern
[Detected error handling with examples]

## Data Access Pattern
[Detected data access pattern]

## Testing Pattern
[Detected testing conventions]
```

## Integration Phase

### Step 1: Create .claude Directory

```
.claude/
  settings.json         # Permissions and hooks
  checkpoints/          # Session checkpoints
  handoff.md            # Context reset handoff
  session-state.md      # Active session state
```

### Step 2: Configure settings.json

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Write", "Bash"],
    "deny": []
  },
  "hooks": {
    "session-start": ".claude/hooks/session-start.sh",
    "session-stop": ".claude/hooks/session-stop.sh"
  }
}
```

### Step 3: Create Initial Checkpoint

```markdown
# Initial Checkpoint: Onboarding Complete

## Context
- Onboarded: [timestamp]
- Technology: [stack summary]
- Structure: [architecture summary]

## Next Steps
- Begin development work
- Use /start for session initialization
- Use /checkpoint to save progress

## Known Areas
- [area 1]: [notes]
- [area 2]: [notes]
```

## Output Format

```
ONBOARDING COMPLETE

Project: [name]
Type: [web/api/library]
Technologies: [count] detected
Conventions: [count] documented

Created:
- CLAUDE.md (AI development guide)
- docs/architecture/ (decision records)
- docs/patterns/ (code patterns)
- .claude/ (session management)

Next Steps:
1. Review generated CLAUDE.md
2. Add project-specific notes
3. Begin using AI assistance
4. Run /start to begin session

Onboarding saved to checkpoint: cp-onboard-[timestamp]
```

## Usage

```
/onboard-codebase                    # Full onboarding
/onboard-codebase --quick            # Quick scan, minimal docs
/onboard-codebase --update           # Update existing documentation
/onboard-codebase --tech-only        # Document technology only
/onboard-codebase --patterns-only    # Document patterns only
```

## Interactive Options

During onboarding, you may be asked:

```
MULTIPLE CONFIG FILES DETECTED

Found:
- .eslintrc.json
- .eslintrc.js
- package.json (eslintConfig)

Which should be authoritative?
[1] .eslintrc.json
[2] .eslintrc.js
[3] package.json
[4] Merge all
```

```
UNCLEAR ARCHITECTURE

Multiple patterns detected:
- MVC (controllers/, models/, views/)
- Layered (api/, services/, data/)
- Modular (modules/, shared/)

Which best describes this project?
[1] MVC
[2] Layered
[3] Modular
[4] Custom (describe)
```

## Integration Points

- **With /start**: Uses onboarded documentation for session context
- **With /checkpoint**: Creates initial checkpoint after onboarding
- **With sprint-contract**: Informs contract creation with project context

## Error Handling

```
ONBOARDING FAILED

Error: [error description]
Recovery: [suggested fix]

Partial results saved to: .claude/onboard-partial.md
Manual intervention may be needed.
```