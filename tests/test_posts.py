import pytest
from app import schemas
from app.models import Post

def test_create_post(authorized_client, session):
    authorized_client, decoded_user = authorized_client
    user_id = decoded_user['user_id']
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post", "content": "Test Content", "published": True, "user_id": user_id})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"

def test_get_all_posts(authorized_client, session):
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post 1", "content": "Test Content 1", "published": True},
    )
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post 2", "content": "Test Content 2", "published": True},
    )
    response = authorized_client.get("/posts?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Post 1"
    assert data[1]["title"] == "Test Post 2"

def test_get_post(authorized_client, session):
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post", "content": "Test Content", "published": True},
    )
    post_id = response.json()["id"]
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"

def test_update_post(authorized_client, session):
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post", "content": "Test Content", "published": True},
    )
    post_id = response.json()["id"]
    response = authorized_client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Post", "content": "Updated Content", "published": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Post"
    assert data["content"] == "Updated Content"

def test_delete_post(authorized_client, session):
    response = authorized_client.post(
        "/create_post",
        json={"title": "Test Post", "content": "Test Content", "published": True},
    )
    post_id = response.json()["id"]
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 404

def test_get_user_posts(authorized_client, session):
    response = authorized_client.post(
        "/create_post",
        json={"title": "User Post", "content": "User Content", "published": True},
    )
    response = authorized_client.get("/pw_meta")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "User Post"
