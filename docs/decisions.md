# Architectural Decisions

## Why FastAPI?
- FastAPI provides automatic API documentation, async support, and Pydantic validation.
- Built on ASGI, scales well for async operations.
- Trade-off: Learning curve, but for this demo, it's production-ready.

## Why Async Throughout?
- Async endpoints for handling concurrent requests.
- Async DB connections (asyncpg) and Redis client.
- Trade-off: Complexity in code, but necessary for performance.

## Why Redis Pub/Sub?
- Simple message queue for decoupling API and Worker.
- Easy to implement in Docker Compose.
- Trade-off: Not persistent, but no need for demo.

## Why PostgreSQL?
- Relational DB for structured data (campaigns, events).
- ACID compliance for data integrity.
- Trade-off: Overhead vs NoSQL, but suits the use case.

## Why SQLAlchemy Async?
- Powerful ORM for async DB operations.
- Type safety and query building.
- Trade-off: Complexity over raw SQL, but good for model management.

## Why pytest for Tests?
- Popular, async support, fixtures.
- Trade-off: None, standard choice.

## Why Docker Compose for Dev Infra?
- Easy to set up multi-service local env.
- Health checks for reliable startup.
- Trade-off: Resource intensive locally.

## Why K8s Files (Minimal)?
- Provides HPA and deployments for scaling.
- Trade-off: Not fully tested, but shows intent.

## Why Single Worker Process?
- Simple for demo.
- Trade-off: No horizontal scaling, but works for development/demo. Production scales via K8s.

## Why Idempotency on event_id?
- Ensures events aren't processed twice.
- Trade-off: Race conditions possible if concurrent workers.

## Trade-offs Summary
- Faster development vs production polish.
- Event-driven architecture adds complexity but provides loose coupling.
- Minimal auth/security for simplicity.
- No metrics/logging aggregation, just basic logging.
