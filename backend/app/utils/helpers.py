import json
import datetime
from flask import jsonify

def to_json(obj, status=200):
    """Convert object to JSON response with status code."""
    return jsonify(obj), status

def success_response(data=None, message="Success"):
    """Standard success response."""
    return {
        "success": True,
        "message": message,
        "data": data
    }

def error_response(message, status=400):
    """Standard error response."""
    return {
        "success": False,
        "error": message
    }, status

def validate_required_fields(data, required_fields):
    """Check if all required fields exist in data dict."""
    missing = [field for field in required_fields if field not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, None

def safe_json_loads(string, default=None):
    """Safely parse JSON string."""
    try:
        return json.loads(string)
    except (json.JSONDecodeError, TypeError):
        return default

def get_current_timestamp():
    """Return current UTC timestamp as ISO string."""
    return datetime.datetime.utcnow().isoformat()

def normalize_action_type(action_type):
    """Normalize action type strings to one of the five core types."""
    action_map = {
        "attack": "fight",
        "combat": "fight",
        "battle": "fight",
        "talk": "diplomatic",
        "negotiate": "diplomatic",
        "persuade": "diplomatic",
        "hide": "stealth",
        "sneak": "stealth",
        "evade": "stealth",
        "dare": "risky",
        "gamble": "risky",
        "defend": "cautious",
        "protect": "cautious"
    }
    return action_map.get(action_type.lower(), action_type.lower())