from sqlalchemy import select

from worker.db import get_session
from api.models import Event

async def is_event_processed(event_id: str) -> bool:
    async with get_session() as session:
        result = await session.execute(select(Event).where(Event.event_id == event_id))
        event = result.scalars().first()
        return event is not None and event.processed_at is not None
