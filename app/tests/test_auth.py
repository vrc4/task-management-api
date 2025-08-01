from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_register_user():
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"  # <-- generate unique username
    response = client.post(
        "/auth/register",
        json={"username": unique_username, "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == unique_username
    assert "id" in data

def test_login_user():
    # First register user to ensure user exists
    client.post("/auth/register", json={"username": "loginuser", "password": "loginpass"})
    
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "loginpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
