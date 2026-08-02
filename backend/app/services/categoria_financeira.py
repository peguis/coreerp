from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.repositories.categoria_financeira import (
    criar_categoria,
    listar_categorias,
    buscar_categoria_por_id,
    atualizar_categoria,
    deletar_categoria
)

from app.schemas.categoria_financeira import (
    CategoriaFinanceiraCreate,
    CategoriaFinanceiraUpdate
)



def criar_categoria_service(
    db: Session,
    dados: CategoriaFinanceiraCreate,
    empresa_id: int
):

    return criar_categoria(
        db,
        dados,
        empresa_id
    )



def listar_categorias_service(
    db: Session,
    empresa_id: int
):

    return listar_categorias(
        db,
        empresa_id
    )



def buscar_categoria_service(
    db: Session,
    categoria_id: int,
    empresa_id: int
):

    return buscar_categoria_por_id(
        db,
        categoria_id,
        empresa_id
    )



def atualizar_categoria_service(
    db: Session,
    categoria_id: int,
    empresa_id: int,
    dados: CategoriaFinanceiraUpdate
):

    categoria = buscar_categoria_por_id(
        db,
        categoria_id,
        empresa_id
    )


    if not categoria:

        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )


    dados_dict = dados.model_dump(
        exclude_unset=True
    )


    return atualizar_categoria(
        db,
        categoria,
        dados_dict
    )



def deletar_categoria_service(
    db: Session,
    categoria_id: int,
    empresa_id: int
):

    categoria = buscar_categoria_por_id(
        db,
        categoria_id,
        empresa_id
    )


    if not categoria:

        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )


    return deletar_categoria(
        db,
        categoria
    )