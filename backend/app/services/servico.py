from decimal import Decimal, InvalidOperation

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.servico import (
    atualizar_servico,
    buscar_servico_por_id,
    criar_servico,
    desativar_servico,
    listar_servicos,
)


def _validar_nome(nome: str | None) -> str:
    if not isinstance(nome, str):
        raise HTTPException(
            status_code=400,
            detail="O nome do servico e obrigatorio.",
        )

    nome_normalizado = nome.strip()
    if not nome_normalizado:
        raise HTTPException(
            status_code=400,
            detail="O nome do servico nao pode ser vazio.",
        )

    return nome_normalizado


def _validar_preco(preco) -> None:
    try:
        valor = Decimal(str(preco))
    except (InvalidOperation, TypeError, ValueError):
        valor = None

    if valor is None or not valor.is_finite() or valor < 0:
        raise HTTPException(
            status_code=400,
            detail="O preco_padrao nao pode ser negativo.",
        )


def criar_servico_service(
    db: Session,
    servico,
    empresa_id: int,
):
    servico.nome = _validar_nome(servico.nome)
    _validar_preco(servico.preco_padrao)

    try:
        novo_servico = criar_servico(db, servico, empresa_id)
        db.commit()
        db.refresh(novo_servico)
        return novo_servico
    except Exception:
        db.rollback()
        raise


def listar_servicos_service(
    db: Session,
    empresa_id: int,
    busca: str | None = None,
    ativo: bool | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    if pagina < 1 or limite < 1:
        raise HTTPException(
            status_code=400,
            detail="Pagina e limite devem ser maiores que zero.",
        )

    return listar_servicos(
        db,
        empresa_id,
        busca.strip() if busca else None,
        ativo,
        pagina,
        limite,
    )


def buscar_servico_service(
    db: Session,
    servico_id: int,
    empresa_id: int,
):
    return buscar_servico_por_id(db, servico_id, empresa_id)


def atualizar_servico_service(
    db: Session,
    servico_id: int,
    dados,
    empresa_id: int,
):
    servico_db = buscar_servico_por_id(db, servico_id, empresa_id)
    if not servico_db:
        raise HTTPException(
            status_code=404,
            detail="Servico nao encontrado.",
        )

    if hasattr(dados, "model_dump"):
        dados_dict = dados.model_dump(exclude_unset=True)
    else:
        dados_dict = dict(dados)

    if "nome" in dados_dict:
        dados_dict["nome"] = _validar_nome(dados_dict["nome"])

    if "preco_padrao" in dados_dict:
        _validar_preco(dados_dict["preco_padrao"])

    try:
        servico_atualizado = atualizar_servico(
            db,
            servico_db,
            dados_dict,
        )
        db.commit()
        db.refresh(servico_atualizado)
        return servico_atualizado
    except Exception:
        db.rollback()
        raise


def deletar_servico_service(
    db: Session,
    servico_id: int,
    empresa_id: int,
):
    servico_db = buscar_servico_por_id(db, servico_id, empresa_id)
    if not servico_db:
        raise HTTPException(
            status_code=404,
            detail="Servico nao encontrado.",
        )

    try:
        servico_desativado = desativar_servico(db, servico_db)
        db.commit()
        db.refresh(servico_desativado)
        return servico_desativado
    except Exception:
        db.rollback()
        raise
