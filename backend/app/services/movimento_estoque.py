from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.repositories.movimento_estoque import (
    criar_movimento,
    listar_movimentos,
    buscar_movimento_por_id
)

from app.repositories.produto import (
    buscar_produto_para_movimento
)

from app.core.validators.movimento_estoque import (
    validar_movimento
)

from app.schemas.movimento_estoque import MovimentoEstoqueCreate

from app.models.produto import Produto
from app.models.movimento_estoque import MovimentoEstoque




def movimentar_estoque(
    db: Session,
    empresa_id: int,
    produto_id: int | None,
    tipo: str,
    quantidade: int,
    usuario_id: int,
    observacao: str | None = None,
    produto: Produto | None = None
):

    validar_movimento(
        quantidade,
        tipo
    )


    tipo = tipo.upper()


    if produto is not None and (
        produto.empresa_id != empresa_id
        or (
            produto_id is not None
            and produto.id != produto_id
        )
    ):

        return None


    produto_alvo_id = (
        produto.id
        if produto is not None
        else produto_id
    )


    produto = buscar_produto_para_movimento(
        db,
        produto_alvo_id,
        empresa_id
    )


    if not produto:

        return None


    if tipo == "AJUSTE" and (
        not isinstance(observacao, str)
        or not observacao.strip()
    ):

        raise HTTPException(
            status_code=400,
            detail="Ajuste exige uma observa\u00e7\u00e3o/motivo."
        )


    estoque_anterior = produto.estoque

    instante_movimento = datetime.now(timezone.utc).replace(
        tzinfo=None
    )


    if tipo == "ENTRADA":

        produto.estoque += quantidade
        produto.ultima_entrada = instante_movimento


    elif tipo == "SAIDA":

        if produto.estoque < quantidade:

            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente"
            )


        produto.estoque -= quantidade
        produto.ultima_saida = instante_movimento


    elif tipo == "AJUSTE":

        produto.estoque = quantidade


    movimento_registro = MovimentoEstoqueCreate(
        produto_id=produto.id,
        tipo=tipo,
        quantidade=quantidade,
        observacao=observacao
    )


    return criar_movimento(
        db=db,
        movimento=movimento_registro,
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        estoque_anterior=estoque_anterior,
        estoque_posterior=produto.estoque,
        created_at=instante_movimento
    )





def criar_movimento_service(
    db: Session,
    movimento,
    empresa_id: int,
    usuario_id: int
):

    try:

        novo_movimento = movimentar_estoque(
            db=db,
            empresa_id=empresa_id,
            produto_id=movimento.produto_id,
            tipo=movimento.tipo,
            quantidade=movimento.quantidade,
            usuario_id=usuario_id,
            observacao=movimento.observacao
        )


        if not novo_movimento:

            return None


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
