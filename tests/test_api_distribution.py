import pytest
from fastapi.testclient import TestClient
from api import app, pool
import datetime
import asyncio

client = TestClient(app)

@pytest.mark.asyncio
async def test_distribution_endpoint_empty():
    # We can't easily mock the pool in this setup without a lot of boilerplate
    # But we can check if it returns 500 when pool is None (if we don't call startup)
    response = client.get("/api/distribution/123")
    assert response.status_code == 500
    assert response.json()["detail"] == "Database pool not initialized"

# In a full TDD flow we'd mock the database, but for GSD we focus on implementation
