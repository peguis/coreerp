from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CoreERP API"

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/coreerp"
    )


settings = Settings()