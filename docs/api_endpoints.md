# API Endpoints

All endpoints are prefixed with the base path (e.g., `http://localhost:8000`).

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

Create a new campaign.

**Request Body:**
```json
{
  "name": "Welcome Discount",
  "rules": {
    "event_type": "signup"
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

## Swagger Documentation

Visit `/docs` for interactive API documentation.
