from sqlalchemy.orm import Session, joinedload

from app.models.financeiro import LancamentoFinanceiro
from app.models.categoria_financeira import CategoriaFinanceira

from app.schemas.lancamento_financeiro import (
    LancamentoFinanceiroCreate
)



def criar_lancamento(
    db: Session,
    dados: LancamentoFinanceiroCreate,
    empresa_id: int,
    usuario_id: int
):

    if dados.categoria_id:

        categoria = (
            db.query(CategoriaFinanceira)
            .filter(
                CategoriaFinanceira.id == dados.categoria_id,
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

        descricao=dados.descricao,

        valor=dados.valor,

        tipo=dados.tipo.upper(),

        categoria_id=dados.categoria_id,

        data_vencimento=dados.data_vencimento,

        status="PENDENTE",

        observacoes=dados.observacoes

    )


    try:

        db.add(novo_lancamento)

        db.commit()

        db.refresh(novo_lancamento)


        return novo_lancamento


    except Exception:

        db.rollback()

        raise







def listar_lancamentos(
    db: Session,
    empresa_id: int
):

    return (

        db.query(LancamentoFinanceiro)

        .options(
            joinedload(
                LancamentoFinanceiro.categoria
            )
        )

        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id
        )

        .order_by(
            LancamentoFinanceiro.id.desc()
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

        .options(
            joinedload(
                LancamentoFinanceiro.categoria
            )
        )

        .filter(

            LancamentoFinanceiro.id == lancamento_id,

            LancamentoFinanceiro.empresa_id == empresa_id

        )

        .first()

    )









def atualizar_lancamento(
    db: Session,
    lancamento_db,
    dados: dict
):

    campos_permitidos = [

        "descricao",

        "valor",

        "tipo",

        "data_vencimento",

        "data_pagamento",

        "status",

        "categoria_id",

        "observacoes"

    ]



    try:


        for campo, valor in dados.items():


            if campo in campos_permitidos:


                if campo == "tipo":

                    valor = valor.upper()



                if campo == "status":

                    valor = valor.upper()



                setattr(
                    lancamento_db,
                    campo,
                    valor
                )



        db.commit()

        db.refresh(lancamento_db)



        return lancamento_db



    except Exception:

        db.rollback()

        raise







def deletar_lancamento(
    db: Session,
    lancamento_db
):

    try:

        db.delete(lancamento_db)

        db.commit()


        return lancamento_db


    except Exception:

        db.rollback()

        raise