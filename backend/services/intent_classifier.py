import re
from dataclasses import dataclass, field

from ml.predictor import predict_intent
from models.intent import DATASET_LABEL_TO_INTENT, Intent
from utils.text_utils import normalize, significant_tokens

_INTENT_RULES: dict[Intent, dict] = {
    Intent.GREETING: {
        "regex": [
            r"^(hi|hello|hey|hola|yo|good (morning|afternoon|evening))\b",
        ],
        "keywords": {"hi", "hello", "hey", "greetings"},
        "weight": 1,
    },
    Intent.ORDER_TRACKING: {
        "regex": [
            r"can'?t find (my )?order",
            r"where('?s| is) my (order|food|package|delivery)",
            r"order (has(n'?t| not))? ?arriv",
            r"order (disappear|missing|lost)",
            r"track(ing)? (my )?(order|food)",
            r"delivery is late",
            r"food (never|hasn'?t) (came|arrived)",
        ],
        "keywords": {
            "track", "tracking", "order", "eta", "arrive", "arrived",
            "arriving", "late", "delayed", "delay", "package",
        },
        "weight": 1,
    },
    Intent.REFUND: {
        "regex": [
            r"\brefund\b",
            r"money ?back",
            r"cancel(led)? (my )?order",
            r"want (a )?refund",
            r"charge(d)? but (no|didn'?t)",
        ],
        "keywords": {"refund", "reimburse", "cancel", "chargeback"},
        "weight": 2,
    },
    Intent.PAYMENT_ISSUE: {
        "regex": [
            r"payment fail",
            r"upi fail",
            r"card declin",
            r"transaction fail",
            r"double charg",
            r"charged twice",
            r"money (was )?deduct",
        ],
        "keywords": {
            "payment", "upi", "card", "declined", "failed", "transaction",
            "deducted", "otp", "gateway",
        },
        "weight": 2,
    },
    Intent.ORDER_ISSUE: {
        "regex": [
            r"wrong item",
            r"missing item",
            r"received something else",
            r"item(s)? (is |are )?missing",
            r"(order|food) (is |was )?(damaged|spilled|cold|incomplete)",
        ],
        "keywords": {
            "wrong", "missing", "damaged", "spilled", "incomplete",
            "item", "items",
        },
        "weight": 1,
    },
    Intent.DELIVERY_PARTNER: {
        "regex": [
            r"delivery (boy|partner|guy)",
            r"\brider\b",
            r"\bdriver\b",
            r"(rude|misbehav).*(rider|driver|delivery)",
        ],
        "keywords": {"rider", "driver", "delivery", "partner"},
        "weight": 1,
    },
    Intent.ACCOUNT_SUPPORT: {
        "regex": [
            r"(log ?in|sign ?in) (issue|problem|fail)",
            r"reset (my )?password",
            r"(update|change) (my )?(account|profile|email|phone|address)",
            r"delete (my )?account",
        ],
        "keywords": {"account", "login", "password", "profile", "signup"},
        "weight": 1,
    },
    Intent.HUMAN_AGENT: {
        "regex": [
            r"(talk|speak|connect) (to|with) (a )?(human|agent|person|representative)",
            r"\bescalat",
            r"human please",
            r"real person",
        ],
        "keywords": {"agent", "human", "representative", "escalate"},
        "weight": 1,
    },
    Intent.SMALLTALK: {
        "regex": [
            r"how are you",
            r"tell me a joke",
            r"good bot",
            r"what'?s up",
        ],
        "keywords": {"joke", "bot", "thanks", "lol"},
        "weight": 1,
    },
}

_REGEX_ONLY_INTENTS = (Intent.ORDER_ISSUE, Intent.DELIVERY_PARTNER)

_CONFIDENCE_THRESHOLD = 1

_ML_CONFIDENCE_THRESHOLD = 0.55


@dataclass
class ClassificationResult:
    intent: Intent
    confidence: float
    candidates: list[Intent] = field(default_factory=list)
    source: str = "regex"


def _regex_score(normalized: str, tokens: set[str], intents=None) -> dict[Intent, float]:
    scores: dict[Intent, float] = {}
    rules_iter = _INTENT_RULES.items() if intents is None else (
        (i, _INTENT_RULES[i]) for i in intents
    )
    for intent, rules in rules_iter:
        score = 0.0
        for pattern in rules.get("regex", []):
            if re.search(pattern, normalized):
                score += 2 * rules["weight"]
        overlap = tokens & rules.get("keywords", set())
        score += len(overlap) * rules["weight"]
        if score > 0:
            scores[intent] = score
    return scores


def _phrase_only_score(normalized: str, intents) -> dict[Intent, float]:
    scores: dict[Intent, float] = {}
    for intent in intents:
        rules = _INTENT_RULES[intent]
        score = 0.0
        for pattern in rules.get("regex", []):
            if re.search(pattern, normalized):
                score += 2 * rules["weight"]
        if score > 0:
            scores[intent] = score
    return scores


def _regex_classify(normalized: str, tokens: set[str]) -> ClassificationResult:
    scores = _regex_score(normalized, tokens)
    if not scores:
        return ClassificationResult(Intent.UNKNOWN, 0.0, [], source="regex")

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_intent, top_score = ranked[0]

    if top_score < _CONFIDENCE_THRESHOLD:
        candidates = [intent for intent, _ in ranked[:3]]
        return ClassificationResult(Intent.UNKNOWN, top_score, candidates, source="regex")

    if len(ranked) > 1:
        second_intent, second_score = ranked[1]
        if second_score > 0 and top_score - second_score <= 0.5 and top_intent != Intent.GREETING:
            candidates = [intent for intent, _ in ranked[:3]]
            return ClassificationResult(Intent.UNKNOWN, top_score, candidates, source="regex")

    return ClassificationResult(top_intent, top_score, [], source="regex")


def classify(message: str) -> ClassificationResult:
    normalized = normalize(message)
    tokens = significant_tokens(message)

    if not normalized:
        return ClassificationResult(Intent.UNKNOWN, 0.0, [], source="regex")

    regex_only_scores = _phrase_only_score(normalized, _REGEX_ONLY_INTENTS)
    if regex_only_scores:
        top_intent, top_score = max(regex_only_scores.items(), key=lambda kv: kv[1])
        if top_score >= _CONFIDENCE_THRESHOLD:
            return ClassificationResult(top_intent, top_score, [], source="regex")

    proba = predict_intent(message)
    ranked_ml: list[tuple[str, float]] = []
    if proba:
        ranked_ml = sorted(proba.items(), key=lambda kv: kv[1], reverse=True)
        top_label, top_prob = ranked_ml[0]
        if top_prob >= _ML_CONFIDENCE_THRESHOLD:
            intent = DATASET_LABEL_TO_INTENT.get(top_label)
            if intent is not None:
                return ClassificationResult(intent, top_prob, [], source="ml")

    fallback = _regex_classify(normalized, tokens)
    if fallback.intent != Intent.UNKNOWN:
        return fallback

    if ranked_ml:
        candidates = [
            DATASET_LABEL_TO_INTENT[label]
            for label, _ in ranked_ml[:3]
            if label in DATASET_LABEL_TO_INTENT
        ]
        if candidates:
            return ClassificationResult(Intent.UNKNOWN, ranked_ml[0][1], candidates, source="ml")

    return fallback
