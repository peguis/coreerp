from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.cliente import (
    ClienteCreate,
    ClienteResponse
)

from app.services.cliente import (
    criar_cliente_service,
    listar_clientes_service,
    buscar_cliente_service,
    atualizar_cliente_service,
    deletar_cliente_service
)

from app.auth.dependencies import require_perfil

from app.middleware.tenant import get_empresa_id


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post(
    "/",
    response_model=ClienteResponse
)
def criar_cliente_endpoint(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(require_perfil("admin", "gerente"))
):

    return criar_cliente_service(
        db,
        cliente,
        empresa_id
    )



@router.get(
    "/",
    response_model=list[ClienteResponse]
)
def listar_clientes_endpoint(
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id)
):

    return listar_clientes_service(
        db,
        empresa_id
    )



@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id)
):

    cliente = buscar_cliente_service(
        db,
        cliente_id,
        empresa_id
    )


    if not cliente:

        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )


    return cliente



@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def editar_cliente(
    cliente_id: int,
    dados: dict,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(require_perfil("admin", "gerente"))
):

    cliente = atualizar_cliente_service(
        db,
        cliente_id,
        dados,
        empresa_id
    )


    if not cliente:

        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )


    return cliente



@router.delete(
    "/{cliente_id}"
)
def remover_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(require_perfil("admin"))
):

    sucesso = deletar_cliente_service(
        db,
        cliente_id,
        empresa_id
    )


    if not sucesso:

        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )


    return {
        "mensagem": "Cliente removido"
    }