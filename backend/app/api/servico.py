from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_modulo, require_perfil
from app.database import get_db
from app.schemas.servico import (
    ServicoCreate,
    ServicoResponse,
    ServicoUpdate,
)
from app.services.servico import (
    atualizar_servico_service,
    buscar_servico_service,
    criar_servico_service,
    deletar_servico_service,
    excluir_servico_service,
    listar_servicos_service,
)


router = APIRouter(
    prefix="/servicos",
    tags=["Servicos"],
    dependencies=[Depends(require_modulo("servicos"))],
)


@router.post(
    "/",
    response_model=ServicoResponse,
)
def criar_servico_endpoint(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return criar_servico_service(db, servico, usuario.empresa_id)


@router.get(
    "/",
    response_model=list[ServicoResponse],
)
def listar_servicos_endpoint(
    busca: str | None = Query(None),
    ativo: bool | None = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_servicos_service(
        db,
        usuario.empresa_id,
        busca,
        ativo,
        pagina,
        limite,
    )


@router.get(
    "/{servico_id}",
    response_model=ServicoResponse,
)
def buscar_servico_endpoint(
    servico_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    servico = buscar_servico_service(
        db,
        servico_id,
        usuario.empresa_id,
    )
    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Servico nao encontrado.",
        )
    return servico


@router.put(
    "/{servico_id}",
    response_model=ServicoResponse,
)
def atualizar_servico_endpoint(
    servico_id: int,
    dados: ServicoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return atualizar_servico_service(
        db,
        servico_id,
        dados,
        usuario.empresa_id,
    )


@router.delete(
    "/{servico_id}",
)
def deletar_servico_endpoint(
    servico_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin")),
):
    deletar_servico_service(
        db,
        servico_id,
        usuario.empresa_id,
    )
    return {"mensagem": "Servico desativado."}


@router.delete(
    "/{servico_id}/permanente",
)
def excluir_servico_endpoint(
    servico_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return excluir_servico_service(db, servico_id, usuario.empresa_id)
