from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate


def criar_produto(
    db: Session,
    produto: ProdutoCreate,
    empresa_id: int
):

    novo_produto = Produto(
    empresa_id=empresa_id,

    nome=produto.nome,
    categoria=produto.categoria,
    codigo_interno=produto.codigo_interno,
    codigo_barras=produto.codigo_barras,
    marca=produto.marca,
    unidade=produto.unidade,
    descricao=produto.descricao,

    preco=produto.preco,
    estoque=produto.estoque,

    estoque_minimo=produto.estoque_minimo,
    estoque_maximo=produto.estoque_maximo,

    peso=produto.peso,
    altura=produto.altura,
    largura=produto.largura,
    comprimento=produto.comprimento,

    localizacao=produto.localizacao,

    custo_medio=produto.custo_medio
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto

def listar_produtos(
    db: Session,
    empresa_id: int,
    busca=None,
    categoria=None,
    pagina=1,
    limite=10
):

    query = db.query(Produto).filter(
        Produto.empresa_id == empresa_id,
        Produto.ativo == True
    )


    if busca:
        query = query.filter(
            Produto.nome.ilike(f"%{busca}%")
        )


    if categoria:
        query = query.filter(
            Produto.categoria == categoria
        )


    produtos = query.offset(
        (pagina - 1) * limite
    ).limit(
        limite
    ).all()


    return produtos

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
    produto_db.ativo = False

    db.commit()

    db.refresh(produto_db)

    return produto_db