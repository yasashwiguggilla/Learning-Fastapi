def test_get_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_post_not_found(client):
    response = client.get("/posts/999999")
    assert response.status_code == 404


def test_create_post_without_token(client):
    response = client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Test Content",
            "published": True
        }
    )
    assert response.status_code in (401, 403)


def test_get_my_posts_without_token(client):
    response = client.get("/posts/mine")
    assert response.status_code in (401, 403)