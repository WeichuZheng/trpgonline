# Directory Structure

> Web development domain project directory organization.

---

## Project Structure

```
/
├── CLAUDE.md                    # Project configuration (references this template)
├── .claude/                     # Claude Code configuration
│   ├── settings.json            # Permissions and hooks
│   ├── agents/                  # Agent definitions (from template)
│   ├── skills/                  # Skill definitions (from template)
│   ├── rules/                   # Coding standards (from template)
│   ├── hooks/                   # Validation hooks (from template)
│   └── docs/                    # Documentation (from template)
│
├── src/                         # Application source code
│   ├── frontend/                # Frontend code
│   │   ├── components/          # UI components
│   │   │   ├── common/          # Generic components
│   │   │   ├── layout/          # Layout components
│   │   │   └── features/        # Feature-specific
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API clients
│   │   ├── utils/               # Utilities
│   │   ├── styles/              # Global styles, tokens
│   │   └── App.tsx              # Main app component
│   │   └── main.tsx             # Entry point
│   │
│   └── backend/                 # Backend code
│   │   ├── api/                 # API layer
│   │   │   ├── routes/          # Route definitions
│   │   │   ├── dependencies.py  # Shared deps (auth)
│   │   │   └── __init__.py      # Router aggregation
│   │   ├── services/            # Business logic
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repository/          # Data access
│   │   ├── utils/               # Utilities
│   │   ├── exceptions.py        # Custom exceptions
│   │   ├── database.py          # DB configuration
│   │   └── main.py              # FastAPI app
│   │
│   └── shared/                  # Shared utilities (optional)
│
├── migrations/                  # Database migrations
│   ├── versions/                # Migration files
│   ├── alembic.ini              # Alembic config
│   └── env.py                   # Migration environment
│
├── tests/                       # Test suites
│   ├── frontend/                # Frontend tests
│   │   ├── components/          # Component tests
│   │   ├── hooks/               # Hook tests
│   │   ├── integration/         # Integration tests
│   │   └── e2e/                 # End-to-end tests
│   │
│   ├── backend/                 # Backend tests
│   │   ├── unit/                # Unit tests
│   │   ├── integration/         # Integration tests
│   │   ├── services/            # Service tests
│   │   └── api/                 # API tests
│   │
│   ├── fixtures/                # Test data
│   ├── helpers/                 # Test helpers
│   └── conftest.py              # Pytest config
│
├── docs/                        # Documentation
│   ├── api/                     # API specifications
│   │   └── users-api.md         # Example API spec
│   │
│   ├── architecture/            # Architecture docs
│   │   ├── adr/                 # ADRs
│   │   │   ├── ADR-001-postgres.md
│   │   │   └── ADR-002-redis.md
│   │   ├── system-design.md     # System overview
│   │   └── data-model.md        # Data model
│   │
│   ├── deployment/              # Deployment guides
│   └── development/             # Dev guides
│
├── docker/                      # Docker configuration
│   ├── frontend/                # Frontend Dockerfile
│   ├── backend/                 # Backend Dockerfile
│   ├── nginx/                   # Nginx config
│   └── docker-compose.yml       # Development compose
│   └── docker-compose.prod.yml  # Production compose
│
├── scripts/                     # Utility scripts
│   ├── deploy.sh                # Deployment script
│   ├── backup.sh                # Backup script
│   ├── migrate.sh               # Migration script
│   └── seed-data.sh             # Data seeding
│
├── .github/                     # GitHub configuration
│   └── workflows/               # CI/CD workflows
│       ├── ci.yml               # CI pipeline
│       ├── deploy.yml           # Deployment
│       └── release.yml          # Release workflow
│
├── production/                  # Production management
│   ├── session-state/           # Session state (gitignored)
│   └── session-logs/            # Session logs (gitignored)
│
├── package.json                 # Frontend dependencies
├── requirements.txt             # Backend dependencies
├── pyproject.toml               # Python project config
├── tsconfig.json                # TypeScript config
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # Project overview
└── LICENSE                      # License file
```

---

## Domain Agent Ownership

### frontend-lead / frontend-dev

| Directory | Role |
|-----------|------|
| `src/frontend/` | Owner |
| `tests/frontend/` | Owner |
| `docs/architecture/frontend-*.md` | Owner |

### backend-lead / api-dev

| Directory | Role |
|-----------|------|
| `src/backend/api/` | Owner |
| `src/backend/services/` | Owner |
| `tests/backend/api/` | Owner |
| `tests/backend/services/` | Owner |
| `docs/api/` | Owner |

### backend-lead / database-dev

| Directory | Role |
|-----------|------|
| `src/backend/models/` | Owner |
| `src/backend/repository/` | Owner |
| `migrations/` | Owner |
| `tests/backend/models/` | Owner |

### devops-dev

| Directory | Role |
|-----------|------|
| `docker/` | Owner |
| `scripts/` | Owner |
| `.github/workflows/` | Owner |

### architect-lead

| Directory | Role |
|-----------|------|
| `docs/architecture/adr/` | Owner |
| `docs/architecture/system-*.md` | Owner |
| Cross-domain coordination | Authority |

---

## Key Files

### Configuration Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Claude Code project config |
| `.claude/settings.json` | Agent permissions |
| `.env.example` | Environment template |
| `docker-compose.yml` | Local development |
| `docker-compose.prod.yml` | Production config |

### Entry Points

| File | Purpose |
|------|---------|
| `src/frontend/main.tsx` | Frontend entry |
| `src/backend/main.py` | Backend entry (FastAPI) |
| `migrations/env.py` | Migration runner |

---

## Ignored Directories

These directories are gitignored but used during development:

| Directory | Purpose |
|-----------|---------|
| `node_modules/` | Frontend packages |
| `__pycache__/` | Python bytecode |
| `.pytest_cache/` | Pytest cache |
| `production/session-state/` | Session persistence |
| `production/session-logs/` | Session logs |
| `.env` | Local secrets |

---

## Naming Conventions

### Files

| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `Button.tsx` |
| Module | snake_case | `user_service.py` |
| Test | Component.test | `Button.test.tsx` |
| Spec | lowercase | `users-api.md` |
| Migration | Revision + desc | `001_add_users.py` |

### Directories

| Type | Convention | Example |
|------|------------|---------|
| Module | snake_case | `components/`, `services/` |
| Domain | lowercase | `frontend/`, `backend/` |
| Feature | snake_case | `user_profile/` |

---

## Best Practices

1. **Keep domains separate**: Don't mix frontend/backend in same directory
2. **Mirror tests to source**: Test directory mirrors source structure
3. **Document in docs**: Not in source code directories
4. **Scripts in scripts/**: Not scattered in project
5. **CI/CD in .github/**: Standard location for workflows