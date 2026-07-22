from app.repositories.movimento_estoque import (
    criar_movimento,
    listar_movimentos,
    buscar_movimento_por_id
)

from app.repositories.produto import (
    buscar_produto_por_id
)

from app.core.validators.movimento_estoque import (
    validar_movimento
)

from fastapi import HTTPException



def criar_movimento_service(
    db,
    movimento,
    usuario
):

    validar_movimento(
        movimento.quantidade,
        movimento.tipo
    )


    movimento.tipo = movimento.tipo.upper()



    produto = buscar_produto_por_id(
        db,
        movimento.produto_id,
        usuario.empresa_id
    )



    if not produto:
        return None



    try:

        if movimento.tipo == "ENTRADA":


            produto.estoque += movimento.quantidade



        elif movimento.tipo == "SAIDA":


            if produto.estoque < movimento.quantidade:

                raise HTTPException(
                    status_code=400,
                    detail="Estoque insuficiente"
                )


            produto.estoque -= movimento.quantidade



        elif movimento.tipo == "AJUSTE":


            produto.estoque = movimento.quantidade



        movimento.empresa_id = usuario.empresa_id

        movimento.usuario_id = usuario.id



        db.add(produto)

        db.add(movimento)

        db.commit()

        db.refresh(movimento)



        return movimento



    except Exception:

        db.rollback()

        raise





def listar_movimentos_service(
    db,
    usuario
):

    return listar_movimentos(
        db,
        usuario.empresa_id
    )





def buscar_movimento_service(
    db,
    movimento_id,
    usuario
):

    return buscar_movimento_por_id(
        db,
        movimento_id,
        usuario.empresa_id
    )