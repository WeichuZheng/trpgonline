# Rule Generator Prompt

> Use this prompt template to generate custom coding rules for the harness framework.

---

## Input Parameters

When generating a custom rule, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `rule_name` | Unique identifier for the rule (lowercase, hyphen-separated) | Yes |
| `rule_purpose` | What the rule enforces or validates | Yes |
| `path_scope` | File patterns this rule applies to (glob patterns) | Yes |
| `severity` | CRITICAL, HIGH, MEDIUM, or LOW | Yes |
| `enforcement` | How the rule is enforced (hook, lint, review, manual) | Yes |
| `code_patterns` | Examples of violations and correct patterns | Yes |
| `exceptions` | When the rule doesn't apply | No |
| `remediation` | How to fix violations | No |

---

## Prompt Template

```
You are generating a new coding rule for the harness framework.

## Rule to Generate

- **Name**: {rule_name}
- **Purpose**: {rule_purpose}
- **Path Scope**: {path_scope}
- **Severity**: {severity}
- **Enforcement**: {enforcement}
- **Code Patterns**: {code_patterns}
- **Exceptions**: {exceptions}
- **Remediation**: {remediation}

## Your Task

Create a complete rule definition following the harness framework conventions.

## Rule Definition Structure

Rules follow this markdown format:

1. **Header Section**:
   - Rule name (title)
   - Path scope (which files this applies to)
   - Severity level

2. **Rule Statement**: Clear, declarative statement of the rule

3. **Why This Matters**: Explanation of the importance

4. **Detection Patterns**: What violations look like

5. **Correct Patterns**: How to do it right

6. **Approved Methods**: Recommended approaches

7. **Exceptions**: When the rule doesn't apply

8. **Remediation**: How to fix violations

9. **Enforcement**: How this rule is enforced

## Design Principles

1. **Clear Statement**: The rule should be unambiguous
2. **Show Examples**: Both violations and correct code
3. **Explain Why**: Users need to understand the reason
4. **Provide Alternatives**: Show approved methods
5. **Define Exceptions**: Be clear about edge cases

Generate the rule definition now.
```

---

## Output Format

The generated file should follow this structure:

```markdown
# {Rule Name} Rule

**Path Scope:** `{path_glob_patterns}`

**Severity:** {CRITICAL | HIGH | MEDIUM | LOW}

---

## Rule: {Declarative Rule Statement}

{Clear, unambiguous statement of what the rule enforces.}

---

## Why This Matters

1. **{Reason 1}**: {Explanation}
2. **{Reason 2}**: {Explanation}
3. **{Reason 3}**: {Explanation}

---

## Detection Patterns

The following patterns are {blocked | flagged | reviewed}:

### {Category 1}

```{language}
// BLOCKED - {Description of violation}
{violation_code}

// CORRECT - {Description of correct approach}
{correct_code}
```

### {Category 2}

```{language}
// BLOCKED - {Description}
{violation_code}

// CORRECT - {Description}
{correct_code}
```

---

## Approved Methods

### 1. {Method Name}

```{language}
{approved_code_pattern}
```

### 2. {Method Name}

```{language}
{approved_code_pattern}
```

---

## Exceptions

The following are acceptable:

### 1. {Exception Name}
```{language}
// ACCEPTABLE - {Why this is okay}
{exception_code}
```

---

## Remediation Steps

If violations are found:

1. **{Step 1}**: {Action}
2. **{Step 2}**: {Action}
3. **{Step 3}**: {Action}

---

## Enforcement

This rule is enforced by:

1. **{Enforcement Method 1}**: {Description}
2. **{Enforcement Method 2}**: {Description}

Violations will:
- {Consequence 1}
- {Consequence 2}
```

---

## Quality Checklist

Before finalizing the rule definition, verify:

- [ ] **Rule Statement Clear**: Unambiguous declaration
- [ ] **Path Scope Defined**: Exact file patterns specified
- [ ] **Severity Appropriate**: Matches rule importance
- [ ] **Examples Provided**: Both violations and correct code
- [ ] **Why Explained**: Rationale is clear
- [ ] **Alternatives Shown**: Approved methods documented
- [ ] **Exceptions Listed**: Edge cases covered
- [ ] **Remediation Steps**: Clear fix instructions
- [ ] **Enforcement Defined**: How rule is enforced
- [ ] **Language Appropriate**: Code examples match project

---

## Severity Levels

| Level | Description | Enforcement |
|-------|-------------|-------------|
| CRITICAL | Security, data loss, safety issues | Block commit/push |
| HIGH | Major bugs, breaking changes | Block commit, warn |
| MEDIUM | Best practices, maintainability | Warn, require review |
| LOW | Style, minor improvements | Flag in code review |

---

## Examples

### Example 1: SQL Injection Prevention Rule

**Input:**
```
rule_name: sql-injection
rule_purpose: Prevent SQL injection vulnerabilities by requiring parameterized queries
path_scope: **/*.{py,js,ts,java,go,rb}
severity: CRITICAL
enforcement: pre-commit hook, code review
code_patterns:
  violation: String concatenation in SQL queries
  correct: Parameterized queries with placeholders
exceptions: Static queries with no user input
remediation: Replace string concatenation with parameterized queries
```

**Output:**
```markdown
# SQL Injection Prevention Rule

**Path Scope:** `**/*.{py,js,ts,java,go,rb}`

**Severity:** CRITICAL

---

## Rule: Use Parameterized Queries for All Database Operations

All database queries must use parameterized statements or prepared statements. String concatenation, interpolation, or formatting to build SQL queries is prohibited.

---

## Why This Matters

1. **Security**: SQL injection is a top vulnerability that can lead to data breaches
2. **Data Integrity**: Injection can corrupt or delete data
3. **Compliance**: Many regulations require protection against injection attacks
4. **Trust**: Users trust applications that protect their data

---

## Detection Patterns

The following patterns are blocked:

### String Concatenation

```python
# BLOCKED - String concatenation in SQL
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)

# CORRECT - Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### String Formatting

```python
# BLOCKED - f-string in SQL
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

# CORRECT - Parameterized query
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (name,))
```

### String Interpolation (JavaScript)

```javascript
// BLOCKED - Template literal in SQL
const query = `SELECT * FROM users WHERE email = '${email}'`;
connection.query(query);

// CORRECT - Parameterized query
const query = 'SELECT * FROM users WHERE email = ?';
connection.query(query, [email]);
```

---

## Approved Methods

### 1. Parameterized Queries (Python)

```python
# Using placeholders
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Named parameters
cursor.execute("SELECT * FROM users WHERE name = :name", {"name": name})
```

### 2. ORM Methods

```python
# SQLAlchemy
User.query.filter_by(id=user_id).first()

# Django ORM
User.objects.get(id=user_id)
```

### 3. Prepared Statements (Java)

```java
PreparedStatement stmt = connection.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setInt(1, userId);
ResultSet rs = stmt.executeQuery();
```

---

## Exceptions

The following are acceptable:

### 1. Static Queries

```python
# ACCEPTABLE - No user input
query = "SELECT * FROM config_settings"
cursor.execute(query)
```

### 2. Hardcoded Values

```python
# ACCEPTABLE - Hardcoded safe values
STATUS_CHOICES = ['active', 'inactive', 'pending']
query = "SELECT * FROM users WHERE status IN (?, ?, ?)"
cursor.execute(query, STATUS_CHOICES)
```

---

## Remediation Steps

If SQL injection vulnerabilities are found:

1. **Identify all user inputs**: Find where user data enters the query
2. **Replace with parameters**: Convert concatenation to parameterized queries
3. **Use ORM if available**: Prefer ORM methods over raw SQL
4. **Validate inputs**: Add input validation before queries
5. **Test thoroughly**: Verify both functionality and security

---

## Enforcement

This rule is enforced by:

1. **Pre-commit Hook**: `safety/hooks/sql-injection-check.sh`
2. **Code Review**: Required reviewer approval
3. **Static Analysis**: Automated SAST scanning

Violations will:
- Block the commit
- Create a security alert
- Require remediation before merge
```

---

### Example 2: No Console Logs in Production Rule

**Input:**
```
rule_name: no-console-logs
rule_purpose: Prevent console.log statements from being committed to production code
path_scope: src/**/*.{js,jsx,ts,tsx}
severity: MEDIUM
enforcement: pre-commit hook, lint rule
code_patterns:
  violation: console.log, console.debug, console.info
  correct: Proper logging library or debugger statements
exceptions: console.error, console.warn, test files
remediation: Remove or replace with proper logging
```

**Output:**
```markdown
# No Console Logs in Production Rule

**Path Scope:** `src/**/*.{js,jsx,ts,tsx}`

**Severity:** MEDIUM

---

## Rule: Remove Debug Console Statements Before Commit

Console.log and similar debug statements must not be committed to production code. Use proper logging libraries or debugger statements instead.

---

## Why This Matters

1. **Performance**: Console operations can slow down applications
2. **Security**: Console logs may expose sensitive data
3. **Code Clutter**: Debug statements reduce code readability
4. **Bundle Size**: Console calls add unnecessary bytes

---

## Detection Patterns

The following patterns are flagged:

### Console.log

```javascript
// BLOCKED - console.log
console.log('User data:', userData);
console.log('Component mounted');

// CORRECT - Use proper logging
import { logger } from '@/utils/logger';
logger.info('User data processed');
logger.debug('Component mounted', { component: 'UserList' });
```

### Console.debug/info

```javascript
// BLOCKED - console.debug/info
console.debug('Debug value:', value);
console.info('Processing started');

// CORRECT - Use logger or debugger
import { logger } from '@/utils/logger';
logger.debug('Value processed', { value });
// Or use debugger for development
debugger; // Gets removed by build tools
```

---

## Approved Methods

### 1. Logger Library

```javascript
import { logger } from '@/utils/logger';

// Structured logging
logger.info('User logged in', { userId: user.id });
logger.error('API request failed', { error: err.message });
logger.warn('Rate limit approaching', { remaining: 10 });
```

### 2. Debugger Statement

```javascript
// Use debugger during development
function complexCalculation(data) {
  debugger; // Automatically removed in production builds
  return processedData;
}
```

### 3. Environment-aware Logging

```javascript
// Only log in development
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info:', data);
}
```

---

## Exceptions

The following are acceptable:

### 1. Error and Warning Logs

```javascript
// ACCEPTABLE - Error logging
console.error('Critical error:', error);
console.warn('Deprecated API used');
```

### 2. Test Files

```javascript
// ACCEPTABLE - In test files
// __tests__/utils.test.js
console.log('Test debug output');  // Test file exception
```

### 3. Server-side Logging

```javascript
// ACCEPTABLE - Backend with proper log levels
if (config.isServer) {
  console.log('[Server] Request received:', req.path);
}
```

---

## Remediation Steps

If console statements are found:

1. **Identify all console statements**: Search for console.* patterns
2. **Determine if necessary**: Is this needed for debugging?
3. **Replace with logger**: Use proper logging library
4. **Remove if temporary**: Delete debug statements
5. **Use debugger**: For development, use debugger statement

---

## Enforcement

This rule is enforced by:

1. **ESLint Rule**: `no-console` in production config
2. **Pre-commit Hook**: `hooks/console-check.sh`
3. **Code Review**: Flagged in PR review

Violations will:
- Show lint warning
- Block commit if configured
- Require removal or replacement
```

---

## Anti-Patterns to Avoid

1. **Vague Rules**: "Don't write bad code" is not enforceable
2. **No Examples**: Rules need concrete examples
3. **Missing Why**: Users need to understand the reason
4. **No Exceptions**: Edge cases exist, document them
5. **Unclear Scope**: Be specific about which files

---

## Integration Notes

After generating a rule:

1. Save to `.claude/rules/{rule_name}.md`
2. Register in settings.json if automated enforcement
3. Add to code review checklist
4. Document in project's coding standards
5. Create enforcement hook if needed