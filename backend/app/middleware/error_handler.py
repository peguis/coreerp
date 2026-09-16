from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(exc)

    origin = request.headers.get("origin")
    cors_headers = {}

    if origin in settings.cors_origins:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Vary": "Origin",
        }

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor"
        },
        headers=cors_headers,
    )
