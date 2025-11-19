import json
import time

from sqlalchemy import select
from sqlalchemy.sql import func

from api.models import Campaign, Event
from common.constants import DEAD_LETTER_QUEUE
from common.utils import retry_with_backoff
from worker.db import get_session
from worker.utils.idempotency import is_event_processed
from worker.utils.logger import get_logger
from common.rule_engine import match_campaigns_enhanced
from common.metrics import events_processed_total, events_processing_time_seconds, idempotent_event_skips_total, dead_letters_total

logger = get_logger(__name__)

def match_campaigns(payload: dict, campaigns):
    """
    Match campaigns based on rules.
    For demo, rule: if rule['event_type'] == payload['event_type']
    """
    matches = []
    for campaign in campaigns:
        rules = campaign.rules
        if rules.get("event_type") == payload.get("event_type"):
            matches.append(campaign.id)
    return matches

async def process_event_core(event: dict):
    """Core event processing logic with error handling."""
    start_time = time.time()
    event_id = event['event_id']
    payload = event['payload']

    logger.info(f"Processing event {event_id}")

    if await is_event_processed(event_id):
        idempotent_event_skips_total.inc()
        logger.info(f"Event {event_id} already processed, skipping")
        return

    async with get_session() as session:
        # Fetch all campaigns
        result = await session.execute(select(Campaign))
        campaigns = result.scalars().all()

        # Match campaigns using enhanced rule engine
        triggered_ids = match_campaigns_enhanced(payload, campaigns)

        # Save event
        db_event = Event(
            event_id=event_id,
            payload=payload,
            campaign_triggers=triggered_ids,
            processed_at=func.now()
        )

        session.add(db_event)
        await session.commit()

        # Track successful processing
        processing_time = time.time() - start_time
        events_processing_time_seconds.observe(processing_time)
        events_processed_total.labels(status="success").inc()

        logger.info(f"Event {event_id} processed successfully. Triggered campaigns: {triggered_ids}")

async def send_to_dlq(event: dict, error: Exception):
    """Send failed event to dead letter queue for later investigation."""
    dead_letters_total.inc()
    # TODO: Actually send to Redis DLQ channel - for now just log
    logger.error(f"Event {event['event_id']} failed: {error}")

async def process_event(event: dict):
    """Process event with retry logic and DLQ."""
    try:
        await retry_with_backoff(
            lambda: process_event_core(event)
        )
    except Exception as e:
        logger.error(f"Event {event['event_id']} failed after all retries: {e}")
        await send_to_dlq(event, e)
        raise
