# Harness Creator

English | [中文](README_CN.md)

> Generate a customized Claude Code harness framework with Fusion Architecture: GAN-inspired multi-agent system + Domain Specialists.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://claude.ai)

---

## What is Harness Creator?

Harness Creator is a meta-framework that generates customized `.claude/` harness structures for AI-assisted software development. It implements Anthropic's best practices for long-running agent tasks with an enhanced Fusion Architecture.

### Key Features

- **Fusion Architecture**: GAN-inspired core + Domain Specialists
- **One-Click Customized Harness**: Auto-detect project type and domain
- **Domain Templates**: Pre-defined templates for web, game, data science, etc.
- **Dynamic Specialist Generation**: Support for any new domain
- **Sprint Contract Mechanism**: Negotiate "done" criteria before implementation
- **Context Reset Protocol**: Structured handoffs for long-running tasks

---

![Fusion Architecture](images/fusion-architecture.svg)

### Three Layers

| Layer | Agents | Responsibility |
|-------|--------|----------------|
| **Decision** | Planner, architect-lead | Product & Architecture decisions |
| **Execution** | Generator, [domain]-dev | Implement features |
| **Evaluation** | Evaluator | Test and grade implementation |

### Why Separation Matters

Models cannot reliably evaluate their own work. When a single agent both builds and reviews:

- Praises mediocre output as "complete"
- Skips edge cases and error handling
- Misses integration issues
- Accepts incomplete solutions

**The solution**: Separate generation and evaluation, delegate to specialists.

---

## Quick Start

### Installation

```bash
npx skills add https://github.com/fanlw0816/harness-creator --skill harness-creator
```

### Usage

```
/harness-creator [target-directory]
```

### Example Session

```
> /harness-creator ./my-game

## Project Analysis

**Path:** ./my-game
**Type:** Game Development (Unity detected)

## Recommended Configuration

Core Agents:
  Planner        - Product planning
  Generator      - Coordinate execution
  Evaluator      - Quality assessment
  architect-lead - Architecture decisions

Specialists:
  [√] gameplay-dev    Game logic, mechanics, AI
  [√] graphics-dev    Rendering, shaders, effects
  [√] audio-dev       Sound system, music
  [√] ui-dev          Game UI, HUD, menus

Options:
  A) Use recommended
  B) Adjust selection
  C) Add custom specialist

> A

Harness generated at ./my-game/.claude/
```

---

## Domain Templates

### Supported Domains

| Domain | Specialists |
|--------|-------------|
| **Web Development** | frontend-dev, api-dev, database-dev, devops-dev |
| **Game Development** | gameplay-dev, graphics-dev, audio-dev, ui-dev |
| **Data Science** | data-engineer, ml-engineer, data-analyst |
| **Mobile App** | ios-dev, android-dev, backend-dev |
| **Custom** | Dynamically generated based on project structure |

### Template Structure

```
domain-templates/
├── web-development/
│   ├── template.yaml
│   └── specialists/
│       ├── frontend-dev.yaml
│       └── api-dev.yaml
├── game-development/
│   └── ...
└── _dynamic/                    # Dynamic generation
    ├── specialist-template.yaml
    └── detection-rules.yaml
```

### Adding New Domains

1. Create template directory: `domain-templates/your-domain/`
2. Define `template.yaml` with detection rules
3. Add specialist definitions in `specialists/*.yaml`

---

## Sprint Contract

### The Contract Lifecycle

```
1. PROPOSE     Generator proposes contract (with specialist assignments)
      |
      v
2. REVIEW      architect-lead reviews architecture
      |         Evaluator reviews testability
      v
3. NEGOTIATE   Back-and-forth until agreement
      |
      v
4. APPROVE     All parties sign off
      |
      v
5. IMPLEMENT   Generator coordinates specialists
      |
      v
6. EVALUATE    Evaluator grades against contract
      |
      v
7. ITERATE     If FAIL: fix issues, re-evaluate
```

### Contract Structure

```markdown
# Sprint Contract: [Feature Name]

## Scope
- What, In Scope, Out of Scope

## Architecture Decision
- Specialists Involved
- Cross-Domain Boundaries

## Testable Behaviors
- [ ] B1.1: [Behavior] | Owner: [specialist]

## Acceptance Criteria
| ID | Criterion | Pass | Fail | Priority | Owner |

## Responsibility Matrix
| Criterion | Responsible | Fallback |
```

---

## Generated Harness Structure

```
<target-dir>/
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── planner.md
│   │   ├── generator.md          # + Agent tool
│   │   ├── evaluator.md
│   │   ├── architect-lead.md
│   │   └── [domain]-dev.md
│   ├── skills/
│   │   ├── start/
│   │   ├── checkpoint/
│   │   ├── resume/
│   │   ├── sprint-contract/
│   │   └── [domain-specific]/
│   ├── hooks/
│   ├── rules/
│   ├── evaluation/
│   └── docs/
├── production/
│   ├── session-state/
│   └── session-logs/
└── CLAUDE.md
```

---

## Key Principles

1. **Generator-Evaluator Separation**: Never the same agent
2. **Sprint Contract First**: Negotiate "done" before building
3. **Domain Specialists**: Delegated by Generator, specialized implementation
4. **Context Reset**: Use handoff artifacts for long tasks
5. **Concrete Criteria**: Convert subjective to gradable

---

## Reference Architecture

```
harness-creator/
├── SKILL.md
├── references/
│   ├── base/
│   │   ├── core/
│   │   │   ├── agents/            # planner, generator, evaluator
│   │   │   ├── skills/            # sprint-contract
│   │   │   └── templates/
│   │   ├── progress/              # start, checkpoint, resume
│   │   ├── evaluator/             # evaluate-feature, evaluate-code
│   │   ├── safety/                # hooks, rules
│   │   └── settings/
│   ├── brainstorm/
│   ├── customizer/
│   └── domain-templates/
│       ├── web-development/
│       ├── game-development/
│       ├── data-science/
│       └── _dynamic/
```

---

## Reference

Design based on [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)

---

## License

MIT License - See [LICENSE](LICENSE) for details.