
def test_vote_without_token(client):
    response = client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 1
        }
    )
    assert response.status_code in (401, 403)


def test_invalid_vote_direction(client):
    response = client.post(
        "/vote/",
        json={
            "post_id": 1,
            "dir": 5
        }
    )
    assert response.status_code in (401, 403, 422)