from database.mongodb import db
intent_collection=db["intents"]

sample_intents=[

{
    "name": "greeting",
    "patterns":["hi","hello","hey"],
    "responses":["hi","hello","hey"],



},


{
    "name": "goodbye",
    "patterns":["bye","goodbye"],
    "responses":["Byee"],



},


{
    "name": "refund",
    "patterns":["refund","i want refund","refund me"],
    "responses":["Please provide order id"],



},

{
    "name": "order_status",
    "patterns":["order status","where is my order"],
    "responses":["please provide order id"],



},





]

intent_collection.insert_many(sample_intents)

print("Sample intents inserted successfully")
