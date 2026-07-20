import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.models.produto_imagem import ProdutoImagem
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/produtos",
    tags=["Produto Imagens"]
)


UPLOAD_DIR = "uploads/produtos"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/{produto_id}/imagem")
def upload_imagem(
    produto_id: int,
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
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


    caminho = f"{UPLOAD_DIR}/{arquivo.filename}"


    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(
            arquivo.file,
            buffer
        )


    imagem = ProdutoImagem(
        empresa_id=usuario.empresa_id,
        produto_id=produto_id,
        nome_arquivo=arquivo.filename,
        caminho=caminho
    )


    db.add(imagem)
    db.commit()
    db.refresh(imagem)


    return imagem

@router.get("/{produto_id}/imagens")
def listar_imagens(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):

    imagens = db.query(ProdutoImagem).filter(
        ProdutoImagem.produto_id == produto_id,
        ProdutoImagem.empresa_id == usuario.empresa_id
    ).all()

    return imagens

@router.delete("/{produto_id}/imagem/{imagem_id}")
def excluir_imagem_produto(
    produto_id: int,
    imagem_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):

    imagem = db.query(ProdutoImagem).filter(
        ProdutoImagem.id == imagem_id,
        ProdutoImagem.produto_id == produto_id,
        ProdutoImagem.empresa_id == usuario.empresa_id
    ).first()


    if not imagem:
        raise HTTPException(
            status_code=404,
            detail="Imagem não encontrada"
        )


    if os.path.exists(imagem.caminho):
        os.remove(imagem.caminho)


    db.delete(imagem)

    db.commit()


    return {
        "mensagem": "Imagem removida"
    }