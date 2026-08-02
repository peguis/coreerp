from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.repositories.lancamento_financeiro import (
    criar_lancamento,
    listar_lancamentos,
    buscar_lancamento_por_id,
    atualizar_lancamento,
    deletar_lancamento
)

from app.schemas.lancamento_financeiro import (
    LancamentoFinanceiroCreate,
    LancamentoFinanceiroUpdate
)



def criar_lancamento_service(
    db: Session,
    dados: LancamentoFinanceiroCreate,
    empresa_id: int,
    usuario_id: int
):

    if dados.valor <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor deve ser maior que zero"
        )


    if dados.tipo.upper() not in [
        "RECEITA",
        "DESPESA"
    ]:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo deve ser RECEITA ou DESPESA"
        )


    return criar_lancamento(
        db,
        dados,
        empresa_id,
        usuario_id
    )



def listar_lancamentos_service(
    db: Session,
    empresa_id: int
):

    return listar_lancamentos(
        db,
        empresa_id
    )



def buscar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    lancamento = buscar_lancamento_por_id(
        db,
        lancamento_id,
        empresa_id
    )


    if not lancamento:

        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )


    return lancamento



def atualizar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int,
    dados: LancamentoFinanceiroUpdate
):

    lancamento = buscar_lancamento_por_id(
        db,
        lancamento_id,
        empresa_id
    )


    if not lancamento:

        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )


    dados_dict = dados.model_dump(
        exclude_unset=True
    )


    return atualizar_lancamento(
        db,
        lancamento,
        dados_dict
    )



def deletar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    lancamento = buscar_lancamento_por_id(
        db,
        lancamento_id,
        empresa_id
    )


    if not lancamento:

        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )


    return deletar_lancamento(
        db,
        lancamento
    )