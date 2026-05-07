# Phase 6: Confirm

Final review and approval before generation.

## Purpose

Present complete generation preview and obtain user approval.

## Input from All Previous Phases

```yaml
discovery:
  path: [target-path]
  type: [new|existing]

vision:
  name: [project-name]
  purpose: [description]
  success_criteria: [list]

tech_stack:
  language: [primary]
  frontend: [framework|null]
  backend: [framework|null]
  database: [type|null]

architecture:
  type: [single|monorepo|microservices]
  structure: [description]

customize:
  agents: [configuration]
  skills: [configuration]
  hooks: [configuration]
  rules: [configuration]
```

## Generation Preview

### Full Structure Preview

```
[target-path]/
├── .claude/
│   ├── settings.json          # Permissions + hooks config
│   ├── agents/
│   │   ├── planner.md         # Plans implementation
│   │   ├── generator.md       # Implements code
│   │   ├── evaluator.md       # Grades output
│   │   └── [specialized...]   # Domain-specific
│   ├── skills/
│   │   ├── start/SKILL.md     # Onboarding
│   │   ├── checkpoint/SKILL.md # Save progress
│   │   ├── resume/SKILL.md    # Restore context
│   │   ├── sprint-contract/SKILL.md
│   │   └── [domain...]        # Domain-specific
│   ├── hooks/
│   │   └── [hook-files]       # Automated checks
│   ├── rules/
│   │   └── [rule-files]       # Code standards
│   ├── evaluation/
│   │   └── criteria.md        # Evaluation criteria
│   └── docs/
│       └── templates/
│           ├── sprint-contract.md
│           └── handoff-artifact.md
├── production/
│   ├── session-state/         # Progress tracking
│   │   ├── active.md
│   │   └ handoffs/
│   └── session-logs/          # Session history
└── CLAUDE.md                  # Master configuration
```

### Summary Table

```
## Generation Summary

| Category | Count | Description |
|----------|-------|-------------|
| Agents | [X] | Core + specialized |
| Skills | [X] | Essential + optional |
| Hooks | [X] | Automated checks |
| Rules | [X] | Code standards |
| Templates | [X] | Document templates |

**Total files:** [X]
**Estimated setup time:** [X minutes]
```

### Configuration Summary

```markdown
## Your Harness Configuration

### Project Info
- **Name:** [project-name]
- **Type:** [type]
- **Architecture:** [architecture]

### Tech Stack
- **Language:** [language]
- **Frontend:** [framework or "none"]
- **Backend:** [framework or "none"]
- **Database:** [type or "none"]

### Multi-Agent Setup
- **Core:** Planner → Generator → Evaluator
- **Specialized:** [list or "none"]
- **Coordination:** [orchestrator or "single-project"]

### Evaluation Criteria
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

### Automation
- **Hooks:** [hook list]
- **Rules:** [scope list]
```

## Approval Questions

### Final Confirmation

```
This is the final step. I will generate:

[X] agents
[X] skills
[X] hooks
[X] rules
[X] templates
[X] settings.json
[X] CLAUDE.md

Total: [X] files in [target-path]/.claude/

Proceed? [Yes/No/Modify]
```

### If No

```
What would you like to change?
A) Add/remove components
B) Adjust configuration
C) Start over
D) Cancel generation
```

### If Modify

Return to appropriate phase:
- Component changes → Phase 5: Customize
- Architecture changes → Phase 4: Architecture
- Tech changes → Phase 3: Tech
- Vision changes → Phase 2: Vision

## Migration Detection

If target has existing `.claude/`:

```
Existing harness detected at [path]/.claude/

Options:
A) Replace entirely (backup old)
B) Merge (keep existing, add new)
C) View differences first
D) Cancel (keep existing)

[Selection]
```

## Generation Command

Once approved, generate files:

```bash
# Create directories
mkdir -p [target]/.claude/{agents,skills,hooks,rules,evaluation,docs/templates}
mkdir -p [target]/production/{session-state/handoffs,session-logs}

# Generate files from references
# [generation logic]
```

## Post-Generation Guidance

```
Harness generated successfully!

Next steps:
1. cd [target-path]
2. Start Claude Code session
3. Run /start to initialize context

Your harness is configured for:
- [architecture] architecture
- [tech stack] development
- [agent setup] multi-agent coordination

Documentation:
- CLAUDE.md - Main configuration
- .claude/docs/ - Detailed guides

Happy coding!
```

## Sprint Contract Fulfillment

Before generation, confirm all phases completed:

```
Phase Checklist:
[x] Phase 1: Discovery
[x] Phase 2: Vision
[x] Phase 3: Tech Stack
[x] Phase 4: Architecture
[x] Phase 5: Customize
[x] Phase 6: Confirm

All decisions captured. Ready to generate.
```

## Output

Final output is the actual generated harness files, not just configuration.

```yaml
confirm:
  approved: true
  generation_complete: true
  target_path: [path]
  files_generated: [count]
  next_steps: [guidance list]
```