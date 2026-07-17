from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CoreERP API"
    APP_VERSION: str = "0.1.0"

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/coreerp"
    )

    SECRET_KEY: str = "sua-chave-super-secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()