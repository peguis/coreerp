from sqlalchemy.orm import Session

from app.models.categoria_financeira import CategoriaFinanceira

from app.schemas.categoria_financeira import (
    CategoriaFinanceiraCreate
)



def criar_categoria(
    db: Session,
    dados: CategoriaFinanceiraCreate,
    empresa_id: int
):

    categoria = CategoriaFinanceira(

        empresa_id=empresa_id,

        nome=dados.nome,

        tipo=dados.tipo.upper(),

        ativo=True

    )


    db.add(categoria)

    db.commit()

    db.refresh(categoria)


    return categoria



def listar_categorias(
    db: Session,
    empresa_id: int
):

    return (
        db.query(CategoriaFinanceira)

        .filter(
            CategoriaFinanceira.empresa_id == empresa_id
        )

        .order_by(
            CategoriaFinanceira.nome.asc()
        )

        .all()
    )



def buscar_categoria_por_id(
    db: Session,
    categoria_id: int,
    empresa_id: int
):

    return (
        db.query(CategoriaFinanceira)

        .filter(
            CategoriaFinanceira.id == categoria_id,
            CategoriaFinanceira.empresa_id == empresa_id
        )

        .first()
    )



def atualizar_categoria(
    db: Session,
    categoria_db,
    dados: dict
):

    campos_permitidos = [

        "nome",
        "tipo",
        "ativo"

    ]


    for campo, valor in dados.items():

        if campo in campos_permitidos:


            if campo == "tipo":

                valor = valor.upper()


            setattr(
                categoria_db,
                campo,
                valor
            )


    db.commit()

    db.refresh(categoria_db)


    return categoria_db



def deletar_categoria(
    db: Session,
    categoria_db
):

    categoria_db.ativo = False


    db.commit()

    db.refresh(categoria_db)


    return categoria_db