---
name: deploy-check
description: "Pre-deployment validation checklist for Docker, CI/CD, and environment configuration. Ensures deployment readiness before production."
user-invocable: true
---

# Deploy Check Skill

You are facilitating the Deploy Check process. Your role is to validate deployment readiness before pushing to production.

## Purpose

Deploy check ensures:
- Docker configurations are correct
- Environment variables are set
- Health checks are configured
- Rollback plan is ready
- Monitoring is in place

## Deploy Check Flow

```
DEPLOY REQUEST -> ENVIRONMENT CHECK -> DOCKER CHECK -> SECURITY CHECK -> HEALTH CHECK -> REPORT -> APPROVAL
```

## Workflow

### Phase 1: Environment Check

Validate environment:
- [ ] All required env vars documented
- [ ] Secrets are in secret manager (not code)
- [ ] Environment configs exist for target
- [ ] Database URLs are correct

### Phase 2: Docker Check

Validate Docker:
- [ ] All images use specific versions (no :latest)
- [ ] Dockerfiles optimized
- [ ] Health checks configured
- [ ] Resource limits set
- [ ] Networks properly configured

### Phase 3: Security Check

Validate security:
- [ ] No secrets in Dockerfiles
- [ ] CORS configured correctly
- [ ] Authentication required on sensitive endpoints
- [ ] SSL/TLS configured
- [ ] Security headers present

### Phase 4: Health Check

Validate health:
- [ ] All services have health endpoints
- [ ] Health check intervals configured
- [ ] Startup periods set
- [ ] Retry counts appropriate

### Phase 5: Rollback Check

Validate rollback:
- [ ] Previous version tagged
- [ ] Rollback procedure documented
- [ ] Database rollback migration ready
- [ ] Rollback tested

### Phase 6: Monitoring Check

Validate monitoring:
- [ ] Logs configured
- [ ] Alerts configured
- [ ] Metrics endpoints available
- [ ] Dashboard updated

### Phase 7: Generate Report

Create deploy readiness report with:
- Checklist status
- Issues found
- Action items
- Approval recommendation

## Deploy Check Report Template

```markdown
# Deploy Check: [Target Environment]

**Date**: [Date]
**Target**: [staging/production]
**Version**: [version to deploy]

---

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Environment | READY/NOT_READY | [count] |
| Docker | READY/NOT_READY | [count] |
| Security | READY/NOT_READY | [count] |
| Health Checks | READY/NOT_READY | [count] |
| Rollback | READY/NOT_READY | [count] |
| Monitoring | READY/NOT_READY | [count] |

**Overall**: READY / NOT_READY

---

## Environment Checklist

- [x] Required env vars documented
- [x] Secrets in secret manager
- [ ] MISSING: [env var name]
- [x] Database URLs correct
- [x] Redis URLs correct

---

## Docker Checklist

- [x] Frontend image: [specific version]
- [x] Backend image: [specific version]
- [x] Database image: postgres:15-alpine
- [x] Redis image: redis:7-alpine
- [x] Health checks configured
- [x] Resource limits set

### Docker Issues
- [Issue description]

---

## Security Checklist

- [x] No secrets in Dockerfiles
- [x] CORS configured
- [x] Auth on sensitive endpoints
- [x] SSL/TLS configured
- [x] Security headers present

### Security Issues
- [Issue description]

---

## Health Check Configuration

| Service | Endpoint | Interval | Timeout | Retries |
|---------|----------|----------|---------|---------|
| Frontend | /health | 30s | 10s | 3 |
| Backend | /health | 30s | 10s | 3 |
| Database | pg_isready | 10s | 5s | 5 |

---

## Rollback Plan

1. **Tag previous version**: v[previous]
2. **Rollback deployment**:
   ```bash
   docker-compose down
   git checkout v[previous]
   docker-compose up -d
   ```
3. **Database rollback**:
   ```bash
   alembic downgrade -1
   ```

---

## Monitoring Configuration

- [x] Logs: [logging system]
- [x] Alerts: [alert system]
- [x] Metrics: [metrics system]
- [ ] MISSING: [monitoring item]

---

## Action Items

| Priority | Action | Assignee |
|----------|--------|----------|
| P1 | [Action] | [Agent] |
| P2 | [Action] | [Agent] |

---

## Approval

- [ ] devops-dev verified
- [ ] backend-lead approved (backend changes)
- [ ] architect-lead approved

---

## Deployment Timeline

- [ ] [Time]: Deploy check complete
- [ ] [Time]: Approval received
- [ ] [Time]: Deployment started
- [ ] [Time]: Deployment verified
```

## Required Environment Variables

| Variable | Purpose | Location |
|----------|---------|----------|
| DATABASE_URL | PostgreSQL connection | Secret manager |
| REDIS_URL | Redis connection | Secret manager |
| API_URL | Backend API URL | Config |
| SECRET_KEY | Auth secret | Secret manager |
| CORS_ORIGINS | Allowed origins | Config |

## Docker Best Practices

### Image Versioning
```yaml
# GOOD - Specific version
image: postgres:15-alpine

# BAD - Latest tag
image: postgres:latest  # NEVER USE
```

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

## Security Checks

### CORS Configuration
```yaml
# Backend CORS
CORS_ORIGINS: ["https://app.example.com"]
```

### Security Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

### SSL/TLS
- Certificates configured
- HTTPS enforced
- Certificate renewal automated

## Rollback Requirements

1. **Previous version tagged and accessible**
2. **Database migration reversible**
3. **Rollback procedure documented**
4. **Rollback tested in staging**

## Monitoring Requirements

1. **Logs centralized and searchable**
2. **Alerts for critical errors**
3. **Metrics for performance**
4. **Dashboard for overview**

## Anti-Patterns to Avoid

- Deploying with :latest tags
- Missing health checks
- No rollback plan
- Missing monitoring
- Deploying without approval
- Deploying on Friday afternoon

## Usage

```
/deploy-check [environment]
```

Example:
```
/deploy-check staging
/deploy-check production
```

## Coordination

- devops-dev performs deploy check
- architect-lead approves production deployments
- Domain leads verify domain-specific readiness
- All checks must pass before approval