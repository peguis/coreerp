from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.categoria_financeira import (
    CategoriaFinanceiraCreate,
    CategoriaFinanceiraUpdate,
    CategoriaFinanceiraResponse
)

from app.services.categoria_financeira import (
    criar_categoria_service,
    listar_categorias_service,
    buscar_categoria_service,
    atualizar_categoria_service,
    deletar_categoria_service
)

from app.auth.dependencies import get_current_user, require_perfil


router = APIRouter(
    prefix="/categorias-financeiras",
    tags=["Financeiro - Categorias"]
)



@router.post(
    "/",
    response_model=CategoriaFinanceiraResponse
)
def criar_categoria(
    dados: CategoriaFinanceiraCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente"))
):

    return criar_categoria_service(
        db,
        dados,
        usuario.empresa_id
    )



@router.get(
    "/",
    response_model=list[CategoriaFinanceiraResponse]
)
def listar_categorias(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    return listar_categorias_service(
        db,
        usuario.empresa_id
    )



@router.get(
    "/{categoria_id}",
    response_model=CategoriaFinanceiraResponse
)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    categoria = buscar_categoria_service(
        db,
        categoria_id,
        usuario.empresa_id
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return categoria



@router.put(
    "/{categoria_id}",
    response_model=CategoriaFinanceiraResponse
)
def atualizar_categoria(
    categoria_id: int,
    dados: CategoriaFinanceiraUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente"))
):

    return atualizar_categoria_service(
        db,
        categoria_id,
        usuario.empresa_id,
        dados
    )



@router.delete(
    "/{categoria_id}"
)
def deletar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin"))
):

    deletar_categoria_service(
        db,
        categoria_id,
        usuario.empresa_id
    )


    return {
        "mensagem": "Categoria removida"
    }