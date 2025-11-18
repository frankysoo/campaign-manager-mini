import asyncio
import logging

from worker.consumer import consume_events

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        asyncio.run(consume_events())
    except KeyboardInterrupt:
        print("Worker stopping...")
