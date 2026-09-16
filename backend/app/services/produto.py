from fastapi import HTTPException

from app.repositories.produto import (
    criar_produto,
    listar_produtos,
    buscar_produto_por_id,
    atualizar_produto,
    deletar_produto
)

from app.core.validators.produto import validar_produto

from app.services.movimento_estoque import movimentar_estoque





def criar_produto_service(
    db,
    produto,
    empresa_id,
    usuario_id
):

    validar_produto(
        produto
    )


    estoque_inicial = produto.estoque
    produto_para_criacao = produto.model_copy(
        update={"estoque": 0}
    )


    try:

        novo_produto = criar_produto(
            db,
            produto_para_criacao,
            empresa_id
        )


        if estoque_inicial > 0:

            movimento_inicial = movimentar_estoque(
                db=db,
                empresa_id=empresa_id,
                produto_id=novo_produto.id,
                tipo="ENTRADA",
                quantidade=estoque_inicial,
                usuario_id=usuario_id,
                observacao="Estoque inicial",
                produto=novo_produto
            )


            if not movimento_inicial:

                raise HTTPException(
                    status_code=400,
                    detail="N\u00e3o foi poss\u00edvel registrar o estoque inicial."
                )


        db.commit()

        db.refresh(novo_produto)


        return novo_produto


    except Exception:

        db.rollback()

        raise







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





    if "estoque" in dados:

        raise HTTPException(
            status_code=400,
            detail=(
                "Estoque nÃ£o pode ser alterado diretamente. "
                "Utilize uma movimentaÃ§Ã£o de estoque."
            )
        )


    if (
        "ultima_entrada" in dados
        or "ultima_saida" in dados
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "ultima_entrada e ultima_saida são controlados pelo sistema."
            )
        )


    if "custo_medio" in dados:

        raise HTTPException(
            status_code=400,
            detail=(
                "custo_medio não é calculado automaticamente "
                "e é controlado pelo sistema."
            )
        )


    if "nome" in dados:

        if not dados["nome"] or len(
            dados["nome"].strip()
        ) < 3:

            return None





    if "preco" in dados:

        if dados["preco"] < 0:

            return None





    for campo in (
        "estoque_minimo",
        "estoque_maximo"
    ):

        if campo in dados:

            valor = dados[campo]

            if (
                isinstance(valor, bool)
                or not isinstance(valor, int)
                or valor < 0
            ):

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
