from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate


def criar_produto(
    db: Session,
    produto: ProdutoCreate,
    empresa_id: int
):

    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque,
        empresa_id=empresa_id
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


def listar_produtos(
    db: Session,
    empresa_id: int
):
    return db.query(Produto).filter(
        Produto.empresa_id == empresa_id
    ).all()


def buscar_produto_por_id(
    db: Session,
    produto_id: int,
    empresa_id: int
):
    return db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.empresa_id == empresa_id
    ).first()


def atualizar_produto(
    db: Session,
    produto_db,
    dados
):
    for campo, valor in dados.items():
        setattr(produto_db, campo, valor)

    db.commit()
    db.refresh(produto_db)

    return produto_db


def deletar_produto(
    db: Session,
    produto_db
):
    db.delete(produto_db)
    db.commit()