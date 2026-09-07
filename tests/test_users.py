def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "newuser@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data


def test_get_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "getuser@example.com",
            "password": "123456"
        }
    )

    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "getuser@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999999")
    assert response.status_code == 404