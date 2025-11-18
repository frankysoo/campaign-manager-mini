# Logging and Monitoring Baselines

This document explains the logging setup, how logs flow through the system, and how to ship logs to external services like Stackdriver (Google Cloud Logging).

## Logging Configuration

The application uses JSON-formatted logging for structured logs that can be easily parsed by log aggregation systems.

### Local Development

For local development, logs are output to console and rotated files:

- **Console**: JSON formatted logs visible in terminal
- **File Rotation**: Logs written to `logs/campaign-manager.log` with rotation at 10MB, keeping 5 backups

### Configuration Files

- Use `infra/logging/logging.json` to configure logging behavior
- Set log level via `LOG_LEVEL` environment variable (INFO, DEBUG, WARNING, ERROR)

## Log Flow and Correlation

### API → Worker Log Flow

1. **API** receives event and publishes to Redis queue
   - Logs event receipt with `trace_id`
   - Publishes message to Redis

2. **Worker** consumes message from Redis queue
   - Attaches same `trace_id` from message
   - Processes event and logs outcome
   - Ensures trace_id flows through entire chain

### Correlation ID (trace_id) Requirement

Every log entry must include a `trace_id` for request correlation:

```json
{
  "asctime": "2023-11-18T16:30:00",
  "name": "api.routers.events",
  "levelname": "INFO",
  "message": "Event received",
  "trace_id": "abc123-def456-ghi789"
}
```

## Monitoring and Alerting

### Health Checks

- `/health` endpoint for API liveness
- Redis connectivity check for worker liveness
- Database connectivity check in readiness probes

### Metrics to Monitor

- Queue depth (Redis LLEN)
- Processing latency per event
- Error rates
- Resource utilization (CPU/Memory)

## Shipping Logs to Stackdriver (GCP)

To ship logs to Google Cloud Logging (Stackdriver):

1. **Install Google Cloud Logging agent** on your infrastructure

2. **Configure logging export** in GCP Console under Logging > Exports

3. **Use structured logging** with JSON formatter (already configured)

4. **Set trace_id** consistently across services for proper correlation

Example Kubernetes config for log shipping:

```yaml
# Add to deployment spec
spec:
  template:
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:1.9
        # Config for Stackdriver export
```

## Structured Logging Best Practices

- No `print()` statements - all output through logging
- Include relevant context (trace_id, service name)
- Use appropriate log levels
- Log errors with stack traces
- Avoid sensitive data in logs
