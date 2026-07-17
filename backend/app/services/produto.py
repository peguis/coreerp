from app.repositories.produto import (
    criar_produto,
    listar_produtos,
    buscar_produto_por_id,
    atualizar_produto,
    deletar_produto
)
from app.models.produto import Produto



def criar_produto_service(
    db,
    produto,
    usuario
):

    return criar_produto(
        db,
        produto,
        usuario.empresa_id
    )


def listar_produtos_service(
    db,
    usuario
):
    return listar_produtos(
        db,
        usuario.empresa_id
    )


def buscar_produto_service(
    db,
    produto_id,
    usuario
):
    return buscar_produto_por_id(
        db,
        produto_id,
        usuario.empresa_id
    )


def atualizar_produto_service(
    db,
    produto_id,
    dados,
    usuario
):
    produto = buscar_produto_por_id(
        db,
        produto_id,
        usuario.empresa_id
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
    produto_id,
    usuario
):
    produto = buscar_produto_por_id(
        db,
        produto_id,
        usuario.empresa_id
    )

    if not produto:
        return False

    deletar_produto(
        db,
        produto
    )

    return True