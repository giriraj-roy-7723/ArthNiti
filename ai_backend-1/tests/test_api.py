import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Backend!"}

def test_some_api_endpoint():
    response = client.get("/api/some-endpoint")
    assert response.status_code == 200
    assert "data" in response.json()  # Adjust based on actual response structure

def test_post_data():
    response = client.post("/api/data", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"success": True}  # Adjust based on actual response structure

def test_invalid_endpoint():
    response = client.get("/api/invalid-endpoint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}  # Adjust based on actual response structure