from utils.logger import logger
from database.mongodb import db


intent_collection = db["intents"]
async def process_chat(message: str):

    logger.info(f'User message: {message}')

    message=message.lower()
    
    #search matching intent
    
    intent=intent_collection.find_one({
        "patterns":{
            "$in":[message]
        }


    })

    #if intent is found
    if intent:
        response=intent["responses"][0]

        return{
            "intent":intent["name"],
            "response":response
        }





    return {
        "intent":"unknown",
        'response': "i do not understant"
    }