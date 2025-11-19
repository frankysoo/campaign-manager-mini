# Campaign Manager Mini

An enterprise-grade, event-driven campaign management system designed for handling complex marketing campaigns with real-time event processing, JWT authentication, advanced rule engines, and production-ready monitoring.

**Key Features:**
- **Event-Driven Architecture** with Redis messaging
- **Advanced Campaign Rules** supporting logical operations (AND/OR/NOT)
- **JWT Authentication** with role-based access control
- **Prometheus Monitoring** with comprehensive metrics
- **Production-Ready** with Kubernetes deployment
- **Full Test Coverage** with CI/CD pipeline

**Technology Stack:**
- **Backend:** Python 3.12, FastAPI, PostgreSQL, Redis
- **Authentication:** JWT tokens with role-based permissions
- **Monitoring:** Prometheus metrics and structured logging
- **Deployment:** Docker containers, Kubernetes manifests
- **Quality:** CI/CD with testing, linting, and security scanning

## Project Summary

This project demonstrates a scalable, event-driven campaign management system. Events are received via API, published to a queue (Redis), consumed by workers, matched against campaign rules, and results are saved to PostgreSQL.

## Architecture

```
Event Source --> FastAPI API --> Redis Pub/Sub --> Worker --> PostgreSQL
     |               |               |              |
  User/Batch       /events/*     publish/get    match & save
                      /campaigns
```

## How to Run

### Local Development

1. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
2. Run PostgreSQL and Redis locally or use docker-compose.
3. Set `.env` from `.env.example` (note: POSTGRES_PASSWORD is now required).
4. Run API: `uvicorn api.main:app --reload`
5. Run Worker: `python worker/main.py`

### Docker (Recommended)

```bash
make build
make up
```

Check logs: `docker-compose logs -f`

Health: `curl http://localhost:8000/health`

### Kubernetes (Production)

Apply K8s manifests in `infra/k8s/`:
```bash
make k8s-apply
```

## API Endpoints

**Authentication:**
- `POST /auth/token` - Login for access token
- `GET /auth/users/me` - Get current user info

**Campaigns:**
- `POST /campaigns` - Create campaign (admin only)
- `GET /campaigns` - List campaigns
- `GET /campaigns/{id}` - Get single campaign

**Events:**
- `POST /events` - Send event for processing

**System:**
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

See API docs at `http://localhost:8000/docs`

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Database**: PostgreSQL, SQLAlchemy (async)
- **Queue**: Redis Pub/Sub
- **Containerization**: Docker, Docker Compose
- **Tests**: pytest, pytest-asyncio
- **Linting**: flake8
- **Formatting**: Black
- **CI**: GitHub Actions

## Testing Commands

```bash
make test
pytest -q -v
pytest tests/unit/test_matching.py
```

## Folder Structure

```
campaign-manager-mini/
├── api/
│   ├── main.py, routers/, models.py, db.py, schemas/
├── worker/
│   ├── main.py, consumer.py, processor.py, db.py, utils/
├── tests/
│   ├── unit/, integration/
├── infra/
│   ├── docker/, docker-compose.yml, k8s/
├── docs/
├── .github/workflows/ci.yml
├── Makefile, README.md, requirements*.txt
```

## Current Limitations

- Basic idempotency handling (uses database constraints)
- Single worker instance (suitable for demo/production scaling via K8s)
- Complex rule evaluation may have performance implications at extreme scale
- No email notification system (campaign triggers are stored in database)

## Roadmap & Enhancements

**Implemented:**
- ✅ **Advanced Rule Engine** supporting logical operations (AND/OR/NOT, nested conditions)
- ✅ **JWT Authentication** with role-based access control (admin/user)
- ✅ **Prometheus Monitoring** with comprehensive metrics and observability
- ✅ **Enterprise Security** including input validation and data protection
- ✅ **Production Deployment** ready with Kubernetes manifests and scaling

**Future Considerations:**
- GraphQL API support
- Real-time campaign performance dashboards
- External service integrations (Salesforce, email providers)
- Machine learning for campaign optimization
- Multi-region global deployments

## Quality Gates and CI/CD

### Code Quality

- **Linting**: flake8 with strict PEP8 enforcement
- **Type Checking**: mypy with strict mode
- **Formatting**: Black and isort
- **Testing**: pytest with coverage >80%

Run quality checks:

```bash
make lint
make test
make fmt
```

### CI Pipeline

GitHub Actions runs on push/PR:
- Dependency caching
- Linting and type checking
- Automated tests
- Docker build and health checks

See `.github/workflows/ci.yml`

## Logging and Monitoring

- **Structured Logging**: JSON format with trace_id correlation
- **Health Checks**: `/health` endpoint for API
- **Metrics**: Queue depth, processing latency, error rates

See `infra/logging/` for configuration.

## Infrastructure

### Docker

Multi-stage builds with security best practices:
- Non-root users
- Minimal images
- Health checks

Run locally:

```bash
make build
make up
make logs
```

### Kubernetes

Production-ready manifests with:
- Resource limits and requests
- Liveness/readiness probes
- HPA for auto-scaling
- ConfigMaps and Secrets

```bash
make k8s-apply
make k8s-delete
```
