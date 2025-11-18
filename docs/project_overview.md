# Campaign Manager Mini - Project Overview

## Overall Project Idea

Campaign Manager Mini is a system that helps businesses automatically trigger campaigns when certain events happen. For example, when a user makes a purchase on your website, it could automatically start a special promotional campaign for that user. The system uses modern technology to handle events coming in, process them quickly, and store the results in a database. It's built to be reliable, easy to run, and ready for real-world use.

The project teaches event-driven architecture, where different parts of the system talk to each other through messages, making it fast and scalable. It's like a warehouse where packages (events) arrive, get sorted (processed), and then stored in shelves (database).

---

## Folder Structure and File Explanations

### Root Files (General Setup)
- **README.md**: The welcome page of the project. It has everything you need to know: what the project does, how to run it, API examples, and links. Read this first to understand the big picture.
- **requirements.txt**: List of all main packages the project needs (like FastAPI, SQLAlchemy). Install with `pip install -r requirements.txt`.
- **requirements-dev.txt**: Extra packages for development (like pytest for testing, black for code formatting). For developers who want to work on the code.
- **.gitignore**: Tells Git which files to ignore (like temporary files or virtual environment). Keeps the repository clean.
- **.env.example**: Example of environment variables (database URLs, Redis settings). Copy to `.env` and fill in real values.
- **Makefile**: Shortcuts for common commands (like `make build` to build containers, `make test` to run tests). Makes life easier.
- **.github/workflows/ci.yml**: Instructions for GitHub to automatically test the code when you make changes. Ensures code quality.

### Configuration Files
- **.flake8**: Linting rules to enforce code style (PEP8, line lengths, complexity).
- **pyproject.toml**: Black formatter config and isort import sorter rules).
- **.mypy.ini**: Type checking rules for strict mypy validation.

### api/ (Application Programming Interface - User Facing Part)
This handles web requests from users or other systems.

- **api/main.py**: The entry point for the web server. Sets up FastAPI, connects routers for campaigns and events, and starts the app. It's like the main door to the house.
- **api/db.py**: Code to connect to the database. Uses SQLAlchemy for safe, async database operations. Needed because the API saves and reads campaign data.
- **api/models.py**: Defines the database tables (Campaign and Event). Like blueprints for how data is stored in the database.
- **api/schemas/ (Data Models)**
  - **campaign.py**: Describes what a campaign looks like in requests/responses (name, rules). Pydantic ensures data is valid.
  - **event.py**: Describes what an event looks like. Keeps data safe and clear.
- **api/routers/ (Route Handlers)**
  - **campaigns.py**: Handles requests for campaigns (create, list). Like a librarian for campaign books.
  - **events.py**: Handles requests for events (send event). Forwards events to the worker via message queue.
- **api/utils/ (Helpers)**
  - **publisher.py**: Sends messages to the queue (Redis) for the worker to pick up. Decouples API from processing.
  - **logger.py**: Helper for logging messages. Tracks what the API is doing for debugging.

### worker/ (Background Processing)
Processes events in the background without making users wait.

- **worker/main.py**: Starts the worker program. Sets up logging and begins listening for messages.
- **worker/db.py**: Same as api/db.py - connects to the database for the worker to save results.
- **worker/consumer.py**: Listens to the message queue (Redis) for new events. Like a mailman watching the mailbox.
- **worker/processor.py**: The brain of the worker. Matches events to campaigns, checks if already processed, and saves to database.
- **worker/utils/ (Helpers)**
  - **logger.py**: Same as API logger but for worker.
  - **idempotency.py**: Ensures the same event isn't processed twice. Important for reliability.

### tests/ (Quality Assurance)
Code to test everything works correctly.

- **tests/unit/test_matching.py**: Tests the logic for matching events to campaigns. Small, fast tests.
- **tests/unit/test_idempotency.py**: Tests that duplicate events are handled right.
- **tests/integration/test_full_flow.py**: Tests the whole system end-to-end (API to DB). Slower but comprehensive.

### infra/ (Infrastructure - Running the System)
Tools to run everything together, especially in production.

- **infra/docker-compose.yml**: Recipe for running multiple services (API, DB, Redis, Worker) locally with Docker.
- **infra/docker/ (Docker Images)**
  - **Dockerfile.api**: Instructions to build the API container. Like packaging the house for travel.
  - **Dockerfile.worker**: Builds the worker container.
  - **Dockerfile.pubsub**: Builds the Redis container (though mostly uses official image).
- **infra/k8s/ (Kubernetes - Cloud Deployment)**
  - **api-deployment.yaml**: Tells Kubernetes how to run the API in the cloud.
  - **worker-deployment.yaml**: For the worker.
  - **service.yaml**: Exposes the API outside the cluster.
  - **hpa.yaml**: Auto-scales the API based on CPU usage.

### docs/ (Documentation)
All the guides and explanations.

- **docs/architecture.md**: Big picture of how components work together, with diagrams.
- **docs/api_endpoints.md**: Details of each API endpoint with examples.
- **docs/message_schema.md**: What data looks like going in/out.
- **docs/troubleshooting.md**: Common problems and fixes.
- **docs/decisions.md**: Why we chose certain technologies.
- **docs/project_overview.md**: This file - summary you're reading.

---

## How It All Works Together (Simple Flow)
1. **User sends event**: API receives it via POST /events, validates, and sends to Redis queue.
2. **Worker picks up**: Listens to queue, checks if seen before, matches to campaigns (e.g., if event_type matches).
3. **Saves results**: Inserts event with triggered campaign IDs into database.
4. **User checks**: Can query campaigns or events via API endpoints.

Why build it this way? To separate concerns (API responds fast, worker processes slowly), use async for performance, and Docker for easy deployment. It's production-ready: handles concurrency, idempency, logging, and works with databases and queues.
