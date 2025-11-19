from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry

# Create a custom registry to avoid conflicts with other applications
registry = CollectorRegistry()

# API Metrics
events_received_total = Counter(
    'campaign_api_events_received_total',
    'Total number of events received via API',
    registry=registry
)

campaigns_created_total = Counter(
    'campaign_api_campaigns_created_total',
    'Total number of campaigns created via API',
    registry=registry
)

api_request_duration_seconds = Histogram(
    'campaign_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint', 'status'],
    registry=registry
)

# Worker Metrics
events_processed_total = Counter(
    'campaign_worker_events_processed_total',
    'Total number of events processed by worker',
    ['status'],  # 'success' or 'error'
    registry=registry
)

campaign_matches_total = Counter(
    'campaign_worker_campaign_matches_total',
    'Total number of campaign matches found',
    registry=registry
)

events_processing_time_seconds = Histogram(
    'campaign_worker_events_processing_time_seconds',
    'Time taken to process events',
    registry=registry
)

idempotent_event_skips_total = Counter(
    'campaign_worker_idempotent_event_skips_total',
    'Number of events skipped due to idempotency',
    registry=registry
)

# Queue Metrics
events_in_queue = Gauge(
    'campaign_events_in_queue',
    'Number of events currently in queue',
    registry=registry
)

dead_letters_total = Counter(
    'campaign_dead_letters_total',
    'Total number of events sent to dead letter queue',
    registry=registry
)

# Database Metrics
db_connections_active = Gauge(
    'campaign_db_connections_active',
    'Number of active database connections',
    registry=registry
)

db_query_duration_seconds = Histogram(
    'campaign_db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation'],  # 'select', 'insert', 'update', etc.
    registry=registry
)

# System Health
service_up = Gauge(
    'campaign_service_up',
    'Service health status (1 if up, 0 if down)',
    ['service'],  # 'api', 'worker'
    registry=registry
)
