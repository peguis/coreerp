from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate


def criar_cliente(
    db: Session,
    cliente: ClienteCreate
):
    novo_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def listar_clientes(db: Session):
    return db.query(Cliente).all()


def buscar_cliente_por_id(
    db: Session,
    cliente_id: int
):
    return db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()


def atualizar_cliente(
    db: Session,
    cliente_db,
    dados
):
    for campo, valor in dados.items():
        setattr(cliente_db, campo, valor)

    db.commit()
    db.refresh(cliente_db)

    return cliente_db


def deletar_cliente(
    db: Session,
    cliente_db
):
    db.delete(cliente_db)
    db.commit()