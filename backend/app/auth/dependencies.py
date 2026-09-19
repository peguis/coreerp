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
        detail="Token inválido"
    )


    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )


        email = payload.get("sub")


        if not email:
            raise credentials_exception



        usuario = buscar_por_email(
            db,
            email
        )


        if not usuario:
            raise credentials_exception



        if not usuario.ativo:

            raise HTTPException(
                status_code=403,
                detail="Usuário inativo"
            )


        if not usuario.empresa.ativo:

            raise HTTPException(
                status_code=403,
                detail="Empresa inativa"
            )


        return usuario



    except JWTError:

        raise credentials_exception





def require_perfil(*perfis):


    def verificar(
        usuario=Depends(get_current_user)
    ):


        if usuario.perfil not in perfis:


            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para esta ação"
            )


        return usuario


    return verificar


def require_modulo(*codigos):
    def verificar_modulo(
        usuario=Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        from app.models.modulo import EmpresaModulo, Modulo

        # Bancos legados ainda não possuem o catálogo. Nesse estado o comportamento
        # anterior é preservado até a migração ser aplicada.
        if db.query(Modulo.id).first() is None:
            return usuario

        habilitado = (
            db.query(EmpresaModulo.id)
            .join(Modulo, Modulo.id == EmpresaModulo.modulo_id)
            .filter(
                EmpresaModulo.empresa_id == usuario.empresa_id,
                EmpresaModulo.ativo.is_(True),
                Modulo.codigo.in_(codigos),
            )
            .first()
        )
        if not habilitado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este módulo não está ativo para a empresa.",
            )
        return usuario

    return verificar_modulo
