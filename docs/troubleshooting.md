# Troubleshooting

## Common Issues

### 1. API Does Not Start
- **Error:** Port 8000 already in use.
  - **Solution:** Kill process on port 8000 or change port: `uvicorn api.main:app --port 8001`

- **Error:** Module not found.
  - **Solution:** Activate venv: `pip install -r requirements.txt`

### 2. Worker Not Connecting to DB/Redis
- **Error:** Connection refused.
  - **Solution:** Ensure Docker containers are running: `docker-compose ps`. If not, `make up`.
  - For local, start local Redis/Postgres instances.

### 3. Tests Fail
- **Error:** pytest not found.
  - **Solution:** `pip install -r requirements-dev.txt`

- **Error:** Database tests fail (no connection).
  - **Solution:** Tests use mocked DB; if integration, need env running.

### 4. Container Problems

#### Docker Compose Not Starting
- Check logs: `docker-compose logs`
- Ensure ports are free: `netstat -an | grep :80`
- Remove volumes if corrupted: `make down`, then `docker volume prune`

#### Worker Not Consuming
- Check Redis logs: `docker-compose logs redis`
- Check if Redis IP is correct (in .env, localhost or service name)
- In Worker logs: `docker-compose logs worker --tail=20`

#### DB Migration Issues
- Remove volumes: `docker-compose down -v` (loses data)
- Or manually inspect DB: `docker-compost exec db psql -U postgres -d postgres`

#### Container Exits Immediately
- Check entrypoint: `docker run --rm <image> python -c "import api.main; print('OK')"`

### 5. GitHub Actions Fail
- Lint/format issues: Run `make lint`, `make format` locally.
- Build issues: Test `make build` locally.

### 6. K8s Deployment Issues
- Check pod statuses: `kubectl get pods`
- Check logs: `kubectl logs <pod>`
- Ensure images are available or pushed to registry.

### 7. Worker Reliability Issues
- Events failing after retries: Check DLQ in logs for permanently failed events
- Worker not starting: Verify common/config.py can load environment variables
- Timeout errors: Increase timeout values in constants.py for network issues
- Correlation ID missing: Check API and worker logging configuration

### 8. Performance/Race Conditions
- Multiple workers causing concurrent access: Use single worker for demo, or coordinate via Redis
- Idempotency failing: Check database connectivity and table constraints
- Queue overflow: Digital worker concurrency via WORKER_CONCURRENCY environment variable
- Memory leaks: Monitor container resource usage with docker stats

## General Tips
- Clear caches: `docker system prune -f`
- Check environment variables in .env
- Use ASCII for diagrams to avoid render issues.
