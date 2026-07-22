from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCreate

from app.repositories.usuario import (
    criar_usuario,
    listar_usuarios,
    buscar_usuario_por_id,
    atualizar_usuario,
    deletar_usuario,
    buscar_por_email
)

from app.auth.hash import verificar_senha
from app.auth.jwt import criar_token

from app.core.validators.usuario import validar_usuario


def criar_usuario_service(
    db: Session,
    usuario: UsuarioCreate
):

    validar_usuario(usuario)

    return criar_usuario(
        db,
        usuario
    )


def listar_usuarios_service(
    db
):

    return listar_usuarios(db)


def buscar_usuario_service(
    db,
    usuario_id
):

    return buscar_usuario_por_id(
        db,
        usuario_id
    )


def atualizar_usuario_service(
    db,
    usuario_id,
    dados
):

    usuario = buscar_usuario_por_id(
        db,
        usuario_id
    )

    if not usuario:
        return None

    if "nome" in dados:
        if len(dados["nome"].strip()) < 3:
            return None

    if "senha" in dados:
        if len(dados["senha"]) < 6:
            return None

    return atualizar_usuario(
        db,
        usuario,
        dados
    )


def deletar_usuario_service(
    db,
    usuario_id
):

    usuario = buscar_usuario_por_id(
        db,
        usuario_id
    )

    if not usuario:
        return False

    deletar_usuario(
        db,
        usuario
    )

    return True


def login_service(
    db,
    dados
):

    usuario = buscar_por_email(
        db,
        dados.username
    )

    if not usuario:
        return None

    if not verificar_senha(
        dados.password,
        usuario.senha
    ):
        return None

    token = criar_token(
        {
            "sub": usuario.email,
            "empresa_id": usuario.empresa_id,
            "perfil": usuario.perfil
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }