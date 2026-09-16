from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.produto import (
    ProdutoCreate,
    ProdutoResponse
)

from app.services.produto import (
    criar_produto_service,
    listar_produtos_service,
    buscar_produto_service,
    atualizar_produto_service,
    deletar_produto_service
)

from app.auth.dependencies import require_perfil

from app.auth.tenant import get_empresa_id

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)



@router.post(
    "/",
    response_model=ProdutoResponse
)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente"
        )
    )
):

    return criar_produto_service(
        db,
        produto,
        empresa_id,
        usuario.id
    )



@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    busca: str | None = Query(None),
    categoria: str | None = Query(None),
    pagina: int = Query(1),
    limite: int = Query(10),
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente",
            "operador",
            "consulta"
        )
    )
):

    return listar_produtos_service(
        db,
        empresa_id,
        busca,
        categoria,
        pagina,
        limite
    )



@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente",
            "operador",
            "consulta"
        )
    )
):

    produto = buscar_produto_service(
        db,
        produto_id,
        empresa_id
    )


    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    return produto



@router.put(
    "/{produto_id}"
)
def editar_produto(
    produto_id: int,
    dados: dict,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente"
        )
    )
):

    produto = atualizar_produto_service(
        db,
        produto_id,
        dados,
        empresa_id
    )


    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    return produto



@router.delete(
    "/{produto_id}"
)
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(
        require_perfil(
            "admin"
        )
    )
):

    sucesso = deletar_produto_service(
        db,
        produto_id,
        empresa_id
    )


    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    return {
        "mensagem": "Produto removido"
    }
