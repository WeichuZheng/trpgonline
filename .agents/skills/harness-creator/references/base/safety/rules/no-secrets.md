# No Secrets Rule

**Path Scope:** `**/*.{py,js,ts,jsx,tsx,java,go,rb,php,cs,swift,kt,rs,scala,c,cpp,h,hpp,sh,yaml,yml,json,env,config,ini,tf}`

**Severity:** CRITICAL

---

## Rule: Never Commit Secrets to Version Control

Secrets must NEVER be committed to version control. This includes but is not limited to:

- API keys and tokens
- Passwords and passphrases
- Private keys and certificates
- Database credentials
- OAuth tokens and secrets
- Encryption keys
- Service account credentials

---

## Why This Matters

1. **Security Risk**: Exposed secrets can be exploited by attackers
2. **Credential Theft**: Secrets in git history are discoverable even after deletion
3. **Compliance**: Many regulations require protection of credentials
4. **Supply Chain Attacks**: Leaked secrets can compromise entire systems

---

## Detection Patterns

The following patterns are blocked by pre-commit hooks:

### API Keys
```python
# BLOCKED - API keys in code
api_key = "sk-1234567890abcdef"
API_KEY = "AKIAIOSFODNN7EXAMPLE"

# CORRECT - Use environment variables
import os
api_key = os.environ.get("API_KEY")
```

### Passwords
```python
# BLOCKED - Hardcoded passwords
password = "mySecretPassword123"
db_password = "admin123"

# CORRECT - Use secret management
from dotenv import load_dotenv
import os
password = os.environ.get("DB_PASSWORD")
```

### Tokens
```python
# BLOCKED - Tokens in code
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
slack_webhook = "https://hooks.slack.com/services/T00/B00/xxx"

# CORRECT - Use environment variables
auth_token = os.environ.get("AUTH_TOKEN")
slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
```

### Private Keys
```python
# BLOCKED - Private keys in code
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----"""

# CORRECT - Load from secure file or secret manager
private_key = os.environ.get("PRIVATE_KEY")
# Or use a secret manager
from aws_secretsmanager import get_secret
private_key = get_secret("my-app/private-key")
```

### Database URLs
```python
# BLOCKED - Credentials in connection strings
DATABASE_URL = "postgres://user:password@localhost:5432/db"
MONGO_URI = "mongodb://admin:secret123@localhost:27017/db"

# CORRECT - Use environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
# Or construct from components
import os
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")
DATABASE_URL = f"postgres://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
```

---

## Approved Methods for Secret Management

### 1. Environment Variables (Recommended for Development)

```bash
# .env file (add to .gitignore)
API_KEY=your-api-key-here
DB_PASSWORD=your-password-here
```

```python
# Load from .env
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

api_key = os.environ.get("API_KEY")
db_password = os.environ.get("DB_PASSWORD")
```

### 2. Secret Managers (Recommended for Production)

```python
# AWS Secrets Manager
import boto3
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='my-secret')
secret = response['SecretString']

# Azure Key Vault
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url, credential)
secret = client.get_secret("my-secret-name")

# HashiCorp Vault
import hvac
client = hvac.Client(url='http://localhost:8200')
secret = client.secrets.kv.v2.read_secret_version(path='my-secret')

# Google Secret Manager
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(name="projects/my-project/secrets/my-secret/versions/latest")
```

### 3. CI/CD Secrets

```yaml
# GitHub Actions
env:
  API_KEY: ${{ secrets.API_KEY }}

# GitLab CI
variables:
  API_KEY: $API_KEY  # Set in CI/CD settings

# CircleCI
environment:
  API_KEY: $API_KEY  # Set in project settings
```

---

## Exceptions and Allowances

The following are acceptable when properly configured:

### 1. Placeholder Values
```python
# ACCEPTABLE - Clear placeholder that requires configuration
API_KEY = "YOUR_API_KEY_HERE"  # Configure in production
DATABASE_URL = "postgresql://user:pass@host/db"  # Example only
```

### 2. Test Credentials
```python
# ACCEPTABLE - Clearly marked test credentials
TEST_API_KEY = "test_key_12345"  # Non-production test key
MOCK_PASSWORD = "test_password"  # Only for unit tests
```

### 3. Public Keys (Not Private Keys)
```python
# ACCEPTABLE - Public keys are meant to be shared
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"""
```

### 4. Configuration with Secrets References
```python
# ACCEPTABLE - References to secret locations
secrets:
  - name: database-credentials
    source: aws-secrets-manager
    path: prod/database
```

---

## Remediation Steps

If secrets are accidentally committed:

1. **Immediately rotate the exposed credential**
   - Generate new API keys
   - Change passwords
   - Revoke tokens

2. **Remove from git history**
   ```bash
   # Using BFG Repo-Cleaner
   bfg --replace-text passwords.txt my-repo.git

   # Using git filter-branch
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/secret/file' \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push (with team coordination)**
   ```bash
   git push origin --force --all
   git push origin --force --tags
   ```

4. **Update all environments** with new credentials

5. **Add secret patterns to .gitignore and pre-commit hooks**

---

## Enforcement

This rule is enforced by:

1. **Pre-commit Hook**: `safety/hooks/validate-commit.sh`
2. **Secret Detection**: `safety/hooks/secret-detection.sh`
3. **CI Pipeline Scans**: Automated scanning on every push

Violations will:
- Block the commit locally
- Fail CI builds
- Trigger security alerts