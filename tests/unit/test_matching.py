import pytest

from worker.processor import match_campaigns

def test_match_campaigns():
    campaigns = [
        type('Campaign', (object,), {'id': 1, 'rules': {'event_type': 'purchase'}})(),
        type('Campaign', (object,), {'id': 2, 'rules': {'event_type': 'signup'}})(),
        type('Campaign', (object,), {'id': 3, 'rules': {'event_type': 'purchase'}})(),
    ]

    # Test purchase event
    payload = {'event_type': 'purchase'}
    matched = match_campaigns(payload, campaigns)
    assert matched == [1, 3]

    # Test signup event
    payload = {'event_type': 'signup'}
    matched = match_campaigns(payload, campaigns)
    assert matched == [2]

    # Test non-matching
    payload = {'event_type': 'login'}
    matched = match_campaigns(payload, campaigns)
    assert matched == []

    # Test missing event_type
    payload = {}
    matched = match_campaigns(payload, campaigns)
    assert matched == []
