import pytest
from app import schemas
from app.models import Post
from app.main import app

def test_create_post(authorized_client, session):
    client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    post_data = {"title": "Test Post", "content": "Test Content", "published": True, "user_id": user_id}
    
    response = client.post("/create_post", json=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]

def test_get_all_posts(authorized_client, session):
    client, _ = authorized_client
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Assuming there's only one post in the database
    assert data[0]["title"] == "Test Post"

def test_get_post(authorized_client, session):
    client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    post_data = {"title": "New Post Title", "content": "New Post Content", "published": True, "user_id": user_id}
    
    response = client.post("/create_post", json=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["published"] == post_data["published"]

def test_update_post(authorized_client, session):
    client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    response = client.post("/create_post", json={"title": "Test Post x", "content": "Test Content x", "published": True, "user_id": user_id})
    assert response.status_code == 201
    post_data = response.json()
    post_id = post_data["id"]
    
    update_data = {"title": "Updated Post", "content": "Updated Content", "published": False}
    update_response = client.put(f"/posts/{post_id}", json=update_data)
    assert update_response.status_code == 200
    updated_post = update_response.json()
    assert updated_post["title"] == update_data["title"]
    assert updated_post["content"] == update_data["content"]
    assert updated_post["published"] == update_data["published"]

def test_delete_post(authorized_client, session):
    client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    response = client.post("/create_post", json={"title": "Test Post", "content": "Test Content", "published": True, "user_id": user_id})
    assert response.status_code == 201
    post_id = response.json()["id"]
    
    delete_response = client.delete(f"/posts/{post_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404

def test_get_user_posts(authorized_client, session):
    client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    post_data = {"title": "User Post", "content": "User Content", "published": True, "user_id": user_id}
    
    response = client.post("/create_post", json=post_data)
    assert response.status_code == 201
    
    get_response = client.get("/posts")
    assert get_response.status_code == 200
    data = get_response.json()
    assert len(data) >= 1  # Assuming there might be other posts too
    assert data[-1]["title"] == post_data["title"]
