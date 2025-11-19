I built Campaign Manager Mini to solve a real problem I saw in e-commerce businesses. Let me walk you through how this whole thing works - I want to explain it so clearly that you'll understand every decision I made and every file in this project.

## The Problem That Started Everything

I kept hearing from online store owners about this one big challenge: how do you automatically reward your best customers at scale? "Send an email when someone spends over $100" or "give free shipping for frequent buyers" - these business rules are easy to describe but nearly impossible to implement reliably when you have thousands of customers.

Every purchase becomes a "customer event" that needs instant processing. Do it manually and you miss opportunities. Do it with poorly designed automation and you get:
- Customers not getting their rewards
- Systems crashing under load
- No way to change rules quickly
- No visibility into what's working

That's what motivated this project.

## The Architecture That Makes It Work

I designed this as an event-driven system - three main parts that talk through messages:

**The API Layer** - A FastAPI web service that accepts customer events and manages reward rules
**The Queue** - Redis to temporarily hold events (stops everything from crashing if one part gets busy)
**The Worker** - Background processors that check events against rules and decide rewards

Here's why this design works so well:
- If your website gets 10x traffic, just add more API servers
- If you need complex rules, add more workers
- Everything scales independently
- Never lose customer events, even under load

## Building the Core System

### Starting with the API (Why FastAPI?)

I chose FastAPI because it gives you:
- Type safety (Python 3.11+ with full type hints)
- Automatic OpenAPI docs (so other teams can integrate easily)
- Async support (handles thousands of concurrent requests)
- Pydantic validation (prevents bad data from breaking everything)

The API files look like this:

**api/main.py** - This starts the FastAPI server and connects all the routers. It's where I define the /health endpoint that checks if everything is working.

**api/routers/events.py** - Handles incoming customer events. This validates the data, adds some tracking info, and sends it to Redis for processing.

**api/routers/campaigns.py** - Where marketing teams create and update reward rules. This has become more complex now with authentication - only admin users can create campaigns to prevent security issues.

**api/schemas/** - Data validation models. If someone sends malformed data, these Pydantic schemas catch it immediately instead of letting bad data corrupt the database.

**api/db.py** - Database connection setup. I use async PostgreSQL because:
- ACID compliance (important for financial/reward systems)
- JSON columns for complex rule storage
- Native async support with SQLAlchemy
- More reliable than document databases for this use case

## The Background Worker (Because Nothing Should Block)

The worker is separate because processing rules can take time, and I didn't want the customer experience slowed down.

**worker/main.py** - Starts the async event loop
**worker/consumer.py** - Listens to Redis for new events
**worker/processor.py** - The brains of the operation:
- Loads active campaigns from database
- Runs events through the rule engine
- Saves successful matches
- Has built-in retry logic for reliability

I built in protections like idempotency (events only process once) because if customers accidentally trigger events multiple times, they shouldn't get rewarded more than once.

### The Rule Engine (Why Complex Rules Matter)

The original system only supported simple rules like "event_type equals 'purchase'". But real marketing teams need things like:
- "Purchase amount greater than $50 AND user is in gold loyalty group"
- "First purchase OR (purchase with high rating AND within 30 days)"
- Nested conditions with AND/OR/NOT

So I built **common/rule_engine.py** - a recursive rule evaluator that parses these complex conditions. It's like writing a mini programming language for marketing teams.

## Reliability Features (Because Production Systems Break)

From day one, I focused on making this production-ready:

**Error Handling:**
- Exponential backoff retries (don't flood failing systems)
- Dead letter queue for events that fail permanently
- Structured logging with correlation IDs

**Health Checks:**
- `/health` endpoint that runs automated tests
- Readiness probes for Kubernetes deployment
- Graceful shutdown handling

**Monitoring Now:**
- Prometheus metrics because you can't fix what you can't measure
- Counters for events processed, campaigns matched, errors
- Response times and queue sizes

**Authentication Now:**
- JWT tokens because you can't have marketing teams accidentally breaking campaigns
- Role-based access (admin vs regular users)
- Secure password hashing

## Infrastructure Choices

**Local Development:**
- Docker Compose because everyone should be able to run this locally
- PostgreSQL + Redis + Adminer (database viewing tool)
- Makefile shortcuts because running long commands sucks

**Production Deployment:**
- Kubernetes manifests because modern cloud platforms use it
- Horizontal scaling with HPA (add more servers when busy)
- ConfigMaps/Secrets for secure configuration
- Multi-stage Dockerfiles for smallest possible images

**Development Workflow:**
- GitHub Actions CI/CD because automated testing catches bugs before they ship
- flake8/MyPy/Black because consistent code is maintainable code
- Pre-commit hooks because let's catch issues immediately

## The Testing Strategy

I built comprehensive testing because bugs in reward systems cost companies money:

**Unit Tests:**
- test_matching.py: Tests rule logic with edge cases
- test_rule_engine.py: Tests complex condition combinations
- test_idempotency.py: Ensures duplicates are handled

**Integration Tests:**
- test_full_flow.py: Tests API → Queue → Worker → Database end-to-end

**Local Testing:**
- Makefile has `make test` shortcut
- CI runs everything on every code change

## Configuration Management

I centralized all settings in **common/config.py** because scattered env vars are hard to manage:

- Database connection strings
- Redis URLs
- Security settings (JWT secret)
- Worker concurrency settings

Everything validates at startup - if you forget to set the Postgres password, it fails immediately with a clear error rather than mysterious connection issues later.

## Where the Code Lives

Let me walk you through every important file and why it exists:

### Core Application Files:
**api/main.py** - FastAPI app setup, connects all routers, health checks
**api/db.py** - Database connection with proper async SQLAlchemy setup
**api/models.py** - SQLAlchemy models for campaigns and events tables
**api/schemas/** - Pydantic validation (campaign rules, event formats)
**api/routers/** - HTTP endpoint handlers (campaigns, events, auth now)
**api/utils/** - Helper functions (message publishing, logging)

### Worker Files:
**worker/main.py** - Async consumer startup
**worker/consumer.py** - Redis message listener
**worker/processor.py** - Core business logic (rule matching, saving results)
**worker/db.py** - Worker-side database connection
**worker/utils/idempotency.py** - Duplicate prevention system

### Shared Utilities:
**common/config.py** - Central configuration management
**common/constants.py** - Universal constants and settings
**common/utils.py** - Shared helper functions (validation, retries, JSON)
**common/auth.py** - Authentication and authorization system
**common/rule_engine.py** - Complex rule evaluation engine
**common/metrics.py** - Prometheus monitoring system

### Testing:
**tests/unit/** - Component testing
**tests/integration/** - Full system testing

### Infrastructure:
**infra/docker-compose.yml** - Local development environment
**infra/k8s/** - Production deployment manifests

## How I Enhanced It (The Journey)

This started as a simple proof-of-concept, but I kept thinking about production use:

**Version 1:** Basic rule matching
**Version 2:** Added authentication for security
**Version 3:** Built a sophisticated rule engine for complex conditions
**Version 4:** Added comprehensive monitoring and metrics

Each enhancement made it more enterprise-ready. The rule engine alone went from simple string matching to a full recursive expression evaluator.

## Why You'd Hire Someone Who Built This

This project shows someone who:
- Thinks about scale from day one
- Understands the full software lifecycle
- Knows how to build reliable systems
- Uses modern Python patterns
- Understands cloud-native architecture
- Balances speed with correctness
- Builds monitoring into everything
- Develops enterprise-grade authentication
- Tests thoroughly
- Documents comprehensively
- Configures infrastructure for production

## Running It Yourself

Get it running with Docker:

```bash
cp .env.example .env  # Configure your settings
make build
make up
curl http://localhost:8000/health  # Check if it's working
```

Then hit the API endpoints documented in docs/api_endpoints.md.

## The Technical Philosophy

I believe software should be:
- **Reliable** - Handles errors gracefully
- **Scalable** - Grows with your business
- **Maintainable** - Easy for teams to work with
- **Observable** - You know what's happening
- **Secure** - Protects sensitive business logic

Every file in this project reflects these principles. I built what I would want to work with - and what I would trust to handle real customer rewards at scale.

That's the story of Campaign Manager Mini. I built it to solve a real problem, made it production-ready, and scaled it up. It's the kind of system I'd be proud to ship to production.
