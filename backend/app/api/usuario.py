from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.auth import Login
from app.services.usuario import (
    criar_usuario_service,
    listar_usuarios_service,
    buscar_usuario_service,
    atualizar_usuario_service,
    deletar_usuario_service,
    login_service
)
from fastapi import HTTPException
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UsuarioResponse
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return criar_usuario_service(
        db,
        usuario
    )

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_usuarios_service(db)

@router.get("/me", response_model=UsuarioResponse)
def usuario_logado(
    usuario=Depends(get_current_user)
):
    return usuario


@router.get("/{usuario_id}")
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = buscar_usuario_service(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return UsuarioResponse.model_validate(usuario)

@router.put("/{usuario_id}")
def editar_usuario(
    usuario_id: int,
    dados: dict,
    db: Session = Depends(get_db)
):
    usuario = atualizar_usuario_service(
        db,
        usuario_id,
        dados
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return UsuarioResponse.model_validate(usuario)

@router.delete("/{usuario_id}")
def remover_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    sucesso = deletar_usuario_service(
        db,
        usuario_id
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "mensagem": "Usuário removido"
    }

@router.post("/login")
def login(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_service(
        db,
        dados
    )

