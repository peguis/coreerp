from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from sqlalchemy.orm import joinedload



def criar_venda(
    db: Session,
    venda: Venda,
    itens: list[ItemVenda]
):

    db.add(venda)

    for item in itens:
        db.add(item)


    db.commit()

    db.refresh(venda)

    return venda





def listar_vendas(
    db,
    empresa_id
):

    return (

        db.query(Venda)

        .options(
            joinedload(Venda.cliente),
            joinedload(Venda.itens)
        )

        .filter(
            Venda.empresa_id == empresa_id
        )

        .all()

    )





def buscar_venda_por_id(
    db,
    venda_id,
    empresa_id
):

    return (

        db.query(Venda)

        .options(

            joinedload(Venda.cliente),
            joinedload(Venda.itens)

        )

        .filter(

            Venda.id == venda_id,

            Venda.empresa_id == empresa_id

        )

        .first()

    )





def atualizar_venda(
    db: Session,
    venda_db,
    dados
):

    campos_permitidos = [
        "status"
    ]


    for campo, valor in dados.items():

        if campo in campos_permitidos:

            setattr(
                venda_db,
                campo,
                valor
            )


    db.commit()

    db.refresh(venda_db)

    return venda_db





def deletar_venda(
    db: Session,
    venda_db
):

    db.delete(venda_db)

    db.commit()