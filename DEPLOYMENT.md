# Getting Campaign Manager Mini Running

So you've got this Campaign Manager system and want to deploy it somewhere. Let me show you how to run it locally for development and get it into production. I've set this up to be pretty straightforward.

## What You Need First

### Basic Requirements
You'll need Docker installed if you want the easy route. For production, you'll want Kubernetes, but that's optional for learning/testing.

You'll want at least 2 CPU cores and 4GB RAM for decent performance. 4 cores and 8GB is better if you're doing real testing.

## Environment Setup

### Config File

Start by copying the example config:

```bash
cp .env.example .env
```

Then edit `.env` with your real values. Here's what you need:

```env
# Database stuff - REQUIRED
POSTGRES_HOST=localhost          # or 'db' for Docker
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_actual_db_password

# Redis queue (for events)
REDIS_URL=redis://localhost:6379  # 'redis://redispubsub:6379' for Docker

# Web server
API_PORT=8000

# Worker settings
WORKER_CONCURRENCY=4

# Security key for JWT tokens - PICK A GOOD ONE
SECRET_KEY=some-really-long-random-key-make-it-secure

# How noisy you want the logs
LOG_LEVEL=INFO
```

Those secrets (password, JWT key) should never go into git. Keep them protected.

## Local Development Deployment

### Using Docker Compose (Recommended)

1. **Start all services**:
```bash
make up
# OR manually:
docker-compose -f infra/docker-compose.yml up -d
```

2. **Check service status**:
```bash
docker-compose ps
# Verify: postgres, redispubsub, fastapi-api, worker all show 'Up'
```

3. **View logs**:
```bash
docker-compose logs -f
# OR:
make logs
```

4. **Test the API**:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Interactive API documentation
```

### Manual Development Setup

1. **Database Setup**:
```bash
# Install PostgreSQL locally, create database:
createdb postgres
psql postgres -c "CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';"
```

2. **Redis Setup**:
```bash
# Install Redis locally, start service
redis-server
```

3. **Run Services**:
```bash
# Terminal 1 - Start API
uvicorn api.main:app --reload --host 0.0.0.0

# Terminal 2 - Start Worker
python worker/main.py

# Terminal 3 - Test API (optional)
python -m pytest tests/
```

## Production Deployment

### Container Image Building

1. **Build API Image**:
```bash
docker build -f infra/docker/Dockerfile.api -t campaign-manager-api:latest .
```

2. **Build Worker Image**:
```bash
docker build -f infra/docker/Dockerfile.worker -t campaign-manager-worker:latest .
```

3. **Push to Registry**:
```bash
# Tag for your registry
docker tag campaign-manager-api:latest your-registry.com/campaign-manager-api:v1.0.0
docker tag campaign-manager-worker:latest your-registry.com/campaign-manager-worker:v1.0.0

# Push images
docker push your-registry.com/campaign-manager-api:v1.0.0
docker push your-registry.com/campaign-manager-worker:v1.0.0
```

### Kubernetes Production Setup

1. **Create Namespace**:
```bash
kubectl create namespace campaign-manager
```

2. **Create Secrets**:
```bash
# Database secret
kubectl create secret generic db-secret \
  --from-literal=username=postgres \
  --from-literal=password=your_secure_db_password \
  --namespace=campaign-manager

# JWT secret
kubectl create secret generic jwt-secret \
  --from-literal=secret-key=your-256-bit-secret-key-here \
  --namespace=campaign-manager
```

3. **Update Manifests**:
Edit `infra/k8s/` files to reference your image registry and update resource limits.

4. **Deploy Services**:
```bash
kubectl apply -f infra/k8s/secret.yaml
kubectl apply -f infra/k8s/configmap.yaml
kubectl apply -f infra/k8s/api-deployment.yaml
kubectl apply -f infra/k8s/worker-deployment.yaml
kubectl apply -f infra/k8s/service.yaml
kubectl apply -f infra/k8s/hpa.yaml
```

5. **Verify Deployment**:
```bash
kubectl get pods -n campaign-manager
kubectl get svc -n campaign-manager
kubectl logs -f deployment/api -n campaign-manager
```

6. **Test Production Endpoint**:
```bash
# Get external IP/port
kubectl get svc campaign-manager-service -n campaign-manager
curl http://<EXTERNAL-IP>:80/health
```

### External Database Setup

For production environments, use managed PostgreSQL:

#### AWS RDS
```bash
# Update .env with RDS endpoint
POSTGRES_HOST=your-rds-endpoint.us-east-1.rds.amazonaws.com
POSTGRES_DB=campaign_manager_prod
```

#### Google Cloud SQL
```bash
# Update .env for Cloud SQL Proxy
POSTGRES_HOST=127.0.0.1
# Configure Cloud SQL Proxy separately
```

## Monitoring Setup

### Prometheus Metrics

The API exposes Prometheus metrics at `/metrics`:

```bash
curl http://localhost:8000/metrics
```

### Sample Prometheus Configuration

```yaml
global:
  scrape_interval: 30s

scrape_configs:
  - job_name: 'campaign-manager'
    static_configs:
      - targets: ['your-deployment-host:8000']
    metrics_path: /metrics
```

### Grafana Dashboard Setup

1. **Import Sample Dashboard**:
   - JSON model available for campaign manager metrics
   - Create visualizations for:
     - Events processed per minute
     - Campaign match rates
     - Worker processing latency
     - Queue depth monitoring

## Scaling Configuration

### Horizontal Pod Autoscaling (HPA)

The included HPA automatically scales based on CPU usage:

```yaml
# Default: Scale between 1-10 pods at 70% CPU
# Adjust in infra/k8s/hpa.yaml for your needs
```

### Worker Concurrency

Control background worker scaling via environment variable:

```env
WORKER_CONCURRENCY=8  # Increase for higher throughput
```

### Database Connection Pooling

The system uses SQLAlchemy connection pooling. Configure pool sizes:

```env
# Add to environment variables for advanced tuning
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_MAX_OVERFLOW=40
```

## High Availability Setup

### Multi-Region Deployment

Deploy across multiple regions:

1. **Separate Kubernetes clusters** per region
2. **Cross-region database replicas** for low-latency reads
3. **Redis Cluster** for multi-region message queue
4. **Load balancer** routing traffic to closest region

### Disaster Recovery

1. **Database backups**: Automated daily backups with point-in-time recovery
2. **Container registry**: Multi-region image hosting
3. **Configuration backup**: All manifests versioned in git
4. **DNS failover**: Automatic routing to backup regions

## Troubleshooting Production Issues

### Common Deployment Problems

**Pods Failing to Start**:
```bash
kubectl describe pod <pod-name> -n campaign-manager
# Check: Image pull errors, resource limits, config map mounting
```

**Services Not Accessible**:
```bash
kubectl get endpoints -n campaign-manager
# Check: Service selectors matching pod labels
```

**Database Connection Issues**:
```bash
kubectl logs deployment/worker -n campaign-manager
# Check: Network policies, security groups, DNS resolution
```

### Performance Monitoring

**Resource Utilization**:
```bash
kubectl top pods -n campaign-manager
kubectl top nodes
```

**Application Metrics**:
```bash
kubectl port-forward svc/campaign-manager-service 8080:80 -n campaign-manager
curl http://localhost:8080/metrics
```

## Security Deployment Checklist

- ✅ **HTTPS enabled** on load balancer
- ✅ **Secrets in K8s secrets** (not config maps)
- ✅ **RBAC configured** for cluster access
- ✅ **Resource limits** set to prevent DoS
- ✅ **Network policies** restrict pod communication
- ✅ **Security contexts** with non-root users
- ✅ **Regular image scanning** for vulnerabilities

This deployment configuration provides a production-ready setup capable of handling enterprise-scale event processing with high reliability and observability.
