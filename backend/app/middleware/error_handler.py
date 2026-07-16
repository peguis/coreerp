from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor"
        }
    )