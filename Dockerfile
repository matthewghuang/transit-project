# --- Stage 1: Build Frontend ---
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy source and build
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Runtime ---
FROM python:3.13-slim

# Install system dependencies (needed for confluent-kafka and other libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml uv.lock ./
# We'll use pip to install since we're in a container, 
# or you could use 'uv' if preferred.
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port for FastAPI
EXPOSE 8000

# Default command: Run the API
# For Azure, you can override this command for workers or use a supervisor
CMD ["fastapi", "run", "api.py", "--port", "8000", "--host", "0.0.0.0"]
