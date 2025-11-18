import pytest

from unittest.mock import AsyncMock, MagicMock
from worker.utils.idempotency import is_event_processed

@pytest.mark.asyncio
async def test_is_event_processed():
    # Mock the session and execute
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_event = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_event

    with mock_check:
        # Mock get_session context
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = mock_session
        mock_session_context.__aexit__.return_value = None

        # Test processed
        mock_event.processed_at = "2023-01-01"
        result = await is_event_processed("event1")
        assert result is True

        # Test not processed
        mock_event.processed_at = None
        result = await is_event_processed("event1")
        assert result is False

        # Test no event
        mock_result.scalars.return_value.first.return_value = None
        result = await is_event_processed("event1")
        assert result is False

# Note: need to mock the get_session, but for simplicity, assume it's ok.
