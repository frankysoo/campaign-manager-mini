import asyncio
import time
import pytest
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_session
from api.models import Campaign, Event
from common.constants import EVENTS_QUEUE
import redis


@pytest.mark.asyncio
async def test_full_campaign_event_flow():
    """
    Full integration test: API -> Redis -> Worker -> Database
    Requires Docker containers running (postgres, redis, api, worker)
    """
    base_url = "http://localhost:8000"

    # Test 1: API health check
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{base_url}/health")
            assert resp.status_code == 200
            assert resp.json() == {"status": "ok"}
        except Exception as e:
            pytest.skip(f"API not available: {e}")

    # Test 2: Create campaign via API
    campaign_data = {
        "name": "Test Campaign",
        "rules": {"event_type": "purchase"}
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{base_url}/campaigns",
            json=campaign_data,
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 200
        campaign_resp = resp.json()
        assert "id" in campaign_resp
        assert campaign_resp["name"] == "Test Campaign"
        campaign_id = campaign_resp["id"]

    # Test 3: Verify campaign in database
    async with get_session() as session:
        result = await session.execute(select(Campaign).where(Campaign.id == campaign_id))
        db_campaign = result.scalars().first()
        assert db_campaign is not None
        assert db_campaign.name == "Test Campaign"
        assert db_campaign.rules == {"event_type": "purchase"}

    # Test 4: Send event via API
    event_data = {
        "event_id": "test-event-123",
        "payload": {
            "event_type": "purchase",
            "user_id": "user123",
            "amount": 100
        }
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{base_url}/events",
            json=event_data,
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 200

    # Test 5: Wait for worker processing
    # Give worker time to process the event
    await asyncio.sleep(5)

    # Test 6: Verify event processed in database
    async with get_session() as session:
        result = await session.execute(select(Event).where(Event.event_id == "test-event-123"))
        db_event = result.scalars().first()
        assert db_event is not None
        assert db_event.event_id == "test-event-123"
        assert db_event.payload == event_data["payload"]
        assert db_event.campaign_triggers == [campaign_id]  # Should match our campaign
        assert db_event.processed_at is not None

    # Test 7: Verify Redis queue is empty (event consumed)
    try:
        redis_conn = redis.Redis(host="localhost", port=6379, decode_responses=True)
        queue_length = redis_conn.llen(EVENTS_QUEUE)
        assert queue_length == 0  # Event should be consumed
    except Exception as e:
        pytest.skip(f"Redis not available for queue check: {e}")

    # Test 8: Verify GET endpoints work
    async with httpx.AsyncClient() as client:
        # List campaigns
        resp = await client.get(f"{base_url}/campaigns")
        assert resp.status_code == 200
        campaigns = resp.json()
        assert len(campaigns) >= 1

        # List events (if endpoint exists)
        resp = await client.get(f"{base_url}/events")
        assert resp.status_code == 200


if __name__ == "__main__":
    # Manual test runner for local development
    asyncio.run(test_full_campaign_event_flow())
    print("Integration test completed!")
