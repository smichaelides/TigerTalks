from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_CONN"))
db = client["tiger-talks"]

try:
    db.command("ping")
    print("MongoDB Atlas connection successful!")
except Exception as e:
    print(f"MongoDB Atlas connection failed: {e}")