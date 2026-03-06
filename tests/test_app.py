import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_calculate_add(client):
    response = client.get("/calculate/add/3.0/4.0")
    assert response.status_code == 200
    assert response.get_json()["result"] == 7.0


def test_calculate_divide_by_zero(client):
    response = client.get("/calculate/divide/5.0/0.0")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_calculate_unknown_op(client):
    response = client.get("/calculate/power/2.0/3.0")
    assert response.status_code == 400
