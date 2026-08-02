from sqlalchemy.orm import Session

from app.models.financeiro import LancamentoFinanceiro
from app.models.categoria_financeira import CategoriaFinanceira

from app.schemas.financeiro import LancamentoCreate





def criar_lancamento(
    db: Session,
    lancamento: LancamentoCreate,
    empresa_id: int,
    usuario_id: int
):

    if lancamento.categoria_id:

        categoria = (
            db.query(CategoriaFinanceira)
            .filter(
                CategoriaFinanceira.id == lancamento.categoria_id,
                CategoriaFinanceira.empresa_id == empresa_id
            )
            .first()
        )


        if not categoria:

            raise ValueError(
                "Categoria financeira inválida para esta empresa."
            )



    novo_lancamento = LancamentoFinanceiro(

        empresa_id=empresa_id,

        usuario_id=usuario_id,

        descricao=lancamento.descricao,

        valor=lancamento.valor,

        tipo=lancamento.tipo.upper(),

        categoria_id=lancamento.categoria_id,

        data_vencimento=lancamento.data_vencimento,

        status=lancamento.status.upper(),

        observacoes=lancamento.observacoes

    )


    db.add(novo_lancamento)

    db.commit()

    db.refresh(novo_lancamento)


    return novo_lancamento





def listar_lancamentos(
    db: Session,
    empresa_id: int,
    tipo=None,
    status=None
):

    query = (
        db.query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id
        )
    )


    if tipo:

        query = query.filter(
            LancamentoFinanceiro.tipo == tipo.upper()
        )


    if status:

        query = query.filter(
            LancamentoFinanceiro.status == status.upper()
        )


    return (
        query
        .order_by(
            LancamentoFinanceiro.data_vencimento.asc()
        )
        .all()
    )





def buscar_lancamento_por_id(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    return (
        db.query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.id == lancamento_id,
            LancamentoFinanceiro.empresa_id == empresa_id
        )
        .first()
    )





def baixar_lancamento(
    db: Session,
    lancamento_db
):

    if lancamento_db.tipo == "RECEITA":

        lancamento_db.status = "RECEBIDO"

    else:

        lancamento_db.status = "PAGO"


    from datetime import datetime

    lancamento_db.data_pagamento = datetime.now()


    db.commit()

    db.refresh(lancamento_db)


    return lancamento_db





def deletar_lancamento(
    db: Session,
    lancamento_db
):

    db.delete(lancamento_db)

    db.commit()


    return lancamento_db