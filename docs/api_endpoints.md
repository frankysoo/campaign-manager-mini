# API Endpoints

All endpoints are prefixed with the base path (e.g., `http://localhost:8000`).

## Authentication Required

Some endpoints require authentication. Include the JWT token in the `Authorization` header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Authentication

### POST /auth/token

Get access token for authenticated user.

**Request Body (OAuth2 form):**
```
username: campaignadmin
password: admin
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:** 401 for invalid credentials.

### GET /auth/users/me

Get current authenticated user information.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "username": "campaignadmin",
  "email": "admin@example.com",
  "full_name": "Campaign Administrator",
  "disabled": false,
  "role": "admin"
}
```

## GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

## Campaigns

### POST /campaigns

Create a new campaign. **Admin authentication required.**

**Authentication:** Required (Admin)

**Request Body:**
```json
{
  "name": "Purchase Over $50",
  "rules": {
    "and": [
      {"field": "event_type", "operator": "equals", "value": "purchase"},
      {"field": "amount", "operator": "greater_than", "value": 50}
    ]
  }
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Welcome Discount",
  "rules": {
    "event_type": "signup"
  },
  "created_at": "2025-11-15T08:00:00"
}
```

**Errors:** 422 for invalid data.

### GET /campaigns

List all campaigns.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Welcome Discount",
    "rules": {
      "event_type": "signup"
    },
    "created_at": "2025-11-15T08:00:00"
  }
]
```

### GET /campaigns/{id}

Get a specific campaign by ID.

**Parameters:**
- `id` (path): Campaign ID

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Welcome Discount",
  "rules": {
    "event_type": "signup"
  },
  "created_at": "2025-11-15T08:00:00"
}
```

**Errors:** 404 if campaign not found.

## Events

### POST /events

Send an event for processing.

**Request Body:**
```json
{
  "event_id": "abc-123",
  "payload": {
    "event_type": "signup",
    "user_id": 42
  }
}
```

**Response (200 OK):**
```json
{
  "id": 0,
  "event_id": "abc-123",
  "payload": {
    "event_type": "signup",
    "user_id": 42
  },
  "campaign_triggers": null,
  "processed_at": null
}
```

**Errors:** 422 for invalid data.

### GET /events

List all events (stub, returns empty list).

**Response (200 OK):**
```json
[]
```

## Monitoring

### GET /metrics

Prometheus metrics endpoint for monitoring.

**Response (200 OK):**
```
# HELP campaign_api_events_received_total Total number of events received via API
# TYPE campaign_api_events_received_total counter
campaign_api_events_received_total 42
...
```

## Campaign Rule Examples

Campaign rules support complex logical operations:

### Simple Rule
```json
{"field": "event_type", "operator": "equals", "value": "purchase"}
```

### Logical AND
```json
{
  "and": [
    {"field": "event_type", "operator": "equals", "value": "purchase"},
    {"field": "amount", "operator": "greater_than", "value": 50}
  ]
}
```

### Logical OR with Nested Field
```json
{
  "or": [
    {"field": "user.loyalty_tier", "operator": "equals", "value": "gold"},
    {"field": "amount", "operator": "greater_than", "value": 100}
  ]
}
```

### Complex Rule with NOT
```json
{
  "and": [
    {"field": "event_type", "operator": "equals", "value": "signup"},
    {"not": {"field": "user.country", "operator": "equals", "value": "blocked"}}
  ]
}
```

### Range Check
```json
{"field": "user.age", "operator": "between", "value": [18, 65]}
```

## Swagger Documentation

Visit `/docs` for interactive API documentation.
