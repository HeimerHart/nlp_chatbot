from rapidfuzz import fuzz
from database.mongodb import db

faq_collection = db["faq"]

MATCH_THRESHOLD = 78


def get_faq_response(message):
    message = message.lower().strip()

    best_score = 0
    best_faq = None

    for faq in faq_collection.find():
        for pattern in faq.get("patterns", []):
            pattern = pattern.lower()

            if message == pattern:
                return {"intent": faq["intent"], "response": faq["response"]}

            score = fuzz.token_set_ratio(message, pattern)
            if score > best_score:
                best_score = score
                best_faq = faq

    if best_faq and best_score >= MATCH_THRESHOLD:
        return {"intent": best_faq["intent"], "response": best_faq["response"]}

    return None
