import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

# Get connection details
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://root:example@localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "turbit_db")

print(f"Connecting to: {MONGODB_URL}")
print(f"Database: {DATABASE_NAME}")

try:
    # Direct connection using pymongo
    client = pymongo.MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # List all collections
    collections = db.list_collection_names()
    print(f"\nCollections in {DATABASE_NAME}: {collections}")

    # Check turbines collection (not turbine_readings)
    if "turbines" in collections:
        count1 = db.turbines.count_documents({"turbine_id": 1})
        count2 = db.turbines.count_documents({"turbine_id": 2})
        print(f"\nTurbine 1 readings: {count1}")
        print(f"Turbine 2 readings: {count2}")

        # Get date range for turbine 1
        if count1 > 0:
            oldest = db.turbines.find_one({"turbine_id": 1}, sort=[("timestamp", 1)])
            newest = db.turbines.find_one({"turbine_id": 1}, sort=[("timestamp", -1)])
            print(f"\nTurbine 1 date range:")
            print(f"  Oldest: {oldest['timestamp']}")
            print(f"  Newest: {newest['timestamp']}")

            # Show sample data
            print(f"\nSample data from Turbine 1:")
            samples = db.turbines.find({"turbine_id": 1}).limit(3)
            for i, sample in enumerate(samples):
                print(f"  {i+1}. Time: {sample['timestamp']}, Wind: {sample['wind_speed']} m/s, Power: {sample['power_output']} kW")

        # Get date range for turbine 2
        if count2 > 0:
            oldest = db.turbines.find_one({"turbine_id": 2}, sort=[("timestamp", 1)])
            newest = db.turbines.find_one({"turbine_id": 2}, sort=[("timestamp", -1)])
            print(f"\nTurbine 2 date range:")
            print(f"  Oldest: {oldest['timestamp']}")
            print(f"  Newest: {newest['timestamp']}")
    else:
        print("\n⚠️  turbines collection not found!")
        print("Run: python3 -m app.turbine_loader")

    client.close()

except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure MongoDB is running:")
    print("  docker ps")
    print("  docker-compose up -d")
