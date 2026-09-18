from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import HTTPException

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


def criar_recurso_service(db: Session, dados, empresa_id: int):
    nome = _texto_obrigatorio(dados.nome, "nome")
    tipo = _texto_obrigatorio(dados.tipo, "tipo").upper()
    try:
        recurso = criar_recurso(db, empresa_id, nome, tipo)
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
):
    return listar_recursos(
        db,
        empresa_id,
        tipo.strip().upper() if tipo else None,
        ativo,
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
