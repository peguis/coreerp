from app.repositories.produto import (
    criar_produto,
    listar_produtos,
    buscar_produto_por_id,
    atualizar_produto,
    deletar_produto
)

from app.core.validators.produto import validar_produto





def criar_produto_service(
    db,
    produto,
    empresa_id
):

    validar_produto(
        produto
    )


    return criar_produto(
        db,
        produto,
        empresa_id
    )







def listar_produtos_service(
    db,
    empresa_id,
    busca=None,
    categoria=None,
    pagina=1,
    limite=10
):

    return listar_produtos(
        db,
        empresa_id,
        busca,
        categoria,
        pagina,
        limite
    )







def buscar_produto_service(
    db,
    produto_id,
    empresa_id
):

    return buscar_produto_por_id(
        db,
        produto_id,
        empresa_id
    )







def atualizar_produto_service(
    db,
    produto_id,
    dados,
    empresa_id
):

    produto = buscar_produto_por_id(
        db,
        produto_id,
        empresa_id
    )


    if not produto:

        return None





    if "nome" in dados:

        if not dados["nome"] or len(
            dados["nome"].strip()
        ) < 3:

            return None





    if "preco" in dados:

        if dados["preco"] < 0:

            return None





    if "estoque" in dados:

        if dados["estoque"] < 0:

            return None





    return atualizar_produto(
        db,
        produto,
        dados
    )







def deletar_produto_service(
    db,
    produto_id,
    empresa_id
):

    produto = buscar_produto_por_id(
        db,
        produto_id,
        empresa_id
    )


    if not produto:

        return False





    deletar_produto(
        db,
        produto
    )


    return True