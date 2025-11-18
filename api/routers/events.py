from fastapi import APIRouter, HTTPException

from api.utils.publisher import publish_event
from api.schemas.event import EventCreate, EventOut
from common.utils import validate_event_payload

router = APIRouter()

@router.post("/", response_model=EventOut)
async def receive_event(event: EventCreate) -> EventOut:
    # Validate payload before publishing
    if not validate_event_payload(event.payload):
        raise HTTPException(status_code=422, detail="Invalid event payload")

    # Publish to queue
    await publish_event(event.dict())

    # Return the event, but not saving to DB yet
    return EventOut(
        id=0,  # Not saved
        event_id=event.event_id,
        payload=event.payload,
        campaign_triggers=None,
        processed_at=None
    )

@router.get("/")
async def list_events():
    # Stub
    return []
