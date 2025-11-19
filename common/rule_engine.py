import operator
from typing import Any, Dict, Union
from common.constants import RULE_OPERATORS, LOGICAL_OPERATORS

def evaluate_condition(payload: Dict[str, Any], field: str, operator: str, value: Union[str, int, float, list]) -> bool:
    """
    Evaluate a single condition against the event payload.

    Args:
        payload: Event payload dictionary
        field: Field name to check (e.g., 'event_type', 'user.age')
        operator: Comparison operator
        value: Value to compare against

    Returns:
        Boolean result of the condition
    """
    if operator not in RULE_OPERATORS:
        raise ValueError(f"Unsupported operator: {operator}")

    # Support nested fields (dot notation)
    field_value = get_nested_value(payload, field)
    if field_value is None:
        return False

    # Convert value to match field_value type if possible
    expected_type = type(field_value)
    if not isinstance(value, type(field_value)) and expected_type in [int, float]:
        try:
            value = expected_type(value)
        except (ValueError, TypeError):
            pass  # Keep as is

    # Apply the operator
    if operator == "equals":
        return field_value == value
    elif operator == "greater_than":
        return field_value > value
    elif operator == "less_than":
        return field_value < value
    elif operator == "contains":
        return str(value).lower() in str(field_value).lower()
    elif operator == "in":
        return field_value in value
    elif operator == "between":
        if isinstance(value, list) and len(value) >= 2:
            return value[0] <= field_value <= value[1]
        return False
    else:
        return False

def evaluate_rule(payload: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """
    Evaluate a complete rule which may include logical operators.

    Args:
        payload: Event payload
        rule: Rule dictionary structure

    Returns:
        Boolean result of the rule
    """
    if "and" in rule:
        return all(evaluate_rule(payload, subrule) for subrule in rule["and"])

    if "or" in rule:
        return any(evaluate_rule(payload, subrule) for subrule in rule["or"])

    if "not" in rule:
        return not evaluate_rule(payload, rule["not"])

    # Single condition rule
    if all(key in rule for key in ["field", "operator", "value"]):
        return evaluate_condition(payload, rule["field"], rule["operator"], rule["value"])

    return False

def match_campaigns_enhanced(payload: Dict[str, Any], campaigns) -> list[int]:
    """
    Enhanced campaign matching with complex rule evaluation.

    Args:
        payload: Event payload
        campaigns: List of campaign objects with rules

    Returns:
        List of matching campaign IDs
    """
    matches = []
    for campaign in campaigns:
        try:
            if evaluate_rule(payload, campaign.rules):
                matches.append(campaign.id)
        except Exception as e:
            # Log error but don't fail processing
            print(f"Error evaluating campaign {campaign.id}: {e}")
            continue
    return matches

def get_nested_value(d: Dict[str, Any], key: str) -> Any:
    """
    Get value from nested dictionary using dot notation.

    Args:
        d: Dictionary to extract from
        key: Dot-separated key path

    Returns:
        Value at key path or None if not found
    """
    keys = key.split('.')
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d
