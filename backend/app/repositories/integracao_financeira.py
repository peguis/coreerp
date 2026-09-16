from datetime import datetime
from decimal import Decimal

from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.orm import Session

from app.models.categoria_financeira import CategoriaFinanceira
from app.models.financeiro import LancamentoFinanceiro


def obter_ou_criar_categoria_sistema(
    db: Session,
    *,
    empresa_id: int,
    chave: str,
    nome: str,
    tipo: str,
) -> CategoriaFinanceira:
    categoria = (
        db.query(CategoriaFinanceira)
        .filter(
            CategoriaFinanceira.empresa_id == empresa_id,
            CategoriaFinanceira.chave_sistema == chave,
        )
        .first()
    )
    if categoria:
        categoria.nome = nome
        categoria.tipo = tipo
        categoria.ativo = True
        return categoria

    categoria_legada = (
        db.query(CategoriaFinanceira)
        .filter(
            CategoriaFinanceira.empresa_id == empresa_id,
            CategoriaFinanceira.chave_sistema.is_(None),
            CategoriaFinanceira.nome == nome,
            CategoriaFinanceira.tipo == tipo,
        )
        .order_by(CategoriaFinanceira.id.asc())
        .first()
    )
    if categoria_legada:
        categoria_legada.chave_sistema = chave
        categoria_legada.ativo = True
        db.flush()
        return categoria_legada

    if db.get_bind().dialect.name == "postgresql":
        comando = (
            postgresql_insert(CategoriaFinanceira)
            .values(
                empresa_id=empresa_id,
                nome=nome,
                tipo=tipo,
                chave_sistema=chave,
                ativo=True,
            )
            .on_conflict_do_nothing(
                index_elements=["empresa_id", "chave_sistema"],
                index_where=CategoriaFinanceira.chave_sistema.is_not(None),
            )
            .returning(CategoriaFinanceira.id)
        )
        categoria_id = db.execute(comando).scalar_one_or_none()
        if categoria_id is not None:
            return db.get(CategoriaFinanceira, categoria_id)
        return (
            db.query(CategoriaFinanceira)
            .filter(
                CategoriaFinanceira.empresa_id == empresa_id,
                CategoriaFinanceira.chave_sistema == chave,
            )
            .one()
        )

    categoria = CategoriaFinanceira(
        empresa_id=empresa_id,
        nome=nome,
        tipo=tipo,
        chave_sistema=chave,
        ativo=True,
    )
    db.add(categoria)
    db.flush()
    return categoria


def buscar_lancamento_por_origem(
    db: Session,
    *,
    empresa_id: int,
    origem_tipo: str,
    origem_id: int,
) -> LancamentoFinanceiro | None:
    return (
        db.query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.origem_tipo == origem_tipo,
            LancamentoFinanceiro.origem_id == origem_id,
        )
        .first()
    )


def criar_lancamento_automatico(
    db: Session,
    *,
    empresa_id: int,
    usuario_id: int,
    categoria_id: int,
    descricao: str,
    valor: Decimal,
    tipo: str,
    status: str,
    data_movimento: datetime,
    forma_pagamento: str,
    origem_tipo: str,
    origem_id: int,
) -> LancamentoFinanceiro:
    existente = buscar_lancamento_por_origem(
        db,
        empresa_id=empresa_id,
        origem_tipo=origem_tipo,
        origem_id=origem_id,
    )
    if existente:
        return existente

    instante = data_movimento.replace(tzinfo=None)
    lancamento = LancamentoFinanceiro(
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        categoria_id=categoria_id,
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        status=status,
        data_vencimento=data_movimento.date(),
        data_pagamento=instante,
        forma_pagamento=forma_pagamento,
        origem_tipo=origem_tipo,
        origem_id=origem_id,
    )
    db.add(lancamento)
    db.flush()
    return lancamento
