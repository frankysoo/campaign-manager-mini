# Architecture Diagram

```mermaid
graph TD
    A[Event Source] -->|HTTP POST| B[FastAPI API]
    B -->|Publish Message| C[Redis Queue]
    C -->|Consume Message| D[Worker Process]
    D -->|Match & Save| E[PostgreSQL DB]

    B --> F[Health Endpoint]
    C --> G[Pub/Sub Queue]
    D --> H[Idempotent Processing]

    subgraph "Docker Compose"
        I[postgres Container]
        J[redis Container]
        K[api Container]
        L[worker Container]
        M[adminer Container]
    end

    subgraph "Kubernetes"
        N[API Deployment + Service + HPA]
        O[Worker Deployment]
        P[ConfigMap + Secret]
        Q[Redis Service]
        R[Postgres Service]
    end

    classDef container fill:#e1f5fe
    classDef k8s fill:#f3e5f5
    classDef external fill:#fff3e0

    class I,J,K,L,M container
    class N,O,P,Q,R k8s
    class A,C,E external
```

## Component Descriptions

### API Service (FastAPI)
- Receives events via REST API
- Publishes events to Redis queue
- Provides health checks and campaign management
- Structured JSON logging with trace_id correlation

### Worker Service
- Consumes events from Redis queue
- Matches events against campaign rules
- Saves matching results to PostgreSQL
- Ensures idempotency with unique event IDs

### Data Flow
1. Event → API → Redis Queue → Worker → Database
2. Each step logs with consistent trace_id
3. Health checks ensure service reliability

### Infrastructure Isolation
- Docker Compose for local development
- Kubernetes manifests for production deployment
- Secrets management via K8s ConfigMaps/Secrets
