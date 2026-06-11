from utils.logger import logger
from database.mongodb import db
from services.intentclassifier import predict_intent
from services.preprocessor import NLPPreprocessor
from services.intentclassifier import predict_intent


processor = NLPPreprocessor()

intent_collection = db["intents"]

conversation_collection = db["conversations"]


async def process_chat(
    session_id: str,
    message: str
):

    logger.info(f'User message: {message}')





    
    processed_tokens = processor.preprocess(message)

    processed_text = " ".join(processed_tokens)

    intent_name = predict_intent(processed_text)

    intent = intent_collection.find_one(
        {
            "name": intent_name
        }
    )





    #if intent is found
    if intent:
        response = intent["responses"][0]
        conversation_collection.insert_one(
            {
                "session_id": session_id,
                "user_message": message,
                "intent": intent_name,
                "bot_response": response
            }
        )


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