from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse

from app.services.produto import (
    criar_produto_service,
    listar_produtos_service,
    buscar_produto_service,
    atualizar_produto_service,
    deletar_produto_service
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post(
    "/",
    response_model=ProdutoResponse
)
def criar_produto_endpoint(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return criar_produto_service(
        db,
        produto,
        usuario
    )


@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar_produtos_endpoint(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_produtos_service(
        db,
        usuario
    )


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    produto = buscar_produto_service(
        db,
        produto_id,
        usuario
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto



@router.put("/{produto_id}")
def editar_produto(
    produto_id: int,
    dados: dict,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    produto = atualizar_produto_service(
        db,
        produto_id,
        dados,
        usuario
    )


    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto



@router.delete("/{produto_id}")
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    sucesso = deletar_produto_service(
        db,
        produto_id,
        usuario
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return {
        "mensagem": "Produto removido"
    }