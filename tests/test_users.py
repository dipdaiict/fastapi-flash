import pytest
from jose import jwt
from app import schemas
from app.config import settings
from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Home Page. Hey Buddy, Congratulations Dip Patel for Successfully Deployment."}

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
    
@pytest.fixture(scope="module")
def test_user(client):
    user_data = {"email": "testlogin@example.com", "password": "password123", "username": "testlogin"}
    res = client.post("/user/createuser", json=user_data)
    assert res.status_code == 201
    return {"id": res.json()["id"], "email": user_data["email"], "password": user_data["password"]}

def test_login_user(test_user, client):
    data={"email": test_user['email'], "password": test_user['password']}
    res = client.post("/authentication/login", json=data)
    assert res.status_code == 200
    login_res = res.json()
    assert "access_token" in login_res
    assert login_res["token_type"] == "Bearer"
    token_data = jwt.decode(login_res["access_token"], settings.secret_key, algorithms=[settings.algorithm])
    assert token_data.get("user_id") == test_user['id']
    assert token_data.get("email") == test_user['email']

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 404),  
    ('testlogin@example.com', 'wrongpassword', 404), 
    ('wrongemail@gmail.com', 'wrongpassword', 404),  
    (None, 'password123', 404),
    ('testlogin@example.com', None, 404)  
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"email": email, "password": password})
    assert res.status_code == status_code

