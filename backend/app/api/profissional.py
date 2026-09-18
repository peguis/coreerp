from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.core.enums import AreaAtuacao
from app.database import get_db
from app.schemas.profissional import (
    ProfissionalCreate,
    ProfissionalResponse,
    ProfissionalUpdate,
)
from app.services.profissional import (
    atualizar_profissional_service,
    buscar_profissional_service,
    criar_profissional_service,
    deletar_profissional_service,
    listar_profissionais_service,
)


router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais"],
)


@router.post(
    "/",
    response_model=ProfissionalResponse,
)
def criar_profissional_endpoint(
    dados: ProfissionalCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin")),
):
    return criar_profissional_service(db, dados, usuario.empresa_id)


@router.get(
    "/",
    response_model=list[ProfissionalResponse],
)
def listar_profissionais_endpoint(
    ativo: bool | None = Query(None),
    area_atuacao: AreaAtuacao | None = Query(None),
    busca: str | None = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return listar_profissionais_service(
        db,
        usuario.empresa_id,
        ativo,
        area_atuacao,
        busca,
        pagina,
        limite,
    )


@router.get(
    "/{profissional_id}",
    response_model=ProfissionalResponse,
)
def buscar_profissional_endpoint(
    profissional_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    profissional = buscar_profissional_service(
        db,
        profissional_id,
        usuario.empresa_id,
    )
    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional nao encontrado.",
        )
    return profissional


@router.put(
    "/{profissional_id}",
    response_model=ProfissionalResponse,
)
def atualizar_profissional_endpoint(
    profissional_id: int,
    dados: ProfissionalUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    if usuario.perfil == "gerente":
        campos_informados = set(dados.model_dump(exclude_unset=True))
        if campos_informados != {"area_atuacao"}:
            raise HTTPException(
                status_code=403,
                detail="Gerente pode alterar apenas a area de atuacao do profissional.",
            )

    return atualizar_profissional_service(
        db,
        profissional_id,
        dados,
        usuario.empresa_id,
    )


@router.delete("/{profissional_id}")
def deletar_profissional_endpoint(
    profissional_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin")),
):
    deletar_profissional_service(
        db,
        profissional_id,
        usuario.empresa_id,
    )
    return {"mensagem": "Profissional desativado."}
