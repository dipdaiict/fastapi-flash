from jose import jwt
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'Message': 'Welcome to the Home Page.'}
    
