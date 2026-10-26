"""
Test AI service health check endpoint.
"""
from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/internal/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "llm_enabled" in data
    assert "embedding_enabled" in data
    # Ensure no secrets leaked
    assert "api_key" not in str(data).lower()
