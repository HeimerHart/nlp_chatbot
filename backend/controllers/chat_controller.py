import re
from typing import Optional
from datetime import datetime, timezone

from utils.logger import logger
from database.mongodb import db
from services.faq import get_faq_response
from services.validator import sanitize
from services.cache import conversation_cache
from services.intent_classifier import classify
from services.response_service import build_response
from services.tone import detect_tone
from models.intent import Intent

conversation_collection = db["conversations"]

_BYE_PATTERN = re.compile(r"^(bye|goodbye|see ya|see you|take care)\b")
_THANKS_PATTERN = re.compile(r"^(thanks|thank you|thankyou|ty)\b")


def _bye_thanks_patch(normalized: str) -> Optional[dict]:
    if _BYE_PATTERN.match(normalized):
        return {
            "reply": "Bye! Reach out anytime you need help.",
            "intent": "bye",
            "quick_replies": [],
            "card": None,
        }
    if _THANKS_PATTERN.match(normalized):
        return {
            "reply": "You're welcome! Anything else I can help with?",
            "intent": "thankyou",
            "quick_replies": [
                "Track my order",
                "Request a refund",
                "Talk to a human",
            ],
            "card": None,
        }
    return None


def _log_and_invalidate(session_id: str, user_id: str, message: str, intent: str,
                         response: str, timestamp, conversation_id: str,
                         quick_replies: list, card: Optional[dict]) -> None:
    conversation_collection.insert_one({
        "session_id": session_id,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "user_message": message,
        "intent": intent,
        "bot_response": response,
        "quick_replies": quick_replies,
        "card": card,
        "timestamp": timestamp
    })
    conversation_cache.pop(session_id, None)
    conversation_cache.pop(f"{session_id}:{conversation_id}", None)


async def process_chat(
    session_id: str,
    message: str,
    context: Optional[list] = None,
    conversation_id: Optional[str] = None,
):
    context = context or []
    conversation_id = conversation_id or "default"

    message = sanitize(message)
    logger.info(f'User message: {message}')
    logger.info(f'Context: {context}')

    user_id = session_id
    timestamp = datetime.now(timezone.utc)

    faq_response = get_faq_response(message)
    if faq_response:
        response = faq_response["response"]
        _log_and_invalidate(
            session_id, user_id, message, faq_response["intent"], response,
            timestamp, conversation_id, [], None,
        )
        return {
            "session_id": session_id,
            "conversation_id": conversation_id,
            "intent": faq_response["intent"],
            "response": response,
            "quick_replies": [],
            "card": None,
        }

    normalized = message.lower().strip()
    patched = _bye_thanks_patch(normalized)
    if patched:
        _log_and_invalidate(
            session_id, user_id, message, patched["intent"], patched["reply"],
            timestamp, conversation_id, patched["quick_replies"], patched["card"],
        )
        return {
            "session_id": session_id,
            "conversation_id": conversation_id,
            "intent": patched["intent"],
            "response": patched["reply"],
            "quick_replies": patched["quick_replies"],
            "card": patched["card"],
        }

    result = classify(message)
    tone = detect_tone(message)
    built = build_response(result.intent, message, result.candidates, tone)

    intent_name = result.intent.value if isinstance(result.intent, Intent) else str(result.intent)

    _log_and_invalidate(
        session_id, user_id, message, intent_name, built["reply"],
        timestamp, conversation_id, built["quick_replies"], built["card"],
    )

    return {
        "session_id": session_id,
        "conversation_id": conversation_id,
        "intent": intent_name,
        "response": built["reply"],
        "quick_replies": built["quick_replies"],
        "card": built["card"],
    }
