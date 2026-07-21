from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.venda import Venda

from sqlalchemy import func, desc


def buscar_dashboard_service(
    db,
    usuario
):

    empresa_id = usuario.empresa_id


    total_produtos = db.query(
        Produto
    ).filter(
        Produto.empresa_id == empresa_id
    ).count()



    total_clientes = db.query(
        Cliente
    ).filter(
        Cliente.empresa_id == empresa_id
    ).count()



    estoque_baixo = db.query(
        Produto
    ).filter(
        Produto.empresa_id == empresa_id,
        Produto.estoque <= Produto.estoque_minimo
    ).count()



    total_vendas = db.query(
        Venda
    ).filter(
        Venda.empresa_id == empresa_id
    ).count()



    faturamento = db.query(
        func.sum(Venda.total)
    ).filter(
        Venda.empresa_id == empresa_id
    ).scalar()



    ultimas_vendas = db.query(
        Venda
    ).filter(
        Venda.empresa_id == empresa_id
    ).order_by(
        desc(Venda.id)
    ).limit(5).all()



    produtos_baixo_estoque = db.query(
        Produto
    ).filter(
        Produto.empresa_id == empresa_id,
        Produto.estoque <= Produto.estoque_minimo
    ).limit(5).all()



    return {

        "total_produtos": total_produtos,

        "total_clientes": total_clientes,

        "estoque_baixo": estoque_baixo,

        "total_vendas": total_vendas,

        "faturamento": faturamento or 0,


        "ultimas_vendas": [
            {
                "id": venda.id,
                "total": venda.total,
                "status": venda.status
            }
            for venda in ultimas_vendas
        ],


        "produtos_baixo_estoque": [
            {
                "id": produto.id,
                "nome": produto.nome,
                "estoque": produto.estoque,
                "minimo": produto.estoque_minimo
            }
            for produto in produtos_baixo_estoque
        ]

    }