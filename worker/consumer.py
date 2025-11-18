import asyncio
import json
import os

from redis.asyncio import from_url

from common.constants import EVENTS_QUEUE
from worker.processor import process_event
from worker.utils.logger import get_logger

logger = get_logger(__name__)

async def consume_events():
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
    redis_conn = from_url(REDIS_URL)

    pubsub = redis_conn.pubsub()
    await pubsub.subscribe(EVENTS_QUEUE)

    logger.info(f"Worker consumer started, listening to '{EVENTS_QUEUE}' channel...")

    try:
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    try:
                        data = json.loads(message['data'].decode('utf-8'))
                        await process_event(data)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        # Continue processing other messages even if one fails
            except asyncio.TimeoutError:
                # Redis connection timeout - continue loop
                continue
            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
                # Brief pause before retrying
                await asyncio.sleep(1)

            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        logger.info("Worker consumer stopped.")
        await pubsub.unsubscribe(EVENTS_QUEUE)
        raise
    except Exception as e:
        logger.error(f"Consumer loop crashed: {e}")
        raise
