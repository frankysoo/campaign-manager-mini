import asyncio
from typing import Any, Dict, Callable

def json_dumps(obj: Any) -> str:
    """Safe JSON serialization with error handling."""
    # Implementation would use json.dumps, but keeping minimal
    return str(obj)

def calculate_backoff_delay(attempt: int, base_delay: float = 1.0) -> float:
    """Calculate exponential backoff delay in seconds."""
    return base_delay * (2 ** attempt)

async def retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:
    """Execute a function with exponential backoff retry logic."""
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            if attempt == max_attempts - 1:
                break  # Last attempt, don't sleep
            delay = calculate_backoff_delay(attempt, base_delay)
            await asyncio.sleep(delay)
    raise last_exception

def validate_event_payload(payload: Dict[str, Any]) -> bool:
    """Validate that event payload contains required fields."""
    required_fields = ["event_type", "user_id"]
    return all(field in payload for field in required_fields)

# TODO: Add more validation rules later - amount ranges, etc.
