from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

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

from app.models.movimento_estoque import MovimentoEstoque




def criar_movimento_service(
    db: Session,
    movimento,
    empresa_id: int,
    usuario_id: int
):

    validar_movimento(
        movimento.quantidade,
        movimento.tipo
    )


    movimento.tipo = movimento.tipo.upper()



    produto = buscar_produto_por_id(
        db,
        movimento.produto_id,
        empresa_id
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




        novo_movimento = criar_movimento(
            db=db,
            movimento=movimento,
            empresa_id=empresa_id,
            usuario_id=usuario_id
        )



        db.commit()

        db.refresh(
            novo_movimento
        )


        return novo_movimento



    except Exception:

        db.rollback()

        raise






def listar_movimentos_service(
    db: Session,
    empresa_id: int
):


    movimentos = (

        db.query(MovimentoEstoque)

        .options(
            joinedload(
                MovimentoEstoque.produto
            )
        )

        .filter(
            MovimentoEstoque.empresa_id == empresa_id
        )

        .all()

    )


    return movimentos






def buscar_movimento_service(
    db: Session,
    movimento_id: int,
    empresa_id: int
):

    return buscar_movimento_por_id(
        db,
        movimento_id,
        empresa_id
    )