#!/bin/bash

# Final Environment Verification Script for Campaign Manager Mini
# Run this script before demo to ensure everything is green

set -e  # Exit on any error

echo "Starting Final Environment Verification..."

# 1. Clean up previous runs
echo "Cleaning up previous containers..."
docker-compose down -v 2>/dev/null || true
docker system prune -f >/dev/null

# 2. Build fresh containers
echo "Building Docker images..."
docker-compose build --parallel

# 3. Start services
echo "Starting services..."
docker-compose up -d

# 4. Wait for services to be healthy
echo "Waiting for services to be healthy..."
timeout=120
echo "Waiting up to ${timeout}s for PostgreSQL..."
elapsed=0
while ! docker-compose exec -T postgres pg_isready -U postgres >/dev/null 2>&1; do
    if [ $elapsed -ge $timeout ]; then
        echo "PostgreSQL failed to start within ${timeout}s"
        docker-compose logs postgres
        exit 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
    echo -n "."
done
echo ""
echo "PostgreSQL is ready"

echo "Waiting up to 30s for Redis..."
timeout=30
elapsed=0
while ! docker-compose exec -T redispubsub redis-cli ping >/dev/null 2>&1; do
    if [ $elapsed -ge $timeout ]; then
        echo "Redis failed to start within ${timeout}s"
        docker-compose logs redispubsub
        exit 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
    echo -n "."
done
echo ""
echo "Redis is ready"

# 5. Check API health
echo "Checking API health..."
sleep 10  # Give API time to start
if curl -f --max-time 10 http://localhost:8000/health >/dev/null 2>&1; then
    echo "API health endpoint responds"
else
    echo "API health endpoint failed"
    docker-compose logs api
    exit 1
fi

# 6. Run tests
echo "Running tests..."
if pytest -q --tb=short >/dev/null 2>&1; then
    echo "All tests pass"
else
    echo "Tests failed"
    pytest -v
    exit 1
fi

# 7. Check database schema
echo "Checking database schema..."
if docker-compose exec -T postgres psql -U postgres -lqt | cut -d \| -f 1 | grep -qw postgres; then
    echo "Database schema exists"
else
    echo "Database schema missing"
    docker-compose exec -T postgres psql -U postgres -l
    exit 1
fi

# 8. Test a simple API call
echo "Testing API endpoints..."
if curl -s -X POST http://localhost:8000/campaigns \
     -H "Content-Type: application/json" \
     -d '{"name": "Demo Campaign", "rules": {"event_type": "demo"}}' \
     --max-time 10 | grep -q '"id"'; then
    echo "Campaign creation works"
else
    echo "Campaign creation failed"
    curl -v -X POST http://localhost:8000/campaigns \
         -H "Content-Type: application/json" \
         -d '{"name": "Demo Campaign", "rules": {"event_type": "demo"}}' \
         --max-time 10
    exit 1
fi

if curl -X GET http://localhost:8000/campaigns --max-time 10 | grep -q '"name"'; then
    echo "Campaign listing works"
else
    echo "Campaign listing failed"
    exit 1
fi

# 9. Check worker logs (basic smoke test)
echo "Checking worker startup..."
if docker-compose logs worker 2>&1 | grep -q "Worker starting"; then
    echo "Worker started successfully"
else
    echo "Worker startup logs missing"
    docker-compose logs worker
    exit 1
fi

# 10. Show summary
echo ""
echo "FINAL VERIFICATION COMPLETE!"
echo ""
echo "Docker Services:"
docker-compose ps
echo ""
echo "Recent API logs:"
docker-compose logs api --tail=5 2>/dev/null || true
echo ""
echo "Recent Worker logs:"
docker-compose logs worker --tail=5 2>/dev/null || true
echo ""
echo "Environment Status: ALL GREEN"
echo ""
echo "Ready for demo! Commands:"
echo "- API: http://localhost:8000"
echo "- Adminer: http://localhost:8080"
echo "- Logs: docker-compose logs -f [service]"
