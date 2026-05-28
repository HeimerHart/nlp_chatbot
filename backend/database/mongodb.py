from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

# Find backend folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from backend folder
load_dotenv(BASE_DIR / ".env")

# Get variables
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Debug prints
print("MONGODB_URI =", MONGODB_URI)
print("DATABASE_NAME =", DATABASE_NAME)

# MongoDB connection
client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

print("MongoDB Connected Successfully")