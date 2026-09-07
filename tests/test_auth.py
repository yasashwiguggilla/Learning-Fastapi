def test_login_invalid_credentials(client):
    response = client.post(
        "/login",
        data={
            "username": "wrong@example.com",
            "password": "wrong"
        }
    )
    assert response.status_code == 403


def test_login_success(client):
    client.post(
        "/users/",
        json={
            "email": "authuser@example.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "authuser@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_protected_route_without_token(client):
    response = client.get("/posts/mine")
    assert response.status_code in (401, 403)