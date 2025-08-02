from app.database import get_sync_database, close_sync_connection

def check_turbine_dates():
    """Check the date range of turbine data in MongoDB"""
    db = get_sync_database()

    print("Checking turbine data date ranges...")

    # Check if turbine_readings collection exists
    collections = db.list_collection_names()
    print(f"\nAvailable collections: {collections}")

    if "turbine_readings" not in collections:
        print("\n❌ ERROR: 'turbine_readings' collection not found!")
        print("Please run: python -m app.turbine_loader")
        return

    # Check data for each turbine
    for turbine_id in [1, 2]:
        print(f"\n--- Turbine {turbine_id} ---")

        # Count documents
        count = db.turbine_readings.count_documents({"turbine_id": turbine_id})
        print(f"Total readings: {count}")

        if count > 0:
            # Get date range
            oldest = db.turbine_readings.find_one(
                {"turbine_id": turbine_id},
                sort=[("timestamp", 1)]
            )
            newest = db.turbine_readings.find_one(
                {"turbine_id": turbine_id},
                sort=[("timestamp", -1)]
            )

            print(f"Oldest reading: {oldest['timestamp']}")
            print(f"Newest reading: {newest['timestamp']}")

            # Sample a few records
            print("\nSample records:")
            samples = db.turbine_readings.find(
                {"turbine_id": turbine_id}
            ).limit(3)

            for i, sample in enumerate(samples):
                print(f"  Sample {i+1}: {sample['timestamp']} - Wind: {sample['wind_speed']} m/s, Power: {sample['power_output']} kW")

    close_sync_connection()

if __name__ == "__main__":
    check_turbine_dates()
