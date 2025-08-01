import requests
from app.database import get_sync_database, close_sync_connection
import sys
import time


BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_data(endpoint):
    """Fetch data from JSONPlaceholder API."""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return None


def load_data_to_mongodb():
    """Load all data from JSONPlaceholder API to MongoDB."""
    print("Starting data loading process...")

    # Get database connection
    db = get_sync_database()

    # Define endpoints and their corresponding collection names
    endpoints = {
        "users": "users",
        "posts": "posts",
        "comments": "comments"
    }

    for endpoint, collection_name in endpoints.items():
        print(f"\nFetching {endpoint}...")
        data = fetch_data(endpoint)

        if data:
            # Clear existing data in collection
            db[collection_name].delete_many({})
            print(f"Cleared existing data in {collection_name} collection")

            # Insert new data
            if isinstance(data, list) and len(data) > 0:
                result = db[collection_name].insert_many(data)
                print(f"Inserted {len(result.inserted_ids)} {endpoint} into MongoDB")
            else:
                print(f"No data to insert for {endpoint}")
        else:
            print(f"Failed to fetch {endpoint}")

    # Create indexes for better query performance
    print("\nCreating indexes...")
    db.posts.create_index("userId")
    db.comments.create_index("postId")
    print("Indexes created successfully")

    # Verify data
    print("\nData verification:")
    print(f"Users count: {db.users.count_documents({})}")
    print(f"Posts count: {db.posts.count_documents({})}")
    print(f"Comments count: {db.comments.count_documents({})}")

    close_sync_connection()
    print("\nData loading completed successfully!")


if __name__ == "__main__":
    # Wait a bit for MongoDB to be ready if running right after docker-compose up
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        print("Waiting 5 seconds for MongoDB to be ready...")
        time.sleep(5)

    load_data_to_mongodb()
