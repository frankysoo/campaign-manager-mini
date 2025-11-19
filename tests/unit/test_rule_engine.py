import pytest
from common.rule_engine import (
    evaluate_condition,
    evaluate_rule,
    match_campaigns_enhanced,
    get_nested_value
)

def test_evaluate_condition_equals():
    payload = {"event_type": "purchase", "user_id": 123}
    assert evaluate_condition(payload, "event_type", "equals", "purchase") == True
    assert evaluate_condition(payload, "event_type", "equals", "signup") == False

def test_evaluate_condition_greater_than():
    payload = {"amount": 150}
    assert evaluate_condition(payload, "amount", "greater_than", 100) == True
    assert evaluate_condition(payload, "amount", "greater_than", 200) == False

def test_evaluate_condition_contains():
    payload = {"email": "user@example.com"}
    assert evaluate_condition(payload, "email", "contains", "example") == True
    assert evaluate_condition(payload, "email", "contains", "test") == False

def test_evaluate_condition_in():
    payload = {"category": "electronics"}
    assert evaluate_condition(payload, "category", "in", ["electronics", "books"]) == True
    assert evaluate_condition(payload, "category", "in", ["books", "music"]) == False

def test_evaluate_condition_between():
    payload = {"age": 25}
    assert evaluate_condition(payload, "age", "between", [18, 65]) == True
    assert evaluate_condition(payload, "age", "between", [30, 40]) == False

def test_get_nested_value():
    data = {"user": {"age": 25, "profile": {"city": "NYC"}}}
    assert get_nested_value(data, "user.age") == 25
    assert get_nested_value(data, "user.profile.city") == "NYC"
    assert get_nested_value(data, "user.notexist") is None

def test_evaluate_rule_single_condition():
    payload = {"event_type": "purchase"}
    rule = {"field": "event_type", "operator": "equals", "value": "purchase"}
    assert evaluate_rule(payload, rule) == True

def test_evaluate_rule_and():
    payload = {"event_type": "signup", "amount": 100}
    rule = {
        "and": [
            {"field": "event_type", "operator": "equals", "value": "signup"},
            {"field": "amount", "operator": "greater_than", "value": 50}
        ]
    }
    assert evaluate_rule(payload, rule) == True

def test_evaluate_rule_or():
    payload = {"event_type": "login", "amount": 200}
    rule = {
        "or": [
            {"field": "event_type", "operator": "equals", "value": "purchase"},
            {"field": "amount", "operator": "greater_than", "value": 150}
        ]
    }
    assert evaluate_rule(payload, rule) == True

def test_evaluate_rule_not():
    payload = {"event_type": "purchase"}
    rule = {
        "not": {"field": "event_type", "operator": "equals", "value": "signup"}
    }
    assert evaluate_rule(payload, rule) == True

def test_match_campaigns_enhanced():
    campaigns = [
        type('Campaign', (object,), {'id': 1, 'rules': {"field": "event_type", "operator": "equals", "value": "purchase"}})(),
        type('Campaign', (object,), {'id': 2, 'rules': {"field": "amount", "operator": "greater_than", "value": 100}})(),
        type('Campaign', (object,), {'id': 3, 'rules': {"field": "event_type", "operator": "equals", "value": "purchase"}})(),
    ]

    payload = {"event_type": "purchase", "amount": 150}
    matched = match_campaigns_enhanced(payload, campaigns)
    assert set(matched) == {1, 2, 3}  # All campaigns should match

    payload = {"event_type": "signup", "amount": 50}
    matched = match_campaigns_enhanced(payload, campaigns)
    assert matched == []  # No campaigns match
