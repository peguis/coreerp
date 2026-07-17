from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings


def criar_token(data: dict):

    dados = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        dados,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )