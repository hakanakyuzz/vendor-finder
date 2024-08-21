import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def connect_to_mongo():
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['vendors']
    try:
        client.admin.command('ping')
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        db = None
    return db
