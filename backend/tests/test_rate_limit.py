from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient

from app.middleware.rate_limit import LoginRateLimitMiddleware


def _client(max_attempts: int = 2) -> TestClient:
    app = FastAPI()

    @app.post("/usuarios/login")
    def login(request: Request):
        if request.headers.get("x-test-success") == "1":
            return {"ok": True}
        return Response(status_code=401)

    app.add_middleware(
        LoginRateLimitMiddleware,
        max_attempts=max_attempts,
        window_seconds=60,
    )
    return TestClient(app)


def test_login_rate_limit_returns_retry_after_after_failed_attempts():
    client = _client()

    assert client.post("/usuarios/login").status_code == 401
    assert client.post("/usuarios/login").status_code == 401

    response = client.post("/usuarios/login")

    assert response.status_code == 429
    assert response.headers["Retry-After"].isdigit()


def test_successful_login_clears_failed_attempts():
    client = _client()

    assert client.post("/usuarios/login").status_code == 401
    assert client.post("/usuarios/login", headers={"x-test-success": "1"}).status_code == 200
    assert client.post("/usuarios/login").status_code == 401
