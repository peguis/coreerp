from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.hash import gerar_hash


def criar_usuario(
    db: Session,
    usuario: UsuarioCreate
):
    novo_usuario = Usuario(
    nome=usuario.nome,
    email=usuario.email,
    senha=gerar_hash(usuario.senha),
    empresa_id=usuario.empresa_id
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

def listar_usuarios(db: Session):
    return db.query(Usuario).all()

def buscar_usuario_por_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()


def atualizar_usuario(db: Session, usuario_db, dados):
    for campo, valor in dados.items():
        setattr(usuario_db, campo, valor)

    db.commit()
    db.refresh(usuario_db)

    return usuario_db


def deletar_usuario(db: Session, usuario_db):
    db.delete(usuario_db)
    db.commit()
    

def buscar_por_email(db, email):

    return (
        db.query(Usuario)
        .filter(
            Usuario.email == email
        )
        .first()
    )