import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError("MONGODB_URI not found in .env file")
        _client = MongoClient(
            uri,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    return _client

def get_db():
    client = get_client()
    db_name = os.getenv("DB_NAME", "price_tracker")
    return client[db_name]

def test_connection():
    try:
        client = get_client()
        client.admin.command("ping")
        print("✅ MongoDB connection successful!")
        db = get_db()
        print(f"✅ Connected to database: {db.name}")
        return True
    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()