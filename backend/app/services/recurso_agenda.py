from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.core.enums import StatusRecursoAgenda
from app.repositories.recurso_agenda import (
    atualizar_recurso,
    buscar_recurso_por_id,
    criar_recurso,
    listar_recursos,
)


def _texto_obrigatorio(valor, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise HTTPException(
            status_code=400,
            detail=f"O campo {campo} e obrigatorio.",
        )
    return valor.strip()


def _normalizar_status(status=None, ativo=None) -> str:
    if status is None:
        return (
            StatusRecursoAgenda.ATIVO.value
            if ativo is not False
            else StatusRecursoAgenda.INATIVO.value
        )
    try:
        return StatusRecursoAgenda(status).value
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Status de recurso invalido.")


def criar_recurso_service(db: Session, dados, empresa_id: int):
    nome = _texto_obrigatorio(dados.nome, "nome")
    tipo = _texto_obrigatorio(dados.tipo, "tipo").upper()
    status = _normalizar_status(dados.status)
    try:
        recurso = criar_recurso(db, empresa_id, nome, tipo, status)
        db.commit()
        db.refresh(recurso)
        return recurso
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ja existe um recurso com este nome nesta empresa.",
        )


def listar_recursos_service(
    db: Session,
    empresa_id: int,
    tipo: str | None = None,
    ativo: bool | None = None,
    status: str | None = None,
):
    status_normalizado = _normalizar_status(status) if status else None
    return listar_recursos(
        db,
        empresa_id,
        tipo.strip().upper() if tipo else None,
        ativo,
        status_normalizado,
    )


def atualizar_recurso_service(
    db: Session,
    recurso_id: int,
    dados,
    empresa_id: int,
):
    recurso = buscar_recurso_por_id(db, recurso_id, empresa_id)
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso nao encontrado.")

    dados_dict = dados.model_dump(exclude_unset=True)
    if "nome" in dados_dict:
        dados_dict["nome"] = _texto_obrigatorio(dados_dict["nome"], "nome")
    if "tipo" in dados_dict:
        dados_dict["tipo"] = _texto_obrigatorio(
            dados_dict["tipo"], "tipo"
        ).upper()
    if "status" in dados_dict:
        dados_dict["status"] = _normalizar_status(dados_dict["status"])
        dados_dict["ativo"] = dados_dict["status"] == StatusRecursoAgenda.ATIVO.value
    elif "ativo" in dados_dict:
        dados_dict["status"] = _normalizar_status(ativo=dados_dict["ativo"])

    try:
        recurso = atualizar_recurso(db, recurso, dados_dict)
        db.commit()
        db.refresh(recurso)
        return recurso
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ja existe um recurso com este nome nesta empresa.",
        )


def desativar_recurso_service(
    db: Session,
    recurso_id: int,
    empresa_id: int,
):
    recurso = buscar_recurso_por_id(db, recurso_id, empresa_id)
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso nao encontrado.")
    recurso.status = StatusRecursoAgenda.INATIVO.value
    recurso.ativo = False
    db.commit()
    db.refresh(recurso)
    return recurso
