import bcrypt
from database.mongodb import db

intent_collection = db["intents"]
user_collection = db["users"]

sample_intents = [

{
    "name": "greeting",
    "patterns": ["hi", "hello", "hey", "good morning"],
    "responses": ["Hi! How can I help today?"],
},

{
    "name": "order_tracking",
    "patterns": ["where is my order", "track my order", "order status"],
    "responses": ["I can help you locate it."],
},

{
    "name": "refund",
    "patterns": ["refund", "i want a refund", "money back"],
    "responses": ["I'm sorry about that — let's get your refund moving."],
},

{
    "name": "payment_issue",
    "patterns": ["payment failed", "card declined", "charged twice"],
    "responses": ["Sorry your payment didn't go through cleanly."],
},

{
    "name": "order_issue",
    "patterns": ["wrong item", "missing item", "order damaged"],
    "responses": ["I'm sorry to hear the order wasn't right. Let's fix it."],
},

{
    "name": "delivery_partner",
    "patterns": ["rider was rude", "driver couldn't find address"],
    "responses": ["Thanks for flagging this — issues with a delivery partner are taken seriously."],
},

{
    "name": "account_support",
    "patterns": ["reset my password", "login issue", "update my email"],
    "responses": ["Happy to help with your account. What do you need?"],
},

{
    "name": "human_agent",
    "patterns": ["talk to a human", "connect me to an agent", "escalate"],
    "responses": ["Got it — connecting you with a human agent."],
},

{
    "name": "smalltalk",
    "patterns": ["how are you", "tell me a joke", "good bot"],
    "responses": ["Ha, I'll take that! Anything I can actually help you sort out today?"],
},

{
    "name": "bye",
    "patterns": ["bye", "goodbye", "see ya"],
    "responses": ["Bye! Reach out anytime you need help."],
},

{
    "name": "thankyou",
    "patterns": ["thanks", "thank you", "thankyou"],
    "responses": ["You're welcome! Anything else I can help with?"],
},

]

if intent_collection.count_documents({}) == 0:
    intent_collection.insert_many(sample_intents)
    print("Sample intents inserted successfully")
else:
    print("Intents already seeded, skipping")

admin_email = "admin@chatbot.com"
admin_password = "Admin@123"

if not user_collection.find_one({"email": admin_email}):
    hashed_password = bcrypt.hashpw(
        admin_password.encode("utf-8"),
        bcrypt.gensalt()
    )
    user_collection.insert_one({
        "email": admin_email,
        "password": hashed_password.decode("utf-8"),
        "role": "admin"
    })
    print(f"Admin user created -> email: {admin_email} password: {admin_password}")
else:
    print("Admin user already exists, skipping")
