# Skill Generator Prompt

> Use this prompt template to generate custom skill definitions for the harness framework.

---

## Input Parameters

When generating a custom skill, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `skill_name` | Unique identifier for the skill (lowercase, hyphen-separated) | Yes |
| `skill_description` | One-line description of what the skill does | Yes |
| `trigger_context` | When this skill should be invoked | Yes |
| `workflow_steps` | The steps the skill should execute | Yes |
| `user_invocable` | Can user manually invoke with /skill-name | No (default: false) |
| `allowed_tools` | Tools this skill can use | No |
| `argument_hint` | Hint for skill arguments | No |
| `output_format` | What the skill produces | No |

---

## Prompt Template

```
You are generating a new Claude Code skill definition for the harness framework.

## Skill to Generate

- **Name**: {skill_name}
- **Description**: {skill_description}
- **Trigger Context**: {trigger_context}
- **User Invocable**: {user_invocable}
- **Allowed Tools**: {allowed_tools}
- **Argument Hint**: {argument_hint}

## Workflow Steps

{workflow_steps}

## Expected Output

{output_format}

## Your Task

Create a complete skill definition file following the harness framework conventions.

## Skill Definition Structure

Skills follow this markdown format:

1. **Frontmatter** (YAML between ---):
   - name: Skill identifier (matches directory name)
   - description: One-line purpose (quoted)
   - user-invocable: true/false
   - argument-hint: Optional argument guidance
   - allowed-tools: Optional tool restrictions

2. **Content Sections**:
   - Purpose statement
   - Workflow steps (numbered)
   - Usage examples
   - Integration notes

## Design Principles

1. **Single Purpose**: Each skill does ONE thing well
2. **Clear Trigger**: Define exactly when skill activates
3. **Guidance First**: Skills guide, not auto-execute
4. **User Control**: User maintains control throughout
5. **Composable**: Skills can call other skills

Generate the skill definition now.
```

---

## Output Format

The generated file should be saved as `SKILL.md` in a directory named after the skill:

```
.claude/skills/{skill_name}/SKILL.md
```

```markdown
---
name: {skill_name}
description: "{one-line description}"
user-invocable: {true|false}
argument-hint: "[optional-args]"
allowed-tools: {tool1}, {tool2}
---

# {Skill Name} Skill

{Brief purpose statement explaining what this skill does and when to use it.}

## Purpose

{Detailed explanation of the skill's purpose and value.}

## When to Use

{Specific conditions that should trigger this skill.}

## Workflow

### Step 1: {First Step}

{Detailed instructions for step 1}

### Step 2: {Second Step}

{Detailed instructions for step 2}

### Step 3: {Third Step}

{Detailed instructions for step 3}

## Usage

```
/{skill_name} [arguments]
```

{Examples of how to invoke and what to expect}

## Examples

### Example 1: {Scenario}

{Example walkthrough}

### Example 2: {Scenario}

{Example walkthrough}

## Integration Notes

{How this skill integrates with other skills or agents}

## Quality Checklist

Before considering this skill complete:
- [ ] {Checklist item 1}
- [ ] {Checklist item 2}
```

---

## Quality Checklist

Before finalizing the skill definition, verify:

- [ ] **Frontmatter Correct**: All required fields present and valid
- [ ] **Name Conventions**: Lowercase, hyphen-separated, matches directory
- [ ] **Description Clear**: One-line description explains value
- [ ] **Trigger Defined**: Clear conditions for when to use
- [ ] **Steps Actionable**: Each step has concrete actions
- [ ] **Tools Appropriate**: Only necessary tools included
- [ ] **Examples Provided**: Real-world usage examples
- [ ] **Integration Clear**: How skill fits with others
- [ ] **User Control**: User maintains agency throughout

---

## Skill Types Reference

### Workflow Skills
Guide through multi-step processes (e.g., `/deploy-check`, `/code-review`)

### Automation Skills
Execute predefined actions (e.g., `/loop`, `/checkpoint`)

### Analysis Skills
Analyze code or state (e.g., `/tech-debt`, `/regression-test`)

### Generation Skills
Create new artifacts (e.g., `/api-design`, `/feature-plan`)

---

## Examples

### Example 1: API Documentation Skill

**Input:**
```
skill_name: api-docs
skill_description: Generate OpenAPI documentation from existing API endpoints
trigger_context: When API endpoints exist but lack documentation, or user mentions "document API"
user_invocable: true
allowed_tools: Read, Glob, Grep, Write
workflow_steps:
  1. Scan codebase for API route definitions
  2. Extract request/response schemas
  3. Generate OpenAPI 3.0 specification
  4. Create documentation files
output_format: OpenAPI YAML file + markdown documentation
```

**Output:**
```markdown
---
name: api-docs
description: "Generate OpenAPI documentation from existing API endpoints"
user-invocable: true
argument-hint: "[api-path]"
allowed-tools: Read, Glob, Grep, Write
---

# API Documentation Skill

Generate comprehensive OpenAPI 3.0 documentation from your existing API code.

## Purpose

This skill analyzes your API route definitions and generates standardized OpenAPI documentation, making your APIs discoverable and testable.

## When to Use

- API endpoints exist but lack documentation
- User mentions "document API" or "OpenAPI spec"
- Before sharing APIs with external teams
- When setting up API testing tools

## Workflow

### Step 1: Scan for API Routes

Use Glob to find route files:
- Look for patterns like `**/routes/**`, `**/api/**`
- Identify Express, FastAPI, or framework-specific routes
- Catalog all endpoints found

### Step 2: Extract Schemas

For each endpoint:
- Identify request body schema
- Identify response schema
- Extract path/query parameters
- Note authentication requirements

### Step 3: Generate OpenAPI Spec

Create `openapi.yaml`:
- Populate info section
- Add server configurations
- Define paths with methods
- Include schemas in components
- Add security schemes if applicable

### Step 4: Create Documentation

Generate markdown documentation:
- Overview page
- Authentication guide
- Endpoint reference
- Examples and samples

## Usage

```
/api-docs [api-path]
```

- Without argument: Scan entire project
- With path: Focus on specific directory

## Examples

### Example 1: Document All APIs

```
/api-docs
```

Scans the entire project and generates complete API documentation.

### Example 2: Document Specific Module

```
/api-docs src/api/users
```

Documents only the user API module.

## Integration Notes

- Works with Express, FastAPI, Flask, NestJS
- Outputs to `docs/api/` directory
- Can be run after API changes to update docs
```

---

### Example 2: Performance Audit Skill

**Input:**
```
skill_name: perf-audit
skill_description: Analyze codebase for performance bottlenecks and optimization opportunities
trigger_context: When user mentions "performance", "slow", "optimize", or "bottleneck"
user_invocable: true
allowed_tools: Read, Glob, Grep, Bash
workflow_steps:
  1. Analyze bundle sizes and dependencies
  2. Check for common performance anti-patterns
  3. Review database query patterns
  4. Identify lazy loading opportunities
  5. Generate optimization report
output_format: Performance audit report with prioritized recommendations
```

**Output:**
```markdown
---
name: perf-audit
description: "Analyze codebase for performance bottlenecks and optimization opportunities"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
---

# Performance Audit Skill

Comprehensive performance analysis to identify bottlenecks and optimization opportunities.

## Purpose

This skill performs a systematic analysis of your codebase to find performance issues, from bundle size to database queries, and provides actionable recommendations.

## When to Use

- User mentions "performance", "slow", "optimize", "bottleneck"
- Before production deployment
- When investigating performance degradation
- As part of code review process

## Workflow

### Step 1: Bundle Analysis

- Analyze package.json dependencies
- Check for duplicate dependencies
- Identify tree-shaking opportunities
- Calculate estimated bundle sizes

### Step 2: Anti-Pattern Detection

Search for:
- N+1 query patterns
- Missing pagination
- Synchronous heavy operations
- Unoptimized images
- Missing caching

### Step 3: Database Query Review

- Find all database queries
- Check for missing indexes
- Identify slow query patterns
- Look for N+1 ORM issues

### Step 4: Lazy Loading Check

- Identify large components
- Check for code splitting
- Find lazy loading opportunities
- Review dynamic imports

### Step 5: Generate Report

Create prioritized report:
- Critical issues (fix immediately)
- Important optimizations (fix soon)
- Nice-to-have improvements
- Estimated impact for each

## Usage

```
/perf-audit [focus-area]
```

- Without argument: Full audit
- With focus: `frontend`, `backend`, `database`, or `network`

## Examples

### Example 1: Full Audit

```
/perf-audit
```

Runs complete performance analysis across all areas.

### Example 2: Frontend Focus

```
/perf-audit frontend
```

Focuses on bundle size, rendering, and lazy loading.

## Integration Notes

- Complements `/code-review` skill
- Use before `/deploy-check`
- Results feed into `/tech-debt` tracking
```

---

## Anti-Patterns to Avoid

1. **Vague Purpose**: "Helps with development" is not specific
2. **Too Broad**: A skill should do ONE thing well
3. **No Trigger**: User should know when to use it
4. **Missing Examples**: Users need examples to understand usage
5. **Auto-execution**: Skills should guide, not auto-execute

---

## Integration Notes

After generating a skill:

1. Create directory: `.claude/skills/{skill_name}/`
2. Save as `SKILL.md` in that directory
3. Test the skill invocation
4. Document in project's skill registry
5. Add to agent references if applicable