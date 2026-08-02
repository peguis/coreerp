from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.repositories import financeiro as financeiro_repository
from app.schemas.financeiro import LancamentoCreate





def criar_lancamento(
    db: Session,
    dados: LancamentoCreate,
    empresa_id: int,
    usuario_id: int
):

    if dados.valor <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor deve ser maior que zero."
        )


    if dados.tipo.upper() not in [
        "RECEITA",
        "DESPESA"
    ]:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo deve ser RECEITA ou DESPESA."
        )


    return financeiro_repository.criar_lancamento(
        db=db,
        lancamento=dados,
        empresa_id=empresa_id,
        usuario_id=usuario_id
    )









def listar_lancamentos(
    db: Session,
    empresa_id: int,
    tipo=None,
    status=None
):

    return financeiro_repository.listar_lancamentos(
        db=db,
        empresa_id=empresa_id,
        tipo=tipo,
        status=status
    )









def obter_lancamento(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    lancamento = (
        financeiro_repository.buscar_lancamento_por_id(
            db=db,
            lancamento_id=lancamento_id,
            empresa_id=empresa_id
        )
    )


    if not lancamento:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento financeiro não encontrado."
        )


    return lancamento









def baixar_lancamento(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    lancamento = (
        financeiro_repository.buscar_lancamento_por_id(
            db=db,
            lancamento_id=lancamento_id,
            empresa_id=empresa_id
        )
    )


    if not lancamento:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento financeiro não encontrado."
        )


    return financeiro_repository.baixar_lancamento(
        db=db,
        lancamento_db=lancamento
    )









def excluir_lancamento(
    db: Session,
    lancamento_id: int,
    empresa_id: int
):

    lancamento = (
        financeiro_repository.buscar_lancamento_por_id(
            db=db,
            lancamento_id=lancamento_id,
            empresa_id=empresa_id
        )
    )


    if not lancamento:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento financeiro não encontrado."
        )


    return financeiro_repository.deletar_lancamento(
        db=db,
        lancamento_db=lancamento
    )









def resumo_financeiro(
    db: Session,
    empresa_id: int
):

    lancamentos = (
        financeiro_repository.listar_lancamentos(
            db=db,
            empresa_id=empresa_id
        )
    )


    total_receber = sum(
        l.valor
        for l in lancamentos
        if l.tipo == "RECEITA"
        and l.status == "PENDENTE"
    )


    total_pagar = sum(
        l.valor
        for l in lancamentos
        if l.tipo == "DESPESA"
        and l.status == "PENDENTE"
    )


    saldo = total_receber - total_pagar


    return {

        "totalReceber": total_receber,

        "totalPagar": total_pagar,

        "saldo": saldo

    }









def listar_categorias(
    db: Session,
    empresa_id: int
):

    from app.models.categoria_financeira import CategoriaFinanceira


    return (
        db.query(CategoriaFinanceira)
        .filter(
            CategoriaFinanceira.empresa_id == empresa_id,
            CategoriaFinanceira.ativo == True
        )
        .order_by(
            CategoriaFinanceira.nome.asc()
        )
        .all()
    )