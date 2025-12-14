import logging
from typing import Dict
from .shared import SHARED_MESSAGES
from .movies import MOVIE_MESSAGES
from .users import USER_MESSAGES
from .types import MessageTemplate

logger = logging.getLogger(__name__)

MESSAGES: Dict[str, MessageTemplate] = {
    **SHARED_MESSAGES,
    **MOVIE_MESSAGES,
    **USER_MESSAGES,
}

def _validate_messages():
    all_keys = []
    message_sources = [
        ("SHARED_MESSAGES", SHARED_MESSAGES),
        ("MOVIE_MESSAGES", MOVIE_MESSAGES),
        ("USER_MESSAGES", USER_MESSAGES),
    ]
    duplicates = []
    for source_name, messages in message_sources:
        for key in messages.keys():
            if key in all_keys:
                duplicates.append(f"{key} (found in {source_name})")
            all_keys.append(key)
    if duplicates:
        logger.error(f"Duplicate message keys found: {', '.join(duplicates)}")

_validate_messages()

__all__ = [
    'MESSAGES',
    'MessageTemplate',
    'SHARED_MESSAGES',
    'MOVIE_MESSAGES',
    'USER_MESSAGES',
]