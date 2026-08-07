from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

print(f"MongoDB connected to database '{DATABASE_NAME}'")

db["users"].create_index(
    "email",
    unique=True
)

db["conversations"].create_index(
    "session_id"
)

db["conversations"].create_index(
    "user_id"
)

db["analytics"].create_index(
    "date"
)
