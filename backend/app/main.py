from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import logger
from app.middleware.error_handler import generic_exception_handler


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

    allow_origins=[
        "http://localhost:5173",
        "https://realized-producing-confidentiality-compatibility.trycloudflare.com"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


logger.info("CoreERP iniciado com sucesso.")


app.include_router(router)


@app.get("/")
def home():
    logger.info("Rota raiz acessada.")

    return {
        "mensagem": f"{settings.APP_NAME} API online!"
    }