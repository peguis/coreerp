from decimal import Decimal, InvalidOperation

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.profissional import (
    atualizar_profissional,
    buscar_profissional_por_id,
    buscar_profissional_por_usuario,
    criar_profissional,
    desativar_profissional,
    listar_profissionais,
)
from app.repositories.usuario import buscar_usuario_por_id


def _normalizar_area(area) -> str:
    if not isinstance(area, str) or not area.strip():
        raise HTTPException(
            status_code=400,
            detail="Area de atuacao obrigatoria.",
        )
    return area.strip().upper()


def _normalizar_percentual(percentual) -> Decimal:
    try:
        valor = Decimal(str(percentual))
    except (InvalidOperation, TypeError, ValueError):
        valor = None

    if (
        valor is None
        or not valor.is_finite()
        or valor < 0
        or valor > 100
    ):
        raise HTTPException(
            status_code=400,
            detail="O percentual_padrao deve estar entre 0 e 100.",
        )
    return valor


def criar_profissional_service(
    db: Session,
    dados,
    empresa_id: int,
):
    usuario = buscar_usuario_por_id(db, dados.usuario_id, empresa_id)
    if not usuario:
        raise HTTPException(
            status_code=400,
            detail="Usuario invalido para esta empresa.",
        )

    existente = buscar_profissional_por_usuario(
        db,
        dados.usuario_id,
        empresa_id,
    )
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Este usuario ja possui um profissional vinculado.",
        )

    area = _normalizar_area(dados.area_atuacao)
    percentual = _normalizar_percentual(dados.percentual_padrao)

    try:
        profissional = criar_profissional(
            db,
            empresa_id,
            dados.usuario_id,
            area,
            percentual,
        )
        db.commit()
        db.refresh(profissional)
        return profissional
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Este usuario ja possui um profissional vinculado.",
        )
    except Exception:
        db.rollback()
        raise


def listar_profissionais_service(
    db: Session,
    empresa_id: int,
    ativo: bool | None = None,
    area_atuacao=None,
    busca: str | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    if pagina < 1 or limite < 1:
        raise HTTPException(
            status_code=400,
            detail="Pagina e limite devem ser maiores que zero.",
        )

    area = _normalizar_area(area_atuacao) if area_atuacao else None
    return listar_profissionais(
        db,
        empresa_id,
        ativo,
        area,
        busca.strip() if busca else None,
        pagina,
        limite,
    )


def buscar_profissional_service(
    db: Session,
    profissional_id: int,
    empresa_id: int,
):
    return buscar_profissional_por_id(db, profissional_id, empresa_id)


def atualizar_profissional_service(
    db: Session,
    profissional_id: int,
    dados,
    empresa_id: int,
):
    profissional = buscar_profissional_por_id(
        db,
        profissional_id,
        empresa_id,
    )
    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional nao encontrado.",
        )

    if hasattr(dados, "model_dump"):
        dados_dict = dados.model_dump(exclude_unset=True)
    else:
        dados_dict = dict(dados)

    if "usuario_id" in dados_dict or "empresa_id" in dados_dict:
        raise HTTPException(
            status_code=400,
            detail="O vinculo de usuario e empresa e imutavel.",
        )

    for campo in ("area_atuacao", "percentual_padrao", "ativo"):
        if campo in dados_dict and dados_dict[campo] is None:
            raise HTTPException(
                status_code=400,
                detail="O campo informado nao pode ser nulo.",
            )

    if "area_atuacao" in dados_dict:
        dados_dict["area_atuacao"] = _normalizar_area(
            dados_dict["area_atuacao"]
        )

    if "percentual_padrao" in dados_dict:
        dados_dict["percentual_padrao"] = _normalizar_percentual(
            dados_dict["percentual_padrao"]
        )

    try:
        profissional = atualizar_profissional(db, profissional, dados_dict)
        db.commit()
        db.refresh(profissional)
        return profissional
    except Exception:
        db.rollback()
        raise


def deletar_profissional_service(
    db: Session,
    profissional_id: int,
    empresa_id: int,
):
    profissional = buscar_profissional_por_id(
        db,
        profissional_id,
        empresa_id,
    )
    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional nao encontrado.",
        )

    try:
        profissional = desativar_profissional(db, profissional)
        db.commit()
        db.refresh(profissional)
        return profissional
    except Exception:
        db.rollback()
        raise
