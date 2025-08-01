from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper function to register and login a user and get token
def get_auth_token():
    username = "taskuser"
    password = "taskpass"
    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post("/auth/login", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return token

def test_create_task():
    token = get_auth_token()
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

def test_get_tasks():
    token = get_auth_token()
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    token = get_auth_token()
    # Create a task first
    response = client.post(
        "/tasks/",
        json={"title": "Old Task", "description": "Old Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Update the task
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Updated Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"

def test_delete_task():
    token = get_auth_token()
    # Create a task first
    response = client.post(
        "/tasks/",
        json={"title": "Task to Delete", "description": "Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
