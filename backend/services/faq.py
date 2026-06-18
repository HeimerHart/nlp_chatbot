from database.mongodb import db

faq_collection = db["faq"]


def get_faq_response(message):
    message = message.lower()
    faq = faq_collection.find()
    for faq in faq:
        patterns = [
            pattern.lower()
            for pattern in faq["patterns"]
        ]

        if message in patterns:
            return {
                "intent": faq["intent"],
                "response": faq["response"]
            }

    return None