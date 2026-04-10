#!/bin/bash

# Configuration
FRONTEND_DIR="frontend"
VENV_PATH=".venv"

# Trap SIGINT (Ctrl+C) and kill all background processes
cleanup() {
    echo ""
    echo "Shutting down services..."
    # Kill the background process groups
    kill 0
    exit 0
}

trap cleanup SIGINT

echo "Starting infrastructure (Docker)..."
docker-compose up -d

echo "Waiting for infrastructure to be ready..."
# Give it a few seconds for TimescaleDB and Kafka to initialize
sleep 5

echo "Initializing database schema and loading GTFS stops..."
uv run python db_init.py

echo "Starting backend services..."

# Start producer
echo "Starting producer (main.py)..."
uv run python main.py &

# Start consumer
echo "Starting consumer (delay_consumer.py)..."
uv run python delay_consumer.py &

# Start API
echo "Starting API (api.py)..."
uv run fastapi run api.py &

echo "Starting frontend..."
cd "$FRONTEND_DIR" && npm start &

# Wait for all background processes to finish (which they won't unless killed)
wait
