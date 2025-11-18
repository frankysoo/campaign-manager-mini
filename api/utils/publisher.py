import asyncio
import json
import os

from redis import asyncio as redis

from common.constants import EVENTS_QUEUE
from api.utils.logger import get_logger

logger = get_logger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.from_url(REDIS_URL)

async def publish_event(event: dict):
    logger.info(f"Publishing event: {event}")
    await redis_client.publish(EVENTS_QUEUE, json.dumps(event))
