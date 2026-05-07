# Settings Generator Prompt

> Use this prompt template to generate custom settings.json configurations for the harness framework.

---

## Input Parameters

When generating custom settings, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `project_name` | Name of the project | Yes |
| `project_type` | Type of project (web, api, mobile, library, etc.) | Yes |
| `tech_stack` | Technologies used | Yes |
| `features_needed` | Which harness features to enable | Yes |
| `agent_config` | Custom agent configurations | No |
| `hook_config` | Which hooks to enable | No |
| `rule_config` | Which rules to enforce | No |

---

## Prompt Template

```
You are generating a custom settings.json for a Claude Code harness framework.

## Project Configuration

- **Project Name**: {project_name}
- **Project Type**: {project_type}
- **Tech Stack**: {tech_stack}
- **Features Needed**: {features_needed}
- **Agent Config**: {agent_config}
- **Hook Config**: {hook_config}
- **Rule Config**: {rule_config}

## Your Task

Create a complete settings.json following the harness framework conventions.

## Settings Structure

settings.json contains:

1. **permissions**: Tool access permissions
2. **hooks**: Event-triggered scripts
3. **env**: Environment variables
4. **agents**: Custom agent configurations
5. **project**: Project metadata

## Design Principles

1. **Least Privilege**: Only enable needed permissions
2. **Sensible Defaults**: Start with safe defaults
3. **Project-Specific**: Tailor to tech stack
4. **Extensible**: Easy to add features later
5. **Documented**: Comments explain choices

Generate the settings.json now.
```

---

## Output Format

The generated settings should follow this structure:

```json
{
  "permissions": {
    "allow": [
      // Allowed tools and patterns
    ],
    "deny": [
      // Denied tools and patterns
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "{tool_pattern}",
        "hooks": ["{hook_script}"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "{tool_pattern}",
        "hooks": ["{hook_script}"]
      }
    ],
    "Notification": [
      {
        "matcher": "{event_pattern}",
        "hooks": ["{hook_script}"]
      }
    ]
  },
  "env": {
    // Environment variables
  },
  "agents": {
    // Custom agent configurations
  },
  "project": {
    "name": "{project_name}",
    "type": "{project_type}",
    "version": "1.0.0"
  }
}
```

---

## Quality Checklist

Before finalizing settings.json, verify:

- [ ] **Valid JSON**: Parses without errors
- [ ] **Permissions Minimal**: Only needed permissions
- [ ] **Hooks Configured**: Required hooks enabled
- [ ] **Agents Defined**: Custom agents included
- [ ] **Project Metadata**: Name and type present
- [ ] **Paths Correct**: All file paths exist
- [ ] **Comments Added**: Complex settings explained
- [ ] **Sensible Defaults**: Safe starting configuration

---

## Permission Types Reference

### Tool Permissions

| Permission | Description | Risk Level |
|------------|-------------|------------|
| `Read(*)` | Read any file | Low |
| `Write(*)` | Write any file | High |
| `Edit(*)` | Edit any file | Medium |
| `Bash(*)` | Execute any command | High |
| `Bash(npm)` | Run npm commands | Medium |
| `Bash(git)` | Run git commands | Medium |

### Pattern Matching

```
*           // Any file
*.js        // JavaScript files
src/**/*    // Files in src directory
!secret*    // Exclude files starting with secret
```

---

## Hook Types Reference

| Hook Type | When It Runs | Common Uses |
|-----------|-------------|-------------|
| PreToolUse | Before tool execution | Validation, logging |
| PostToolUse | After tool execution | Cleanup, notification |
| Notification | On events | Alerts, status updates |
| PreCommit | Before git commit | Linting, validation |
| PostCommit | After git commit | Notifications |
| SessionStart | Session begins | Context loading |
| SessionStop | Session ends | Cleanup, backup |

---

## Examples

### Example 1: Web Application Settings

**Input:**
```
project_name: my-web-app
project_type: web
tech_stack: React, Node.js, PostgreSQL
features_needed: agents, hooks, rules
agent_config: planner, generator, evaluator
hook_config: session-start, session-stop, pre-commit
rule_config: no-secrets, lint-check
```

**Output:**
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Write(tests/**/*)",
      "Write(docs/**/*)",
      "Edit(src/**/*)",
      "Edit(tests/**/*)",
      "Bash(npm)",
      "Bash(npx)",
      "Bash(git)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Write(.env*)",
      "Write(*.secret)",
      "Write(credentials/*)",
      "Bash(rm -rf*)",
      "Bash(sudo*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [".claude/hooks/validate-write.sh"]
      },
      {
        "matcher": "Bash",
        "hooks": [".claude/hooks/validate-command.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [".claude/hooks/format-code.sh"]
      }
    ],
    "Notification": [
      {
        "matcher": "*",
        "hooks": [".claude/hooks/log-activity.sh"]
      }
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "DATABASE_URL": "${DATABASE_URL}",
    "API_URL": "http://localhost:3000"
  },
  "agents": {
    "planner": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "WebSearch"]
    },
    "generator": {
      "model": "sonnet",
      "tools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(npm)", "Bash(npx)"]
    },
    "evaluator": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "Bash(npm test)"]
    }
  },
  "project": {
    "name": "my-web-app",
    "type": "web",
    "version": "1.0.0",
    "tech_stack": ["React", "Node.js", "PostgreSQL"],
    "structure": {
      "frontend": "src/frontend",
      "backend": "src/backend",
      "shared": "src/shared",
      "tests": "tests",
      "docs": "docs"
    }
  },
  "rules": [
    ".claude/rules/no-secrets.md",
    ".claude/rules/lint-check.md"
  ],
  "session": {
    "state_file": ".claude/session-state.md",
    "checkpoint_dir": ".claude/checkpoints",
    "log_dir": "production/session-logs"
  }
}
```

---

### Example 2: API Service Settings

**Input:**
```
project_name: payment-api
project_type: api
tech_stack: Python, FastAPI, PostgreSQL, Redis
features_needed: agents, hooks, rules, multi-project
agent_config: planner, generator, evaluator, coordinator
hook_config: session-start, pre-commit, secret-detection
rule_config: no-secrets, api-versioning, error-handling
```

**Output:**
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Write(tests/**/*)",
      "Write(api/**/*)",
      "Edit(src/**/*)",
      "Edit(tests/**/*)",
      "Bash(python)",
      "Bash(pip)",
      "Bash(pytest)",
      "Bash(git)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Write(.env*)",
      "Write(*.pem)",
      "Write(*.key)",
      "Write(credentials/*)",
      "Bash(rm -rf*)",
      "Bash(sudo*)",
      "Bash(eval*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [".claude/hooks/validate-write.sh"]
      },
      {
        "matcher": "Write",
        "hooks": [".claude/hooks/secret-detection.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [".claude/hooks/format-code.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/session-start.sh"
    ],
    "SessionStop": [
      ".claude/hooks/session-stop.sh"
    ],
    "PreCommit": [
      ".claude/hooks/validate-commit.sh"
    ]
  },
  "env": {
    "PYTHON_ENV": "development",
    "DATABASE_URL": "${DATABASE_URL}",
    "REDIS_URL": "${REDIS_URL}",
    "API_VERSION": "v1"
  },
  "agents": {
    "planner": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "WebSearch"]
    },
    "generator": {
      "model": "sonnet",
      "tools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python)", "Bash(pip)"]
    },
    "evaluator": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "Bash(pytest)"]
    },
    "coordinator": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep"],
      "description": "Coordinates work across multiple services"
    }
  },
  "project": {
    "name": "payment-api",
    "type": "api",
    "version": "1.0.0",
    "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Redis"],
    "structure": {
      "api": "src/api",
      "models": "src/models",
      "services": "src/services",
      "tests": "tests",
      "docs": "docs"
    },
    "api_versioning": {
      "current": "v1",
      "deprecated": [],
      "sunset_policy_days": 90
    }
  },
  "rules": [
    ".claude/rules/no-secrets.md",
    ".claude/rules/api-versioning.md",
    ".claude/rules/error-handling.md"
  ],
  "session": {
    "state_file": ".claude/session-state.md",
    "checkpoint_dir": ".claude/checkpoints",
    "log_dir": "production/session-logs",
    "context_reset_threshold": 150000
  },
  "multi_project": {
    "enabled": true,
    "services": [
      {
        "name": "payment-api",
        "path": ".",
        "type": "api"
      },
      {
        "name": "notification-service",
        "path": "../notification-service",
        "type": "service"
      }
    ],
    "shared_libraries": ["../shared-libs"]
  }
}
```

---

### Example 3: Mobile App Settings

**Input:**
```
project_name: mobile-app
project_type: mobile
tech_stack: React Native, TypeScript
features_needed: agents, hooks, rules
agent_config: planner, generator, evaluator
hook_config: session-start, pre-commit
rule_config: no-secrets, no-console-logs
```

**Output:**
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Write(app/**/*)",
      "Write(tests/**/*)",
      "Edit(src/**/*)",
      "Edit(app/**/*)",
      "Edit(tests/**/*)",
      "Bash(npm)",
      "Bash(npx)",
      "Bash(yarn)",
      "Bash(git)",
      "Bash(react-native)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Write(.env*)",
      "Write(*.keystore)",
      "Write(*.jks)",
      "Write(android/app/google-services.json)",
      "Write(ios/GoogleService-Info.plist)",
      "Bash(rm -rf*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [".claude/hooks/validate-write.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [".claude/hooks/format-code.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/session-start.sh"
    ],
    "PreCommit": [
      ".claude/hooks/validate-commit.sh",
      ".claude/hooks/lint-check.sh"
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "REACT_NATIVE_ENV": "development"
  },
  "agents": {
    "planner": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "WebSearch"]
    },
    "generator": {
      "model": "sonnet",
      "tools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(npm)", "Bash(npx)", "Bash(react-native)"]
    },
    "evaluator": {
      "model": "sonnet",
      "tools": ["Read", "Glob", "Grep", "Bash(npm test)", "Bash(npx detox)"]
    }
  },
  "project": {
    "name": "mobile-app",
    "type": "mobile",
    "version": "1.0.0",
    "tech_stack": ["React Native", "TypeScript"],
    "platforms": ["ios", "android"],
    "structure": {
      "src": "src",
      "components": "src/components",
      "screens": "src/screens",
      "navigation": "src/navigation",
      "services": "src/services",
      "tests": "tests"
    }
  },
  "rules": [
    ".claude/rules/no-secrets.md",
    ".claude/rules/no-console-logs.md"
  ],
  "session": {
    "state_file": ".claude/session-state.md",
    "checkpoint_dir": ".claude/checkpoints",
    "log_dir": "production/session-logs"
  },
  "mobile": {
    "ios": {
      "bundle_id": "com.company.app",
      "deployment_target": "13.0"
    },
    "android": {
      "package_name": "com.company.app",
      "min_sdk_version": 23
    }
  }
}
```

---

## Anti-Patterns to Avoid

1. **Overly Permissive**: `Bash(*)` without restrictions
2. **Missing Deny Rules**: Not blocking dangerous operations
3. **No Hooks**: Missing validation hooks
4. **Hardcoded Secrets**: Credentials in settings
5. **Missing Paths**: Referenced files don't exist

---

## Integration Notes

After generating settings.json:

1. Save to `.claude/settings.json`
2. Create referenced hook files
3. Create referenced rule files
4. Test with sample operations
5. Review and adjust permissions
6. Document any project-specific settings