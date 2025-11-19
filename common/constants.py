# Redis queue names
EVENTS_QUEUE = "events"

# Campaign rule operators
RULE_OPERATORS = ["equals", "greater_than", "less_than", "contains", "in", "between"]
LOGICAL_OPERATORS = ["and", "or", "not"]
DEAD_LETTER_QUEUE = "dead_letter_queue"

# Event types
EVENT_TYPE_PURCHASE = "purchase"
EVENT_TYPE_SIGNUP = "signup"

# Environment variable keys
POSTGRES_HOST = "POSTGRES_HOST"
POSTGRES_PORT = "POSTGRES_PORT"
POSTGRES_DB = "POSTGRES_DB"
POSTGRES_USER = "POSTGRES_USER"
POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
REDIS_URL = "REDIS_URL"
API_PORT = "API_PORT"
WORKER_CONCURRENCY = "WORKER_CONCURRENCY"
LOG_LEVEL = "LOG_LEVEL"

# Retry configuration
MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_FACTOR = 2  # seconds
