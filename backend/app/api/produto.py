from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import Query

import os
import shutil
import uuid


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


from app.auth.dependencies import get_current_user


from app.models.produto import Produto
from app.models.produto_imagem import ProdutoImagem



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
    busca: str | None = Query(None),
    categoria: str | None = Query(None),
    pagina: int = Query(1),
    limite: int = Query(10),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    return listar_produtos_service(
        db,
        usuario,
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




# =================================================
# UPLOAD IMAGEM PRODUTO
# =================================================


@router.post("/{produto_id}/imagem")
def upload_imagem_produto(
    produto_id: int,
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):


    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.empresa_id == usuario.empresa_id
    ).first()



    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )



    pasta = "uploads/produtos"


    os.makedirs(
        pasta,
        exist_ok=True
    )



    nome_arquivo = f"{uuid.uuid4()}.jpg"


    caminho = f"{pasta}/{nome_arquivo}"



    with open(caminho, "wb") as buffer:

        shutil.copyfileobj(
            arquivo.file,
            buffer
        )



    imagens_existentes = db.query(ProdutoImagem).filter(
        ProdutoImagem.produto_id == produto_id,
        ProdutoImagem.empresa_id == usuario.empresa_id
    ).all()



    # remove principal anterior

    for imagem in imagens_existentes:

        imagem.principal = False



    nova_imagem = ProdutoImagem(

        empresa_id=usuario.empresa_id,

        produto_id=produto_id,

        nome_arquivo=nome_arquivo,

        caminho=caminho,

        principal=True

    )



    db.add(nova_imagem)


    db.commit()


    db.refresh(nova_imagem)



    return nova_imagem

@router.get("/{produto_id}/imagens")
def listar_imagens_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    imagens = db.query(ProdutoImagem).filter(
        ProdutoImagem.produto_id == produto_id,
        ProdutoImagem.empresa_id == usuario.empresa_id
    ).all()


    return imagens

