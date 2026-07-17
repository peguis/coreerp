from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.database import get_db
from app.repositories.usuario import buscar_por_email


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/usuarios/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        usuario = buscar_por_email(
            db,
            email
        )

        if not usuario:
            raise credentials_exception

        return usuario

    except JWTError:
        raise credentials_exception