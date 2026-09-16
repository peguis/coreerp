from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.categoria_financeira import buscar_categoria_por_id
from app.repositories.lancamento_financeiro import (
    atualizar_lancamento,
    buscar_lancamento_por_id,
    criar_lancamento,
    deletar_lancamento,
    listar_lancamentos,
)
from app.schemas.lancamento_financeiro import (
    LancamentoFinanceiroCreate,
    LancamentoFinanceiroUpdate,
)


def criar_lancamento_service(
    db: Session,
    dados: LancamentoFinanceiroCreate,
    empresa_id: int,
    usuario_id: int,
):
    if dados.valor <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor deve ser maior que zero",
        )
    if dados.tipo.upper() not in {"RECEITA", "DESPESA"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo deve ser RECEITA ou DESPESA",
        )
    try:
        lancamento = criar_lancamento(db, dados, empresa_id, usuario_id)
        db.commit()
        db.refresh(lancamento)
        return lancamento
    except Exception:
        db.rollback()
        raise


def listar_lancamentos_service(db: Session, empresa_id: int):
    return listar_lancamentos(db, empresa_id)


def buscar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int,
):
    lancamento = buscar_lancamento_por_id(db, lancamento_id, empresa_id)
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lancamento nao encontrado")
    return lancamento


def atualizar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int,
    dados: LancamentoFinanceiroUpdate,
):
    lancamento = buscar_lancamento_por_id(db, lancamento_id, empresa_id)
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lancamento nao encontrado")
    if lancamento.origem_tipo is not None:
        raise HTTPException(
            status_code=409,
            detail="Lancamento automatico nao pode ser editado",
        )

    dados_dict = dados.model_dump(exclude_unset=True)
    if dados_dict.get("categoria_id") is not None:
        categoria = buscar_categoria_por_id(
            db, dados_dict["categoria_id"], empresa_id
        )
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria nao encontrada")

    try:
        lancamento = atualizar_lancamento(db, lancamento, dados_dict)
        db.commit()
        db.refresh(lancamento)
        return lancamento
    except Exception:
        db.rollback()
        raise


def deletar_lancamento_service(
    db: Session,
    lancamento_id: int,
    empresa_id: int,
):
    lancamento = buscar_lancamento_por_id(db, lancamento_id, empresa_id)
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lancamento nao encontrado")
    if lancamento.origem_tipo is not None:
        raise HTTPException(
            status_code=409,
            detail="Lancamento automatico nao pode ser removido",
        )
    try:
        lancamento = deletar_lancamento(db, lancamento)
        db.commit()
        return lancamento
    except Exception:
        db.rollback()
        raise
