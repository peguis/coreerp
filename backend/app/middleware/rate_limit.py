"""Small, process-local protection for the login endpoint.

This intentionally has no external dependency. A shared store or an edge
rate limiter should replace it before running multiple backend instances.
"""

from collections import defaultdict, deque
from math import ceil
from threading import Lock
from time import monotonic

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoginRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_attempts: int = 10, window_seconds: int = 60):
        super().__init__(app)
        if max_attempts <= 0 or window_seconds <= 0:
            raise ValueError("login rate limit values must be positive")
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts = defaultdict(deque)
        self._lock = Lock()

    @staticmethod
    def _is_login(request: Request) -> bool:
        return (
            request.method.upper() == "POST"
            and request.url.path.rstrip("/") == "/usuarios/login"
        )

    @staticmethod
    def _client_key(request: Request) -> str:
        return request.client.host if request.client else "unknown"

    def _prune(self, attempts: deque, now: float) -> None:
        cutoff = now - self.window_seconds
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()

    async def dispatch(self, request: Request, call_next) -> Response:
        if not self._is_login(request):
            return await call_next(request)

        key = self._client_key(request)
        now = monotonic()
        with self._lock:
            attempts = self._attempts[key]
            self._prune(attempts, now)
            if len(attempts) >= self.max_attempts:
                retry_after = max(1, ceil(self.window_seconds - (now - attempts[0])))
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": (
                            "Muitas tentativas de login. "
                            "Tente novamente em instantes."
                        )
                    },
                    headers={"Retry-After": str(retry_after)},
                )

        response = await call_next(request)
        with self._lock:
            attempts = self._attempts[key]
            self._prune(attempts, monotonic())
            if response.status_code == 401:
                attempts.append(monotonic())
            elif 200 <= response.status_code < 300:
                self._attempts.pop(key, None)
        return response
