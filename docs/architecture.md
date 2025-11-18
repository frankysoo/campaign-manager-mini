# Architecture

## System Diagram

```
                   +--------------+
                   | External     |
                   | Event Source |
                   +--------------+
                          |
                          | POST /events
                          v
                   +--------------+
                   | FastAPI API  |
                   +--------------+
                          |
                          | Publish to Redis (with validation & retry)
                          v
                   +--------------+
                   |    Redis     |
                   | Pub/Sub      |
                   +--------------+
                          |
                          | Subscribe to 'events'
                          v
                  +--------------+
                  |    Worker    |
                  | (Consumer)   |
                  |  + Retry/DLQ |
                  +--------------+
                          |
                          | Match & Process + Health Checks
                          v
                  +---------------+
                  | PostgreSQL DB |
                  | Events Table  |
                  +---------------+
```

## High-Level Flow

1. **Event Reception**: Client sends POST `/events` with validated payload using shared utils.
2. **Publishing**: API publishes validated event to Redis 'events' channel with correlation ID.
3. **Consumption**: Worker consumes from Redis with enhanced error handling and timeout recovery.
4. **Processing with Reliability**:
   - Checks event idempotency.
   - Queries active campaigns.
   - Applies campaign rules.
   - Saves results with retry logic.
   - DLQ handling for permanent failures.
5. **Monitoring**: All steps logged with structured JSON and correlation IDs across services.
6. **Health & Scaling**: Services expose health endpoints, auto-scale based on load.

## Components

- **API**: Built with FastAPI, provides CRUD for campaigns and event ingestion, includes health check.
- **Worker**: Python script using asyncio to consume from Redis, process events, and interact with DB.
- **Database**: PostgreSQL for relational storage of campaigns and event logs.
- **Queue**: Redis Pub/Sub for decoupling API and Worker.

## Technologies

- **Async All the Way**: Uvicorn, asyncpg, Redis async client for high concurrency.
- **ORM**: SQLAlchemy async for DB interactions.
- **Validation**: Pydantic for request/response schemas.
- **Testing**: pytest for unit and integration tests.
