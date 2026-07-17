from sqlalchemy.orm import Session

from app.repositories.produto import (
    criar_produto,
    listar_produtos,
    buscar_produto_por_id,
    atualizar_produto,
    deletar_produto
)


def criar_produto_service(
    db: Session,
    produto
):
    return criar_produto(db, produto)


def listar_produtos_service(db):
    return listar_produtos(db)


def buscar_produto_service(
    db,
    produto_id
):
    return buscar_produto_por_id(
        db,
        produto_id
    )


def atualizar_produto_service(
    db,
    produto_id,
    dados
):
    produto = buscar_produto_por_id(
        db,
        produto_id
    )

    if not produto:
        return None

    return atualizar_produto(
        db,
        produto,
        dados
    )


def deletar_produto_service(
    db,
    produto_id
):
    produto = buscar_produto_por_id(
        db,
        produto_id
    )

    if not produto:
        return False

    deletar_produto(
        db,
        produto
    )

    return True