import requests
from app.database import get_sync_db

API_URL = "https://jsonplaceholder.typicode.com"

def fetch_and_load_data():
    """Fetches data from JSONPlaceholder and loads it into MongoDB."""
    db, client = get_sync_db()
    print("\nStarting data loading process...")

    endpoints = {
        "users": "/users",
        "posts": "/posts",
        "comments": "/comments"
    }

    for collection_name, endpoint in endpoints.items():
        print(f"\nFetching {collection_name}...")
        response = requests.get(f"{API_URL}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            collection = db[collection_name]

            # Clear existing data
            collection.delete_many({})
            print(f"Cleared existing data in {collection_name} collection")

            # Insert new data
            collection.insert_many(data)
            print(f"Inserted {len(data)} {collection_name} into MongoDB")
        else:
            print(f"Failed to fetch {collection_name}")

    # Create indexes for better query performance
    print("\nCreating indexes...")
    db.posts.create_index([("userId", 1)])
    db.comments.create_index([("postId", 1)])
    print("Indexes created successfully")

    # Verify data counts
    print("\nData verification:")
    print(f"Users count: {db.users.count_documents({})}")
    print(f"Posts count: {db.posts.count_documents({})}")
    print(f"Comments count: {db.comments.count_documents({})}")

    client.close()
    print("Disconnected from MongoDB (Sync)")
    print("\nData loading completed successfully!")


if __name__ == "__main__":
    fetch_and_load_data()
