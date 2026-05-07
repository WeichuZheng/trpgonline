# Safety Standards Documentation

This document defines the safety standards and security practices for the project.

---

## Overview

Safety standards ensure that common security mistakes are caught before they reach the repository. This includes:

- **Secret Detection**: Preventing credentials from being committed
- **Commit Validation**: Checking for security anti-patterns
- **Push Protection**: Enforcing branch and push policies

---

## Safety Hooks

### 1. validate-commit.sh

**Purpose**: Validates commits before they are created.

**Checks**:

| Check | Severity | Description |
|-------|----------|-------------|
| Hardcoded Secrets | BLOCK | Detects API keys, passwords, tokens, private keys |
| Docker :latest Tags | WARN | Warns against using `:latest` tag in Dockerfiles |
| Missing API Validation | WARN | Warns if API routes lack input validation |
| Hardcoded URLs | WARN | Warns about hardcoded URLs in source code |

**Usage**:

```bash
# Validate staged files
./validate-commit.sh --staged

# Validate specific files
./validate-commit.sh src/main.py src/config.py

# As a pre-commit hook
ln -s $(pwd)/validate-commit.sh .git/hooks/pre-commit
```

**Exit Codes**:

- `0`: All checks passed
- `1`: Block - commit rejected
- `2`: Warnings only - commit allowed

**Sample Output**:

```
=== Commit Validation ===
Checking 5 file(s)...

BLOCKED: Potential secret detected in src/config.py
  Pattern matched: api_key\s*[=:]\s*["'][a-zA-Z0-9_\-]{20,}
  Line: API_KEY = "sk-1234567890abcdefghijklmnop"

=== Validation Summary ===
BLOCKED: 1 error(s) found
Please fix the above issues before committing.
```

---

### 2. validate-push.sh

**Purpose**: Validates pushes before they are sent to remote.

**Checks**:

| Check | Severity | Description |
|-------|----------|-------------|
| Direct Push to Main | BLOCK | Prevents direct pushes to main/master |
| Force Push | BLOCK | Detects and blocks force push attempts |
| Protected Branches | WARN | Warns when pushing to protected branches |
| Large Commit Count | WARN | Warns when pushing many commits |
| Large Changeset | WARN | Suggests PR for large changes |

**Usage**:

```bash
# Validate current push
./validate-push.sh origin main

# As a pre-push hook
ln -s $(pwd)/validate-push.sh .git/hooks/pre-push
```

**Exit Codes**:

- `0`: All checks passed
- `1`: Block - push rejected
- `2`: Warnings only - push allowed

**Sample Output**:

```
=== Push Validation ===
Remote: origin
Branch: feature/add-auth

WARNING: Your branch has diverged from remote
  Local commits may not include remote changes.
  Consider using 'git pull --rebase' before pushing.
  If you must force push, use 'git push --force-with-lease'.

=== Push Validation Summary ===
WARNING: 1 warning(s) found
Push allowed, but please review the warnings above.
```

---

### 3. secret-detection.sh

**Purpose**: Comprehensive secret detection utility for scanning codebases.

**Features**:

- Detects 40+ secret patterns
- Supports entropy-based detection
- Baseline support for known secrets
- Recursive directory scanning
- Multiple output formats

**Supported Secret Types**:

| Category | Examples |
|----------|----------|
| API Keys | `api_key`, `apikey`, `API_KEY` |
| AWS | `AKIA...`, AWS secret access keys |
| Azure | Azure storage keys, connection strings |
| GCP | Google Cloud API keys |
| Passwords | `password`, `passwd`, `pwd` |
| Tokens | `auth_token`, `access_token`, `refresh_token` |
| OAuth | `client_secret`, `oauth_token` |
| JWT | JWT tokens, JWT secrets |
| SSH Keys | RSA, DSA, EC, OpenSSH private keys |
| Database URLs | MongoDB, PostgreSQL, MySQL, Redis URLs |
| Webhooks | Slack, Discord webhooks |
| Payment | Stripe keys (sk_live, pk_live) |
| GitHub | Personal access tokens (ghp_, gho_, ghu_) |
| Email | SendGrid API keys |
| SMS | Twilio account SIDs and tokens |

**Usage**:

```bash
# Basic scan of current directory
./secret-detection.sh

# Recursive deep scan
./secret-detection.sh --recursive --deep ./src

# Scan specific file
./secret-detection.sh --file .env

# Strict mode (exit 1 on any finding)
./secret-detection.sh --strict --recursive .

# With entropy detection
./secret-detection.sh --entropy ./src

# Using a baseline
./secret-detection.sh --baseline .secrets-baseline ./src

# Quiet mode (exit code only)
./secret-detection.sh --quiet ./src && echo "Clean" || echo "Secrets found"

# Output to file
./secret-detection.sh --output results.txt ./src
```

**Command Line Options**:

| Option | Description |
|--------|-------------|
| `-a, --all` | Scan all files including hidden |
| `-d, --deep` | Deep scan with context lines |
| `-r, --recursive` | Scan directories recursively |
| `-f, --file FILE` | Scan specific file |
| `-o, --output FILE` | Write results to file |
| `-q, --quiet` | Quiet mode (exit code only) |
| `-v, --verbose` | Verbose output |
| `--strict` | Exit 1 on any finding |
| `--entropy` | Enable entropy detection |
| `--baseline FILE` | Use baseline file for known secrets |

**Sample Output**:

```
Starting secret detection scan...
Scanning: src/config.py

[SECRET] api_key
  File:     src/config.py
  Line:     15
  Match:    API_KEY = "sk-1234567890abcdefghijklmnop"
  Context:
    14: # Database configuration
    15: API_KEY = "sk-1234567890abcdefghijklmnop"
    16: DB_URL = os.environ.get("DATABASE_URL")

==========================================
Secret Detection Summary
==========================================
Found 1 potential secret(s)

Recommendations:
  1. Review each finding above
  2. Remove secrets from code
  3. Use environment variables or secret managers
  4. Rotate any exposed credentials immediately
  5. Add secrets to .gitignore
```

---

## Integration Guide

### Git Hooks Setup

```bash
# Navigate to your repository
cd /path/to/your/repo

# Copy hooks to .git/hooks
cp references/base/safety/hooks/validate-commit.sh .git/hooks/pre-commit
cp references/base/safety/hooks/validate-push.sh .git/hooks/pre-push

# Make executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push

# Or create symbolic links
ln -s $(pwd)/references/base/safety/hooks/validate-commit.sh .git/hooks/pre-commit
ln -s $(pwd)/references/base/safety/hooks/validate-push.sh .git/hooks/pre-push
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run secret detection
        run: |
          chmod +x references/base/safety/hooks/secret-detection.sh
          ./references/base/safety/hooks/secret-detection.sh --strict --recursive .

      - name: Validate commits
        run: |
          ./references/base/safety/hooks/validate-commit.sh --staged
```

#### GitLab CI

```yaml
security-scan:
  stage: test
  script:
    - chmod +x references/base/safety/hooks/secret-detection.sh
    - ./references/base/safety/hooks/secret-detection.sh --strict --recursive .
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

#### Pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-commit
        name: Validate Commit
        entry: references/base/safety/hooks/validate-commit.sh
        language: script
        stages: [commit]

      - id: secret-detection
        name: Secret Detection
        entry: references/base/safety/hooks/secret-detection.sh
        language: script
        args: ['--strict']
        stages: [commit]
```

---

## Configuration

### Skipping Directories

The secret detection automatically skips:

```
.git, .svn, .hg
node_modules, venv, .venv
__pycache__, dist, build
target, vendor
.idea, .vscode
```

### Skipping File Types

Binary and generated files are automatically skipped:

```
.png, .jpg, .jpeg, .gif, .ico, .svg
.woff, .woff2, .ttf, .eot, .otf
.mp3, .mp4, .avi, .mov
.pdf, .zip, .tar, .gz, .rar, .7z
.exe, .dll, .so, .dylib
.pyc, .pyo, .class, .jar
.min.js, .min.css
```

### Custom Patterns

Add custom patterns to `secret-detection.sh`:

```bash
# Add to SECRET_PATTERNS array
SECRET_PATTERNS["custom_token"]="my_custom_token_[a-zA-Z0-9]{32}"
SECRET_PATTERNS["internal_key"]="internal_key_[a-zA-Z0-9]{16}"
```

### Baseline Management

Create a baseline for known secrets:

```bash
# Generate baseline (review output first!)
./secret-detection.sh --recursive . > .secrets-baseline

# Edit baseline to remove false positives
vim .secrets-baseline

# Use baseline for future scans
./secret-detection.sh --baseline .secrets-baseline .
```

---

## Best Practices

### 1. Environment Variables

```python
# Good: Load from environment
import os
api_key = os.environ.get("API_KEY")

# Better: Use python-dotenv
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ.get("API_KEY")

# Best: Use with defaults for development
api_key = os.environ.get("API_KEY", "dev-key-for-testing")
```

### 2. Configuration Files

```yaml
# config.yaml (committed to repo)
database:
  host: ${DB_HOST}
  port: ${DB_PORT}
  name: ${DB_NAME}

# .env (NOT committed)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
```

### 3. Secret Managers

```python
# Production: Use secret managers
from aws_secretsmanager import get_secret

def get_database_password():
    secret = get_secret("prod/database/password")
    return secret["password"]
```

### 4. CI/CD Secrets

```yaml
# Never hardcode in CI/CD
# BAD
env:
  API_KEY: "sk-1234567890"

# GOOD
env:
  API_KEY: ${{ secrets.API_KEY }}
```

---

## Troubleshooting

### Hook Not Running

```bash
# Check if hooks are executable
ls -la .git/hooks/

# Make executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

### False Positives

```bash
# Option 1: Add to baseline
./secret-detection.sh --recursive . >> .secrets-baseline

# Option 2: Add inline comment
API_KEY = "test_key_123"  # pragma: allowlist secret

# Option 3: Update patterns to exclude test values
# Edit secret-detection.sh and add to false positive patterns
```

### Pre-commit Bypass (Emergency Only)

```bash
# NOT RECOMMENDED - only for emergencies
git commit --no-verify
```

---

## Security Incident Response

If secrets are discovered in the repository:

1. **Immediate**: Rotate the exposed credential
2. **Investigate**: Check git history for exposure
3. **Clean**: Remove from history using BFG or git filter-branch
4. **Notify**: Inform security team and affected users
5. **Document**: Record the incident and remediation steps
6. **Prevent**: Add patterns to detection hooks

---

## References

- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheatsheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [GitLab Secret Detection](https://docs.gitlab.com/ee/user/application_security/secret_detection/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)