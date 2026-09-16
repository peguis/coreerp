from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "CoreERP API"
    APP_VERSION: str = "0.1.0"

    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174"

    LOGIN_RATE_LIMIT_MAX_ATTEMPTS: int = 10

    LOGIN_RATE_LIMIT_WINDOW_SECONDS: int = 60

    @field_validator("SECRET_KEY")
    @classmethod
    def validar_secret_key(cls, value: str) -> str:
        if len(value) < 32 or value.lower() in {
            "change-me",
            "replace-with-at-least-32-random-characters",
            "secret",
            "teste_secret_key",
        }:
            raise ValueError(
                "SECRET_KEY deve possuir ao menos 32 caracteres e nao pode ser placeholder"
            )
        return value

    @property
    def cors_origins(self) -> list[str]:
        origins = [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

        if not origins:
            raise ValueError("CORS_ORIGINS deve conter ao menos uma origin")

        if "*" in origins:
            raise ValueError(
                "CORS_ORIGINS não pode usar '*' quando allow_credentials está habilitado"
            )

        return origins


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
