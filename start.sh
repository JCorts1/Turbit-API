echo "Starting MongoDB with Docker Compose..."
docker-compose up -d

echo "Waiting for MongoDB to be ready..."
sleep 5

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Loading data from JSONPlaceholder API..."
python -m app.data_loader

echo "Starting FastAPI application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
