from typing import Dict, Any
from apps.shared.messages import MESSAGES

def get_message_detail(message_key: str, lang: str = 'en', context: Dict[str, Any] = None) -> Dict[str, Any]:
    message_template = MESSAGES.get(message_key)
    
    if not message_template:
        return {
            "id": "UNKNOWN_ERROR",
            "message": "Unknown error occurred",
            "status_code": 500
        }
    
    message = message_template["messages"].get(lang, message_template["messages"]["en"])

    if context:
        try:
            message = message.format(**context)
        except (KeyError, ValueError):
            pass
    
    return {
        "id": message_template["id"],
        "message": message,
        "status_code": message_template["status_code"]
    }