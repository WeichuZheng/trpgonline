# Fusion Architecture Design

> GAN-inspired Multi-Agent System + Domain Specialists Integration
> Version: 2.0
> Date: 2024-04-07

---

## Overview

Harness Creator 是一个**生成器**，根据不同场景、领域、项目生成一套 harness 配置。

本文档描述两个系统的融合设计：

1. **Core GAN Architecture**: Planner → Generator → Evaluator
2. **Domain Specialists**: 根据领域动态配置的专业实现者

---

## Core Principle: GAN at Control Layer

GAN 概念（Generator-Evaluator 分离）应用在**控制层**，而非每个领域内部。

```
Control Layer: Generator → spawns specialists → Evaluator evaluates whole
Domain Layer: Specialists only generate, never evaluate
```

---

## Architecture

### Layer Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Decision Layer                                  │
│                                                                         │
│  Planner ─────────── 产品决策 (WHAT)│
│  architect-lead ───── 架构决策 (HOW) [Contract阶段参与]│
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          Execution Layer                                 │
│                                                                         │
│  Generator ─────────── 协调者，spawn specialist(+ Agent 工具)         │
│    ├─ [domain]-dev    受委托，只生成                       │
│    ├─ [domain]-dev    受委托，只生成                       │
│    └─ [domain]-dev    受委托，只生成                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          Evaluation Layer                                │
│                                                                         │
│  Evaluator ─────────── 评估整体，不委托                              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Layer | Role | Tools |
|-------|-------|------|-------|
| Planner | Decision | 产品规划 | Read, Glob, Grep, Write, WebSearch |
| architect-lead | Decision | Contract阶段架构审核 | Read, Glob, Grep, Write, Edit, Bash |
| Generator | Execution | 协调执行，spawn specialist | **+Agent**, Read, Glob, Grep, Write, Edit, Bash |
| [domain]-dev | Execution | 领域实现 | Read, Glob, Grep, Write, Edit, Bash |
| Evaluator | Evaluation | 评估实现 | Read, Glob, Grep, Write, Bash |

---

## Domain Template System

### 混合模式：预定义模板 + 动态生成

```
/harness-creator ./my-project
        │
        ▼
┌─────────────────────────────┐
│ 1. 项目分析                 │
│    - 检测技术栈             │
│    - 检测目录结构           │
│    - 用户描述项目类型       │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│ 2. 领域匹配                 │
│    预定义模板库:            │
│    ├── web-development      │
│    ├── game-development     │
│    ├── data-science         │
│    ├── mobile-app           │
│    └── ...                  │
└─────────────────────────────┘
        │
        ├─────────────┴─────────────┐
        ▼                           ▼
┌──────────────────┐      ┌──────────────────┐
│ 匹配到模板       │      │ 无匹配           │
│                  │      │                  │
│ → 使用预定义     │      │ → 动态生成       │
│ → 可调整         │      │                  │
└──────────────────┘      └──────────────────┘
        │                           │
        └─────────────┬─────────────┘
                      ▼
              ┌──────────────────┐
              │ 3. 用户确认       │
              │                  │
              │ 展示specialist列表│
              │ 用户可增/删/改    │
              └──────────────────┘
                      │
                      ▼
              ┌──────────────────┐
              │ 4. 生成 harness  │
              └──────────────────┘
```

---

## Domain Template Structure

```
domain-templates/
├── web-development/
│   ├── template.yaml              # 模板配置
│   ├── specialists/               # Specialist 定义
│   │   ├── frontend-dev.yaml
│   │   ├── api-dev.yaml
│   │   ├── database-dev.yaml
│   │   └── devops-dev.yaml
│   ├── skills/
│   ├── rules/
│   └── evaluation/
│
├── game-development/
│   ├── template.yaml
│   ├── specialists/
│   │   ├── gameplay-dev.yaml
│   │   ├── graphics-dev.yaml
│   │   ├── audio-dev.yaml
│   │   └── ui-dev.yaml
│   └── ...
│
├── data-science/
│   ├── template.yaml
│   ├── specialists/
│   │   ├── data-engineer.yaml
│   │   ├── ml-engineer.yaml
│   │   └── data-analyst.yaml
│   └── ...
│
└── _dynamic/                      # 动态生成模板
    ├── specialist-template.yaml   # 通用 specialist 模板
    └── detection-rules.yaml       # 推断规则
```

---

## Template Configuration (template.yaml)

```yaml
# domain-templates/game-development/template.yaml

template:
  name: game-development
  version: 1.0.0
  description: "Game development with Unity/Unreal/Godot"

  # 匹配条件
  detection:
    files: ["*.unity", "*.gd", "*.uproject"]
    directories: ["Assets/", "Scripts/", "Prefabs/"]
    dependencies: ["unity", "unreal", "godot"]
    keywords: ["game", "unity", "unreal", "godot"]

  # 核心角色（固定）
  core_agents:
    - planner
    - generator    # 带 Agent 工具
    - evaluator
    - architect-lead

  # 领域 Specialists（可调整）
  specialists:
    - name: gameplay-dev
      source: ./specialists/gameplay-dev.yaml
    - name: graphics-dev
      source: ./specialists/graphics-dev.yaml
    - name: audio-dev
      source: ./specialists/audio-dev.yaml
    - name: ui-dev
      source: ./specialists/ui-dev.yaml

  # 领域特定 skills
  skills:
    - level-design
    - asset-pipeline
    - performance-profile

  # 领域特定 rules
  rules:
    - game-code
    - asset-organization

  # 领域特定 evaluation
  evaluation:
    - gameplay-criteria
    - performance-criteria

  # 生成的目录结构
  structure:
    directories:
      - Scripts/Gameplay
      - Scripts/Graphics
      - Scripts/Audio
      - Assets/Shaders
      - Assets/Audio
```

---

## Specialist Definition Format

```yaml
# domain-templates/game-development/specialists/gameplay-dev.yaml

# 基本信息
name: gameplay-dev
description: "Specialist agent for gameplay logic, mechanics, and AI implementation"

# 委托模式（融合架构核心）
delegation:
  mode: spawned_by_generator    # 由 Generator spawn
  contract_required: true       # 需要有 sprint contract
  can_modify_contract: false    # 不能修改 contract
  report_issues_to: generator   # 问题报告给 Generator

# 领域边界
domain_scope:
  directories:
    - "Scripts/Gameplay/"
    - "Scripts/Mechanics/"
    - "Scripts/AI/"
  files:
    - "*.cs"      # Unity C#
    - "*.gd"      # Godot GDScript
  excludes:
    - "Scripts/Graphics/"
    - "Scripts/Audio/"

# 职责
responsibilities:
  - Implement game mechanics and rules
  - Create state machines for game objects
  - Implement AI behavior trees
  - Handle player input and controls
  - Manage game state and progression

# 领域原则
key_principles:
  - principle: "State-First"
    description: "Define states before behavior"
  - principle: "Separation"
    description: "Logic separate from presentation"
  - principle: "Performance"
    description: "Target 60fps minimum"

# 工作流程
workflow:
  - step: receive_task
    from: generator
    description: "Receive delegated task from Generator"
  - step: read_spec
    description: "Read specification from contract"
  - step: implement
    description: "Implement the feature"
  - step: test
    description: "Test in editor/runtime"
  - step: submit
    to: generator
    description: "Submit output to Generator"

# 质量检查
quality_checklist:
  - "Mechanic works as designed"
  - "No performance regression (check FPS)"
  - "State transitions are smooth"
  - "AI behaves predictably"
  - "No hardcoded magic numbers"

# 反模式
anti_patterns:
  - pattern: "rendering_in_gameplay"
    description: "Don't put rendering code in gameplay scripts"
  - pattern: "hardcoded_values"
    description: "Don't hardcode magic numbers, use ScriptableObjects"
  - pattern: "blocking_main_thread"
    description: "Don't block main thread with heavy calculations"

# 与其他 specialist 的边界
boundaries:
  - with: graphics-dev
    rule: "Gameplay triggers events, Graphics handles visual response"
  - with: audio-dev
    rule: "Gameplay triggers events, Audio handles sound response"
  - with: ui-dev
    rule: "Gameplay exposes state, UI displays it"
```

---

## Dynamic Generation Logic

当无匹配模板时，动态创建 specialists：

### 推断规则

```yaml
# domain-templates/_dynamic/detection-rules.yaml

# 从目录结构推断领域
directory_to_specialist:
  - pattern: "src/frontend/**|src/components/**|src/ui/**"
    suggests: frontend-dev
  - pattern: "src/api/**|src/routes/**|src/controllers/**"
    suggests: api-dev
  - pattern: "src/models/**|migrations/**|db/**"
    suggests: database-dev
  - pattern: "Scripts/Gameplay/**|src/mechanics/**"
    suggests: gameplay-dev
  - pattern: "Scripts/Graphics/**|shaders/**|assets/shaders/**"
    suggests: graphics-dev
  - pattern: "src/audio/**|assets/audio/**"
    suggests: audio-dev
  - pattern: "src/ml/**|models/**|notebooks/**"
    suggests: ml-engineer
  - pattern: "src/data/**|pipelines/**"
    suggests: data-engineer

# 从文件类型推断
file_type_to_specialist:
  - extensions: [".tsx", ".jsx", ".vue", ".svelte"]
    suggests: frontend-dev
  - extensions: [".cs", ".gd"]
    context:
      - in_directory: "Scripts/Graphics"
        suggests: graphics-dev
      - in_directory: "Scripts/Audio"
        suggests: audio-dev
      - default: gameplay-dev
  - extensions: [".py"]
    context:
      - in_directory: "src/api"
        suggests: api-dev
      - in_directory: "models"
        suggests: ml-engineer
      - default: backend-dev
```

### 动态生成模板

```yaml
# domain-templates/_dynamic/specialist-template.yaml

# 动态生成 specialist 的基础模板
name: "{{area}}-dev"
description: "Specialist agent for {{area}} implementation"

delegation:
  mode: spawned_by_generator
  contract_required: true
  can_modify_contract: false
  report_issues_to: generator

# 以下字段从推断 + 用户确认填充
domain_scope:
  directories: []   # 从项目分析推断
  files: []         # 从文件类型推断

responsibilities: []  # 从领域知识 + 用户输入生成

key_principles: []    # 从领域知识生成

workflow:
  - step: receive_task
    from: generator
  - step: read_spec
  - step: implement
  - step: test
  - step: submit
    to: generator

quality_checklist: []  # 通用检查项

anti_patterns: []      # 从领域知识生成
```

---

## Sprint Contract (Enhanced)

```markdown
# Sprint Contract: [Feature Name]

> Contract Version: 2.0 (Fusion Architecture)
> Created: [DATE]
> Status: DRAFT | PENDING_REVIEW | APPROVED | IN_PROGRESS | COMPLETED

---

## Scope

### What
[Feature description]

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Item 1]

### Dependencies
- [Dependency 1]

---

## Architecture Decision

### architect-lead: [Name]

### Specialists Involved
| Specialist | Tasks | Domain Scope |
|------------|-------|--------------|
| gameplay-dev | Player movement | Scripts/Gameplay/Player/ |
| graphics-dev | Movement VFX | Scripts/Graphics/Effects/ |
| audio-dev | Footstep sounds | Scripts/Audio/Player/ |

### Cross-Domain Boundaries
- Event: PlayerMovedEvent (gameplay → graphics + audio)
- Interface: IMovementController (gameplay defines, implements)

---

## Testable Behaviors

### Gameplay
- [ ] **B1.1**: Player moves with WASD | Owner: gameplay-dev
- [ ] **B1.2**: Movement speed is 5 units/sec | Owner: gameplay-dev

### Graphics
- [ ] **B2.1**: Dust particles on movement | Owner: graphics-dev

### Audio
- [ ] **B3.1**: Footstep sounds play on movement | Owner: audio-dev

---

## Acceptance Criteria

| ID | Criterion | Pass | Fail | Priority | Owner |
|----|-----------|------|------|----------|-------|
| AC1 | Player moves correctly | Smooth movement | Jerky/stuck | P1 | gameplay-dev |
| AC2 | VFX plays | Particles visible | No particles | P2 | graphics-dev |

---

## Responsibility Matrix

| Criterion | Responsible | Fallback |
|-----------|-------------|----------|
| B1.1 | gameplay-dev | Generator |
| B2.1 | graphics-dev | Generator |
| B3.1 | audio-dev | Generator |

---

## Negotiation Log

| Round | Party | Action | Notes |
|-------|-------|--------|-------|
| 1 | Generator | PROPOSED | Initial proposal |
| 1 | architect-lead | REVIEWED | Architecture OK |
| 1 | Evaluator | REVIEWED | Criteria testable |
| 2 | All | APPROVED | - |

---

## Sign-off

- [ ] Generator: Will coordinate execution
- [ ] architect-lead: Architecture is sound
- [ ] Evaluator: Criteria are testable
```

---

## Generated Harness Structure

用户运行 `/harness-creator ./my-game-project` 后生成：

```
my-game-project/
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── planner.md
│   │   ├── generator.md          # + Agent 工具
│   │   ├── evaluator.md
│   │   ├── architect-lead.md
│   │   ├── gameplay-dev.md       # 从模板生成
│   │   ├── graphics-dev.md
│   │   ├── audio-dev.md
│   │   └── ui-dev.md
│   ├── skills/
│   │   ├── start/
│   │   ├── checkpoint/
│   │   ├── resume/
│   │   ├── sprint-contract/
│   │   ├── level-design/         # 领域特定
│   │   └── asset-pipeline/       # 领域特定
│   ├── hooks/
│   │   ├── session-start.sh
│   │   ├── session-stop.sh
│   │   ├── pre-compact.sh
│   │   └── validate-*.sh
│   ├── rules/
│   │   ├── game-code.md          # 领域特定
│   │   └── asset-organization.md # 领域特定
│   ├── evaluation/
│   │   ├── gameplay-criteria.md  # 领域特定
│   │   └── performance-criteria.md
│   ├── templates/
│   │   ├── sprint-contract.md
│   │   ├── evaluation-report.md
│   │   └── handoff-artifact.md
│   └── docs/
│       ├── multi-agent-architecture.md
│       └── fusion-architecture.md
├── production/
│   ├── session-state/
│   └── session-logs/
└── CLAUDE.md
```

---

## User Confirmation Flow

```
检测到项目类型: Game Development (Unity)

推荐的配置:

核心 Agents:
  Planner        - 产品规划
  Generator      - 协调执行
  Evaluator      - 评估实现
  architect-lead - 架构决策

Specialists:
  [√] gameplay-dev    游戏逻辑、机制、AI
  [√] graphics-dev    渲染、shader、特效
  [√] audio-dev       音效、音乐系统
  [ ] physics-dev     物理模拟、碰撞检测
  [√] ui-dev          游戏UI、HUD、菜单

Skills:
  [√] level-design    关卡设计流程
  [√] asset-pipeline  资源管线
  [ ] performance-profile  性能分析

操作:
  A) 直接使用推荐
  B) 调整选择
  C) 添加自定义 specialist
  D) 查看详情

你的选择: _
```

---

## File Changes

### Keep Unchanged

| Path | Reason |
|------|--------|
| `references/base/core/agents/planner.md` | No role change |
| `references/base/core/agents/evaluator.md` | No role change |
| `references/base/progress/` | Entire system works |
| `references/base/safety/` | Entire system works |
| `references/base/evaluator/skills/` | Evaluation skills work |
| `references/brainstorm/` | Brainstorm flow works |

### Modify

| Path | Change |
|------|--------|
| `references/base/core/agents/generator.md` | Add Agent tool, delegation mechanism |
| `references/base/core/templates/sprint-contract.md` | Add architecture section, responsibility matrix |
| `references/base/core/skills/sprint-contract/SKILL.md` | Add architect-lead participation |
| `SKILL.md` | Update for fusion architecture, domain detection |

### Add New

| Path | Content |
|------|---------|
| `domain-templates/*/template.yaml` | Template configurations |
| `domain-templates/*/specialists/*.yaml` | Specialist definitions |
| `domain-templates/_dynamic/` | Dynamic generation templates |
| `references/base/core/templates/task-delegation.md` | Delegation template |

### Restructure

| Path | Action |
|------|--------|
| `references/domain-templates/web-development/agents/` | Move to `specialists/` as YAML |

---

## Implementation Priority

1. **High**: Modify generator.md (add Agent tool, delegation mode)
2. **High**: Enhance sprint-contract template
3. **High**: Create domain template structure (template.yaml format)
4. **High**: Convert existing web-development agents to YAML format
5. **Medium**: Implement domain detection logic
6. **Medium**: Implement dynamic specialist generation
7. **Medium**: Create game-development template
8. **Low**: Create additional domain templates (data-science, mobile-app)

---

## Summary

| Aspect | Design |
|--------|--------|
| **GAN Principle** | Generator-Evaluator separation preserved |
| **Specialists** | Domain-specific, delegated by Generator |
| **Template Mode** | Pre-defined templates for common domains |
| **Dynamic Mode** | Generate specialists for new domains |
| **Contract** | Architect-lead participates, responsibility matrix |
| **Evaluation** | Evaluator tests whole, localizes via contract |
| **Hooks/Rules** | Reuse existing, no changes needed |