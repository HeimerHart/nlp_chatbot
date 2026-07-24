from utils.logger import logger
from database.mongodb import db
from services.intentclassifier import predict_intent
from services.preprocessor import NLPPreprocessor
from services.faq import get_faq_response
from services.ner_service import extract_entities
from services.validator import sanitize



processor = NLPPreprocessor()

intent_collection = db["intents"]

conversation_collection = db["conversations"]


async def process_chat(
    session_id: str,
    message: str,
    context: list = []
):
    message = sanitize(message)
    logger.info(f'User message: {message}')

    entities = extract_entities(message)
    logger.info(f"Entities: {entities}")

    logger.info(f'Context: {context}')

    faq_response = get_faq_response(message)

    if faq_response:

        conversation_collection.insert_one(
            {
                "session_id": session_id,
                "user_id": "user123",
                "user_message": message,
                "intent": faq_response["intent"],
                "bot_response": faq_response["response"]
            }
        )

        return {
            "session_id": session_id,
            "intent": faq_response["intent"],
            "response": faq_response["response"]
        }

    processed_tokens = processor.preprocess(message)

    processed_text = " ".join(processed_tokens)

    intent_name = predict_intent(processed_text)

    intent = intent_collection.find_one(
        {
            "name": intent_name
        }
    )

    if intent:
        response = intent["responses"][0]
        conversation_collection.insert_one(
            {
                "session_id": session_id,
                "user_id": "user123",
                "user_message": message,
                "intent": intent_name,
                "bot_response": response
            }
        )



        if "ORDER_ID" in entities:
            response = f"Your order #{entities['ORDER_ID']} is currently being processed."

        elif "DATE" in entities:
                    response = f"You mentioned the date {entities['DATE']}."

        elif "GPE" in entities:
            response = f"I found the location {entities['GPE']}."

        elif "PRODUCT" in entities:
            response = f"You are asking about {entities['PRODUCT']}."



        return {
            "session_id": session_id,
            "intent": intent_name,
            "response": response
            }

    return {
            "session_id": session_id,
            "intent": "unknown",
            "response": "I do not understand"
        }