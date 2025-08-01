import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://root:example@localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "turbit_db")

# Async motor client for FastAPI
motor_client = None
database = None

# Sync pymongo client for data loading
sync_client = None
sync_database = None


async def connect_to_mongo():
    """Create database connection for FastAPI."""
    global motor_client, database
    motor_client = AsyncIOMotorClient(MONGODB_URL)
    database = motor_client[DATABASE_NAME]
    print("Connected to MongoDB (Async)")


async def close_mongo_connection():
    """Close database connection."""
    global motor_client
    if motor_client:
        motor_client.close()
        print("Disconnected from MongoDB (Async)")


def get_sync_database():
    """Get synchronous database connection for data loading."""
    global sync_client, sync_database
    if sync_client is None:
        sync_client = MongoClient(MONGODB_URL)
        sync_database = sync_client[DATABASE_NAME]
        print("Connected to MongoDB (Sync)")
    return sync_database


def close_sync_connection():
    """Close synchronous database connection."""
    global sync_client
    if sync_client:
        sync_client.close()
        print("Disconnected from MongoDB (Sync)")
