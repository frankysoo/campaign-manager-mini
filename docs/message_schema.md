# Message Schemas

All requests and responses use JSON.

## Event Schema

Used for POST /events and event processing.

### Event Create Schema
```json
{
  "event_id": "string (unique identifier)",
  "payload": {
    "event_type": "string (e.g., 'purchase', 'signup')",
    "user_id": "integer (optional)",
    "timestamp": "string (optional ISO format)"
  }
}
```

### Example Event
```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "payload": {
    "event_type": "purchase",
    "user_id": 12345,
    "amount": 99.99
  }
}
```

## Campaign Schema

### Campaign Create Schema
```json
{
  "name": "string",
  "rules": {
    "event_type": "string (rule to match event payload)"
  }
}
```

### Example Campaign
```json
{
  "name": "Discount for First Purchase",
  "rules": {
    "event_type": "purchase"
  }
}
```

### Campaign Out Schema
```json
{
  "id": "integer",
  "name": "string",
  "rules": "object",
  "created_at": "string (ISO datetime)"
}
```

## Event Out Schema
```json
{
  "id": "integer",
  "event_id": "string",
  "payload": "object",
  "campaign_triggers": "array of integers or null",
  "processed_at": "string or null"
}
```

## Notes
- Use UUID for event_id to ensure uniqueness.
- Campaign rules are simple; only 'event_type' is checked against payload.event_type.
- Responses include processing results for events.
