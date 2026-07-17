from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse

from app.services.cliente import (
    criar_cliente_service,
    listar_clientes_service,
    buscar_cliente_service,
    atualizar_cliente_service,
    deletar_cliente_service
)

from app.auth.dependencies import get_current_user


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
    usuario=Depends(get_current_user)
):
    return criar_cliente_service(
        db,
        cliente,
        usuario
    )


@router.get(
    "/",
    response_model=list[ClienteResponse]
)
def listar_clientes_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_clientes_service(
        db,
        usuario
    )


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    cliente = buscar_cliente_service(
        db,
        cliente_id,
        usuario
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente


@router.put("/{cliente_id}")
def editar_cliente(
    cliente_id: int,
    dados: dict,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    cliente = atualizar_cliente_service(
        db,
        cliente_id,
        dados,
        usuario
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente


@router.delete("/{cliente_id}")
def remover_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    sucesso = deletar_cliente_service(
        db,
        cliente_id,
        usuario
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return {
        "mensagem": "Cliente removido"
    }