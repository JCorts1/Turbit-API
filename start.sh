
set -e

# Start Docker services in the background
echo "--- Starting Docker services (MongoDB & Mongo Express) ---"
docker-compose up -d --build

# Wait a few seconds for MongoDB to initialize
echo "--- Waiting for MongoDB to be ready... ---"
sleep 5

# Install Python dependencies using pip3
echo "--- Installing Python dependencies... ---"
pip3 install -r requirements.txt

# --- THIS IS THE FIX ---
# Run BOTH data loader scripts to populate the database

echo "--- Loading JSONPlaceholder data (users, posts, comments)... ---"
python3 -m app.data_loader

echo "--- Loading Turbine data... ---"
python3 -m app.turbine_loader
# ----------------------

# Start the FastAPI application with auto-reload
echo "--- Starting FastAPI application on http://localhost:8000 ---"
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
