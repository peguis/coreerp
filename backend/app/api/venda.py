from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.venda import (
    VendaCreate,
    VendaResponse
)

from app.services.venda import (
    criar_venda_service,
    listar_vendas_service,
    buscar_venda_service,
    atualizar_venda_service,
    deletar_venda_service
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"]
)



@router.post(
    "/",
    response_model=VendaResponse
)
def criar_venda_endpoint(
    venda: VendaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    resultado = criar_venda_service(
        db,
        venda,
        usuario
    )

    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar venda. Produto inexistente ou estoque insuficiente"
        )

    return resultado


@router.get(
    "/",
    response_model=list[VendaResponse]
)
def listar_vendas_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    return listar_vendas_service(
        db,
        usuario
    )


@router.get(
    "/{venda_id}",
    response_model=VendaResponse
)
def buscar_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    venda = buscar_venda_service(
        db,
        venda_id,
        usuario
    )

    if not venda:
        raise HTTPException(
            status_code=404,
            detail="Venda não encontrada"
        )

    return venda


@router.put(
    "/{venda_id}"
)
def editar_venda(
    venda_id: int,
    dados: dict,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    venda = atualizar_venda_service(
        db,
        venda_id,
        dados,
        usuario
    )

    if not venda:
        raise HTTPException(
            status_code=404,
            detail="Venda não encontrada"
        )

    return venda


@router.delete(
    "/{venda_id}"
)
def remover_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    sucesso = deletar_venda_service(
        db,
        venda_id,
        usuario
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Venda não encontrada"
        )

    return {
        "mensagem": "Venda removida"
    }