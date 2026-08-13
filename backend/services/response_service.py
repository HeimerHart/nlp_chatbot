import re

from datas.mock_data import simulated_order_status, simulated_refund_timeline
from models.intent import INTENT_LABELS, Intent
from services import llm_service
from services.tone import Tone

_ORDER_ID_PATTERN = re.compile(r"\b([A-Za-z]{2,6}-?\d{3,8})\b")


def _extract_order_id(message: str) -> str | None:
    match = _ORDER_ID_PATTERN.search(message)
    return match.group(1) if match else None


_TONE_PREFIXES = {
    Tone.URGENT: "",
    Tone.REASSURING: "Take a breath, I've got you. ",
    Tone.UPBEAT: "",
}


def _apply_tone(reply: str, tone: Tone | None) -> str:
    if tone is None:
        return reply
    prefix = _TONE_PREFIXES.get(tone, "")
    return f"{prefix}{reply}" if prefix else reply


def llm_prompt_for(intent: Intent, message: str) -> str:
    base = (
        "You are a warm, competent customer-support agent for a food "
        "delivery app. This is a prototype with no live backend, so you "
        "never claim to check a real system. Be concise, concrete, and "
        "always move the user toward a next step. Never say things like "
        "'I don't understand' or 'invalid request' — if unsure, offer the "
        "closest relevant options instead."
    )
    intent_hints = {
        Intent.ORDER_TRACKING: "The user wants to know where their order is. Ask for order ID / merchant / approx time if not given, and reassure them.",
        Intent.REFUND: "The user wants a refund or cancellation. Explain the (simulated) refund flow and timeline.",
        Intent.PAYMENT_ISSUE: "The user had a failed or incorrect payment. Reassure them money isn't lost and outline what typically happens next.",
        Intent.ORDER_ISSUE: "The user got a wrong, missing, or damaged item. Apologize briefly and offer resolution paths (replacement/refund).",
        Intent.DELIVERY_PARTNER: "The user has an issue related to the delivery rider/driver. Handle with extra care and empathy.",
        Intent.ACCOUNT_SUPPORT: "The user needs help with login, password, or account/profile details.",
        Intent.HUMAN_AGENT: "The user explicitly wants to talk to a human. Acknowledge and describe how they'd be connected to one.",
        Intent.SMALLTALK: "The user is bantering, joking, or chit-chatting rather than raising an issue. Respond lightly and briefly, then offer help.",
        Intent.GREETING: "Greet the user and summarize what you can help with.",
        Intent.UNKNOWN: "The intent is unclear. Do not guess wildly — offer the closest matching categories as options.",
    }
    return f"{base}\n\nIntent: {intent.value}\nGuidance: {intent_hints[intent]}\nUser message: {message!r}"


def build_response(
    intent: Intent,
    message: str,
    candidates: list[Intent] | None = None,
    tone: Tone | None = None,
) -> dict:
    result = _build_deterministic_response(intent, message, candidates, tone)

    if llm_service.is_available():
        natural = llm_service.generate_reply(
            llm_prompt_for(intent, message), result["reply"], message
        )
        if natural:
            result["reply"] = natural

    return result


def _build_deterministic_response(
    intent: Intent,
    message: str,
    candidates: list[Intent] | None = None,
    tone: Tone | None = None,
) -> dict:
    order_id = _extract_order_id(message)

    if intent == Intent.GREETING:
        return {
            "reply": "Hi! How can I help today?",
            "quick_replies": [
                "Track my order",
                "Request a refund",
                "Payment issue",
                "Wrong or missing item",
                "Delivery partner issue",
            ],
            "card": None,
        }

    if intent == Intent.ORDER_TRACKING:
        card = simulated_order_status(order_id)
        reply = (
            "I can help you locate it. Here's the latest status on your order:"
        )
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Order still preparing",
                "Rider delayed",
                "Marked delivered but not received",
                "Something else",
            ],
            "card": card,
        }

    if intent == Intent.REFUND:
        card = simulated_refund_timeline(order_id)
        reply = (
            "I'm sorry about that — let's get your refund moving.\n\n"
            "Here's what the refund flow looks like:"
        )
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Why is my refund delayed?",
                "Cancel order instead",
                "Talk to a human",
            ],
            "card": card,
        }

    if intent == Intent.PAYMENT_ISSUE:
        reply = (
            "Sorry your payment didn't go through cleanly — that's stressful, "
            "but in almost all cases any deducted amount is auto-reversed by "
            "your bank within a few business days if the order wasn't placed.\n\n"
            "To help narrow this down:\n"
            "• Was the amount deducted from your account?\n"
            "• Which payment method — UPI, card, or wallet?\n"
            "• Did you get an order confirmation despite the error?"
        )
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Amount was deducted",
                "No confirmation received",
                "Charged twice",
            ],
            "card": None,
        }

    if intent == Intent.ORDER_ISSUE:
        reply = "I'm sorry to hear the order wasn't right. Let's fix it.\n\nIs the issue:"
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Wrong item received",
                "Item missing",
                "Item damaged / spilled",
                "Order incomplete",
            ],
            "card": None,
        }

    if intent == Intent.DELIVERY_PARTNER:
        reply = (
            "Thanks for flagging this — issues with a delivery partner are "
            "taken seriously. Could you tell me a bit more?"
        )
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Rider was late",
                "Rider was rude",
                "Rider couldn't find address",
                "Safety concern",
            ],
            "card": None,
        }

    if intent == Intent.ACCOUNT_SUPPORT:
        reply = "Happy to help with your account. What do you need?"
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Reset password",
                "Update phone/email",
                "Login issue",
                "Delete account",
            ],
            "card": None,
        }

    if intent == Intent.HUMAN_AGENT:
        reply = (
            "Got it — connecting you with a human agent.\n\n"
            "You'll be handed off with your full conversation history attached "
            "so you don't have to repeat yourself."
        )
        return {
            "reply": _apply_tone(reply, tone),
            "quick_replies": [
                "Refund",
                "Payment issue",
                "Order tracking",
            ],
            "card": None,
        }

    if intent == Intent.SMALLTALK:
        return {
            "reply": "Ha, I'll take that! Anything I can actually help you sort out today?",
            "quick_replies": [
                "Track my order",
                "Request a refund",
                "Talk to a human",
            ],
            "card": None,
        }

    if candidates:
        labels = [INTENT_LABELS[c] for c in candidates if c in INTENT_LABELS]
    else:
        labels = list(INTENT_LABELS.values())

    reply = "I'm not completely sure which issue you're referring to.\n\nIs it related to:"
    return {
        "reply": _apply_tone(reply, tone),
        "quick_replies": labels[:4] if labels else ["Order tracking", "Refund", "Payment", "Wrong item"],
        "card": None,
    }
