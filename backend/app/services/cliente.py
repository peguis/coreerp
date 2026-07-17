from sqlalchemy.orm import Session

from app.repositories.cliente import (
    criar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    deletar_cliente
)


def criar_cliente_service(
    db: Session,
    cliente
):
    return criar_cliente(
        db,
        cliente
    )


def listar_clientes_service(db):
    return listar_clientes(db)


def buscar_cliente_service(
    db,
    cliente_id
):
    return buscar_cliente_por_id(
        db,
        cliente_id
    )


def atualizar_cliente_service(
    db,
    cliente_id,
    dados
):
    cliente = buscar_cliente_por_id(
        db,
        cliente_id
    )

    if not cliente:
        return None

    return atualizar_cliente(
        db,
        cliente,
        dados
    )


def deletar_cliente_service(
    db,
    cliente_id
):
    cliente = buscar_cliente_por_id(
        db,
        cliente_id
    )

    if not cliente:
        return False

    deletar_cliente(
        db,
        cliente
    )

    return True