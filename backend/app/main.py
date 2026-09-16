from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import logger
from app.database.connection import engine
from app.middleware.error_handler import generic_exception_handler
from app.middleware.rate_limit import LoginRateLimitMiddleware


from app.api.router import router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    LoginRateLimitMiddleware,
    max_attempts=settings.LOGIN_RATE_LIMIT_MAX_ATTEMPTS,
    window_seconds=settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS,
)


logger.info("CoreERP iniciado com sucesso.")


app.include_router(router)


@app.get("/")
def home():

    logger.info("Rota raiz acessada.")

    return {
        "mensagem": f"{settings.APP_NAME} API online!"
    }


@app.get("/healthz", include_in_schema=False)
def healthz():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok"}
