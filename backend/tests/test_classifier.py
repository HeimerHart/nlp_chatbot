from services.intent_classifier import classify
from models.intent import Intent


def test_classify_returns_a_known_intent():
    result = classify("hello there")
    assert isinstance(result.intent, Intent)


def test_classify_refund_message():
    result = classify("I want a refund for my order")
    assert result.intent == Intent.REFUND
