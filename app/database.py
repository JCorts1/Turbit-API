import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create a class to hold the database connection
class DB:
    client: AsyncIOMotorClient = None
    database = None

# Create a single instance of this class to be shared
db = DB()

# --- Asynchronous connection for FastAPI ---
async def connect_to_mongo():
    print("Connecting to MongoDB (Async)...")
    db.client = AsyncIOMotorClient(MONGODB_URL)
    db.database = db.client[DATABASE_NAME]
    print("Connected to MongoDB (Async)")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB (Async)")

# --- Synchronous connection for the data loader ---
def get_sync_db():
    """Provides a temporary synchronous database client for the data loader."""
    print("Connecting to MongoDB (Sync)...")
    sync_client = MongoClient(MONGODB_URL)
    sync_db = sync_client[DATABASE_NAME]
    return sync_db, sync_client
