---
name: release
description: "Release workflow for version bumping, changelog generation, and deployment preparation. Coordinates release across all domains."
user-invocable: true
---

# Release Skill

You are facilitating the Release process. Your role is to coordinate version bumping, changelog generation, and deployment preparation.

## Purpose

Release workflow ensures:
- Version numbers are properly bumped
- Changelogs document all changes
- Tests pass before release
- Deployment is prepared correctly

## Release Flow

```
RELEASE REQUEST -> VERSION DECISION -> CHANGELOG -> PRE-RELEASE TESTS -> TAG -> DEPLOY PREP -> ANNOUNCE
```

## Workflow

### Phase 1: Release Request

1. Parse release request
2. Determine release type:
   - **Major**: Breaking changes (x.0.0)
   - **Minor**: New features (0.x.0)
   - **Patch**: Bug fixes (0.0.x)

### Phase 2: Version Decision

1. Analyze changes since last release
2. Recommend version bump
3. Get user approval for version number

### Semantic Versioning

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking API change | Major | 1.0.0 -> 2.0.0 |
| New feature | Minor | 1.0.0 -> 1.1.0 |
| Bug fix | Patch | 1.0.0 -> 1.0.1 |

### Phase 3: Changelog Generation

1. Gather commits since last tag
2. Categorize changes:
   - Features
   - Fixes
   - Breaking Changes
   - Dependencies
   - Documentation
3. Generate changelog

### Phase 4: Pre-Release Tests

Run full test suite:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Coverage meets targets
- [ ] No security vulnerabilities

### Phase 5: Tag and Commit

1. Update version in all config files
2. Commit version bump
3. Create git tag
4. Push tag to remote

### Phase 6: Deploy Prep

Prepare deployment:
- [ ] Docker images built
- [ ] Environment configs ready
- [ ] Migration scripts ready
- [ ] Rollback plan documented

### Phase 7: Announce

Create release announcement:
- Release notes
- Migration instructions (if breaking)
- Deployment timeline

## Release Report Template

```markdown
# Release: v[VERSION]

**Date**: [Date]
**Type**: Major | Minor | Patch
**Previous Version**: v[PREV]

---

## Summary

[2-3 sentence summary of this release]

---

## Changelog

### Breaking Changes
- [Breaking change 1]
- [Breaking change 2]

### Features
- [Feature 1]
- [Feature 2]

### Fixes
- [Fix 1]
- [Fix 2]

### Dependencies
- [Dependency update 1]

### Documentation
- [Doc update 1]

---

## Migration Guide

[If breaking changes, provide migration steps]

### Step 1: [Description]
```bash
[command]
```

### Step 2: [Description]
[instructions]

---

## Files Changed

| Domain | Files Changed |
|--------|---------------|
| Frontend | [count] |
| Backend | [count] |
| Database | [count] |
| DevOps | [count] |

---

## Test Results

| Category | Status |
|----------|--------|
| Unit Tests | PASS/FAIL |
| Integration Tests | PASS/FAIL |
| E2E Tests | PASS/FAIL |
| Coverage | [percentage]% |

---

## Deployment Checklist

- [ ] Docker images built
- [ ] Staging deployment verified
- [ ] Migrations tested
- [ ] Rollback plan ready
- [ ] Monitoring configured
- [ ] Team notified

---

## Rollback Plan

If issues occur:
1. [Rollback step 1]
2. [Rollback step 2]

---

## Timeline

- [ ] [Time]: Tag created
- [ ] [Time]: Staging deployed
- [ ] [Time]: Production deployed

---

## Sign-off

- [ ] architect-lead approved
- [ ] frontend-lead approved (frontend changes)
- [ ] backend-lead approved (backend changes)
- [ ] All tests pass
```

## Version Files to Update

| File | Format | Location |
|------|--------|----------|
| package.json | "version": "x.x.x" | Frontend |
| pyproject.toml | version = "x.x.x" | Backend |
| __init__.py | __version__ = "x.x.x" | Backend |
| docker-compose.yml | image: app:x.x.x | DevOps |

## Changelog Categories

### Breaking Changes
- API endpoint removed/changed
- Authentication flow changed
- Database schema incompatible
- Configuration format changed

### Features
- New endpoint
- New component/page
- New configuration option
- Performance improvement

### Fixes
- Bug resolved
- Error handling improved
- Security vulnerability patched
- Performance regression fixed

### Dependencies
- Package upgraded
- Package added
- Package removed

### Documentation
- API docs updated
- README updated
- Architecture docs updated

## Pre-Release Checklist

- [ ] All tests pass
- [ ] No regressions detected
- [ ] Coverage at target
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] Changelog complete
- [ ] Version bumped in all files
- [ ] Tag created

## Post-Release Checklist

- [ ] Tag pushed to remote
- [ ] Staging deployed
- [ ] Smoke tests pass
- [ ] Production deployed
- [ ] Monitoring verified
- [ ] Announcement sent

## Anti-Patterns to Avoid

- Releasing without passing tests
- Missing changelog entries
- Breaking changes without migration guide
- Version bump in wrong files
- Releasing on Friday

## Usage

```
/release [type]
```

Example:
```
/release minor
/release patch
```

## Coordination

- architect-lead approves all releases
- Domain leads approve domain changes
- All tests must pass before release
- Breaking changes require migration documentation