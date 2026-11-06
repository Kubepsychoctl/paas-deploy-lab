import pytest

import app as app_module


@pytest.fixture(autouse=True)
def clean_state():
    app_module.USERS.clear()
    app_module.NEXT_ID = 1


@pytest.fixture
def client():
    return app_module.app.test_client()


def test_health_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_home_has_version(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_create_and_get_user(client):
    created = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert created.status_code == 201
    user_id = created.get_json()["id"]
    fetched = client.get(f"/users/{user_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["email"] == "alice@example.com"


def test_duplicate_email_rejected(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    again = client.post("/users", json={"name": "Alice2", "email": "alice@example.com"})
    assert again.status_code == 409


def test_missing_fields_rejected(client):
    assert client.post("/users", json={"name": "NoEmail"}).status_code == 400


def test_unknown_user_404(client):
    assert client.get("/users/999").status_code == 404
