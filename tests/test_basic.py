
    
    
import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_not_found():
    response = client.get("/does-not-exist")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "number, expected",
    [
        (1, 2),
        (5, 6),
        (10, 11),
    ],
)
def test_numbers(number, expected):
    assert number + 1 == expected


class TestBasic:

    def test_addition(self):
        assert 2 + 2 == 4

    def test_string(self):
        assert "fastapi".upper() == "FASTAPI"


@pytest.fixture
def sample_data():
    return {
        "name": "test",
        "age": 22,
    }


def test_fixture(sample_data):
    assert sample_data["name"] == "test"
    assert sample_data["age"] == 22


def divide(a, b):
    return a / b


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)