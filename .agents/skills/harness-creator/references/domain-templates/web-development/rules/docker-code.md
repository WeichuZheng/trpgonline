# Docker Code Rule

**Path Scope:** `docker/**/*`, `Dockerfile*`, `docker-compose*.yml`, `.github/workflows/**/*.yml`

**Severity:** STANDARD

---

## Rule: Docker and CI/CD Standards

All Docker and CI/CD configurations must follow these standards for security, reliability, and maintainability.

---

## Dockerfile Standards

### File Organization

```
docker/
├── frontend/
│   └── Dockerfile        # Frontend container
├── backend/
│   └── Dockerfile        # Backend container
├── nginx/
│   └── Dockerfile        # Nginx reverse proxy
docker-compose.yml        # Local development
docker-compose.prod.yml   # Production
docker-compose.staging.yml # Staging
```

### Dockerfile Template

```dockerfile
# Backend Dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Best Practices

1. **Use Specific Versions**: Never use `:latest`

```dockerfile
# GOOD
FROM python:3.11-slim
FROM node:18-alpine

# BAD
FROM python:latest  # Never use latest
FROM node:latest    # Never use latest
```

2. **Multi-stage Builds**: Reduce image size

```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

3. **Health Checks**: Every service needs health check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

---

## Docker Compose Standards

### Compose Template

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./src/frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - API_URL=http://backend:8000
    volumes:
      - ./src/frontend:/app
      - /app/node_modules
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build:
      context: ./src/backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@database:5432/app
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./src/backend:/app
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### Compose Best Practices

1. **No :latest Tags**

```yaml
# GOOD
image: postgres:15-alpine
image: redis:7-alpine

# BAD
image: postgres:latest  # Never
```

2. **Health Checks Required**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

3. **Environment Variables from .env**

```yaml
environment:
  - DATABASE_URL=${DATABASE_URL}  # From .env
  - SECRET_KEY=${SECRET_KEY}      # From .env
```

4. **Depends On with Condition**

```yaml
depends_on:
  database:
    condition: service_healthy  # Wait for health check
```

---

## CI/CD Standards

### GitHub Actions Template

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=src/backend --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage.xml

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: docker-compose build
      
      - name: Save images
        run: |
          docker save app-frontend:latest | gzip > frontend.tar.gz
          docker save app-backend:latest | gzip > backend.tar.gz
      
      - uses: actions/upload-artifact@v3
        with:
          name: docker-images
          path: '*.tar.gz'

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging
```

### CI/CD Best Practices

1. **Version Pin Actions**

```yaml
# GOOD
- uses: actions/checkout@v3
- uses: actions/setup-python@v4

# BAD
- uses: actions/checkout@main  # Unstable
```

2. **Matrix Testing**

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    node-version: ['16', '18', '20']
```

3. **Environment Secrets**

```yaml
environment: production
steps:
  - name: Deploy
    env:
      AWS_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
```

---

## Security Checklist

- [ ] No secrets in Dockerfiles/compose
- [ ] No :latest tags
- [ ] Health checks configured
- [ ] Environment variables from .env/secrets
- [ ] Resource limits set (production)
- [ ] Networks isolated appropriately
- [ ] Volumes for persistent data
- [ ] CI uses pinned action versions

---

## Anti-Patterns to Avoid

1. **:latest Tag**: Always use specific versions
2. **Hardcoded Secrets**: Use environment/secrets
3. **Missing Health Checks**: Every service needs one
4. **No Resource Limits**: Set limits in production
5. **Unpinned Actions**: Use versioned actions
6. **Missing Deps Conditions**: Wait for services
7. **No Volume Persistence**: Data lost on restart
8. **Root User**: Use non-root in containers