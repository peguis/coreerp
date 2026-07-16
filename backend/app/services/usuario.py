from sqlalchemy.orm import Session

from app.repositories.usuario import criar_usuario
from app.schemas.usuario import UsuarioCreate

from app.repositories.usuario import listar_usuarios

from app.repositories.usuario import (
    buscar_usuario_por_id,
    atualizar_usuario,
    deletar_usuario
)

def criar_usuario_service(
    db: Session,
    usuario: UsuarioCreate
):
    return criar_usuario(
        db,
        usuario
    )

def listar_usuarios_service(db):
    return listar_usuarios(db)

def buscar_usuario_service(db, usuario_id):
    return buscar_usuario_por_id(db, usuario_id)


def atualizar_usuario_service(db, usuario_id, dados):
    usuario = buscar_usuario_por_id(db, usuario_id)

    if not usuario:
        return None

    return atualizar_usuario(db, usuario, dados)


def deletar_usuario_service(db, usuario_id):
    usuario = buscar_usuario_por_id(db, usuario_id)

    if not usuario:
        return False

    deletar_usuario(db, usuario)

    return True