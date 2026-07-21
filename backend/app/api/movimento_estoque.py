from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.movimento_estoque import (
    MovimentoEstoqueCreate,
    MovimentoEstoqueResponse
)

from app.services.movimento_estoque import (
    criar_movimento_service,
    listar_movimentos_service,
    buscar_movimento_service
)

from app.auth.dependencies import get_current_user



router = APIRouter(
    prefix="/movimentos-estoque",
    tags=["Movimentos de Estoque"]
)



@router.post(
    "/",
    response_model=MovimentoEstoqueResponse
)
def criar_movimento_endpoint(
    movimento: MovimentoEstoqueCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    novo_movimento = criar_movimento_service(
        db,
        movimento,
        usuario
    )


    if novo_movimento is None:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    return novo_movimento





@router.get(
    "/",
    response_model=list[MovimentoEstoqueResponse]
)
def listar_movimentos_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    return listar_movimentos_service(
        db,
        usuario
    )





@router.get(
    "/{movimento_id}",
    response_model=MovimentoEstoqueResponse
)
def buscar_movimento(
    movimento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    movimento = buscar_movimento_service(
        db,
        movimento_id,
        usuario
    )


    if not movimento:

        raise HTTPException(
            status_code=404,
            detail="Movimento não encontrado"
        )


    return movimento