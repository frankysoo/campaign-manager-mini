import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from worker.utils.idempotency import is_event_processed

@pytest.mark.asyncio
@patch('worker.utils.idempotency.get_session')
async def test_is_event_processed(mock_get_session):
    # Mock the session and execute
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_event = MagicMock()

    mock_get_session.return_value.__aenter__.return_value = mock_session
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_scalars.first.return_value = mock_event

    # Test processed
    mock_event.processed_at = "2023-01-01"
    result = await is_event_processed("event1")
    assert result is True

    # Test not processed
    mock_event.processed_at = None
    result = await is_event_processed("event1")
    assert result is False

    # Test no event
    mock_scalars.first.return_value = None
    result = await is_event_processed("event1")
    assert result is False
