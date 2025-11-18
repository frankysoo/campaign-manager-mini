# Demo Script for Campaign Manager Mini

This script demonstrates the full functionality of the Campaign Manager Mini system in a production-like setup using Docker Compose.

## 1. Problem Introduction

Campaign Manager Mini is a production-grade, event-driven system that processes user events against predefined campaign rules. It uses FastAPI, Redis, PostgreSQL, and a worker process to handle matching and storage.

## 2. Architecture Overview

The system follows an event-driven architecture:

```
Event Source → FastAPI API → Redis Queue → Worker → PostgreSQL
                 ↓
              /health
              /campaigns
                 ↓
               /events
                 ↓
              Publishes
                 ↓
             Consumes
                 ↓
             Matches_rules
                 ↓
             Saves_result
```

Key components:
- **API**: REST endpoints for campaigns and events
- **Worker**: Background processor for rule matching
- **Redis**: Message queue for decoupling
- **PostgreSQL**: Persistent storage

## 3. Create Campaign

First, start the system in clean state:

```bash
# Clean up previous runs
docker-compose down -v
docker system prune -f

# Build and start services
docker-compose up --build -d

# Wait for health (API startup)
sleep 30
curl http://localhost:8000/health
```

Create a campaign:

```bash
curl -X POST http://localhost:8000/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Purchase Campaign",
    "rules": {
      "event_type": "purchase"
    }
  }'
```

Response should include campaign ID.

## 4. Send Event

Submit an event that matches the campaign:

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt-123",
    "payload": {
      "event_type": "purchase",
      "user_id": "user001",
      "amount": 150.00
    }
  }'
```

This publishes to Redis queue.

## 5. Worker Processes

Worker consumes from queue and applies rules:

```bash
# Check worker logs
docker-compose logs worker --tail=10 --follow
```

You should see logs indicating:
- Message consumed
- Rules matched
- Result saved to database

## 6. Database Updated

Verify the match was saved:

```bash
# Check database
docker-compose exec postgres psql -U postgres -d postgres -c \
"SELECT * FROM campaign_matches;"

# Expected: 1 row with campaign_id, event_id, matched_at
```

## 7. Tests Green

Run the full test suite:

```bash
make test
# or
pytest -q

# All tests should pass
pytest tests/integration/test_full_flow.py
```

## 8. Clean Flow Demonstration

Monitor the complete flow:

```bash
# Tail API logs
docker-compose logs api --tail=5 --follow &
echo ""

# Tail worker logs
docker-compose logs worker --tail=5 --follow &
echo ""

# Send another event
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt-456",
    "payload": {
      "event_type": "purchase"
    }
  }'
```

Observe processing in logs.

## Demo Verification

For a complete demo, ensure:
- Services are running and healthy
- API responds to requests
- Worker consumes messages
- Database receives matches
- Tests pass consistently
- Logs are clean and structured (no errors)
- System handles duplicate events gracefully

## Commands Summary

```bash
# Setup
docker-compose down -v
docker-compose up --build -d
sleep 30

# Demo
curl http://localhost:8000/health
curl -X POST http://localhost:8000/campaigns -H "Content-Type: application/json" -d '{"name":"Demo","rules":{"event_type":"purchase"}}'
curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '{"event_id":"demo-evt","payload":{"event_type":"purchase"}}'

# Check
docker-compose logs worker | tail -10
docker-compose exec postgres psql -U postgres -d postgres -c "SELECT * FROM campaign_matches;"
make test
