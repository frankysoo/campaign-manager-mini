from pydantic import BaseModel


class EventCreate(BaseModel):
    event_id: str
    payload: dict


class EventOut(BaseModel):
    id: int
    event_id: str
    payload: dict
    campaign_triggers: dict | None = None
    processed_at: str | None = None
