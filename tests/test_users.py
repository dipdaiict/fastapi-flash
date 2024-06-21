from fastapi.testclient import TestClient
from app import schemas

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'Message': 'Welcome to the Home Page.'}

def test_create_user(client: TestClient):
    res = client.post(
        "/user/createuser", json={"email": "uniqueemail@example.com", "password": "newpassword456", 
                                  "username": "uniqueuser"})
    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "uniqueemail@example.com"

def test_create_user_email_exists(client: TestClient):
    client.post("/user/createuser", json={
        "email": "testemail@example.com",
        "username": "testuser",
        "password": "password123"
    })
    response = client.post("/user/createuser", json={
        "email": "testemail@example.com",
        "username": "anotheruser",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists."}

def test_create_user_username_exists(client: TestClient):
    client.post("/user/createuser", json={
        "email": "testemail2@example.com",
        "username": "testuser2",
        "password": "password123"
    })
    response = client.post("/user/createuser", json={
        "email": "anothertestemail@example.com",
        "username": "testuser2",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists."}
