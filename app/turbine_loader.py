import requests
import pandas as pd
from app.database import get_sync_db
import os

# URLs for the turbine data
TURBINE_URLS = {
    1: "https://nextcloud.turbit.com/s/GTbSwKkMnFrKC7A/download/Turbine_1.csv",
    2: "https://nextcloud.turbit.com/s/G3bwdkrXx6Kmxs3/download/Turbine_2.csv"
}
DATA_DIR = "data"

def load_turbine_data():
    """Downloads, parses, and loads turbine CSV data into MongoDB."""
    print("Starting turbine data loading process...")
    db, client = get_sync_db()
    collection = db.turbines

    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Clear existing turbine data
    collection.delete_many({})
    print("Cleared existing data in turbines collection.")

    for turbine_id, url in TURBINE_URLS.items():
        file_path = os.path.join(DATA_DIR, f"turbine_{turbine_id}.csv")

        # Download the file
        print(f"Downloading data for Turbine {turbine_id}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded Turbine {turbine_id} data.")
        else:
            print(f"Failed to download data for Turbine {turbine_id}.")
            continue

        # Parse the CSV and load into MongoDB
        print(f"Parsing CSV file for Turbine {turbine_id}...")
        try:
            df = pd.read_csv(file_path, sep=';')
            # Rename columns to be more database-friendly
            df.rename(columns={
                '# Date and time': 'timestamp',
                'Wind speed (m/s)': 'wind_speed',
                'Power (kW)': 'power_output'
            }, inplace=True)

            # Add the turbine_id to each record
            df['turbine_id'] = turbine_id

            # Convert timestamp to datetime objects
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Convert dataframe to a list of dictionaries to insert
            records = df.to_dict('records')

            if records:
                collection.insert_many(records)
                print(f"Successfully inserted {len(records)} readings for Turbine {turbine_id}.")

        except Exception as e:
            print(f"Error processing file for Turbine {turbine_id}: {e}")

    # Create indexes for faster queries
    collection.create_index([("turbine_id", 1), ("timestamp", 1)])
    print("Created indexes on turbines collection.")

    client.close()

if __name__ == "__main__":
    load_turbine_data()
