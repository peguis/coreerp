import os

import pytest

from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:senha@localhost:5432/coreerp"
)

os.environ["SECRET_KEY"] = "teste_secret_key"


from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):

    response = client.post(
        "/usuarios/login",
        data={
            "username": "admin@coreerp.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }