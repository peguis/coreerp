from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.venda import Venda

from sqlalchemy import func


def buscar_dashboard_service(
    db,
    usuario
):

    total_produtos = db.query(
        Produto
    ).filter(
        Produto.empresa_id == usuario.empresa_id
    ).count()


    total_clientes = db.query(
        Cliente
    ).filter(
        Cliente.empresa_id == usuario.empresa_id
    ).count()


    estoque_baixo = db.query(
        Produto
    ).filter(
        Produto.empresa_id == usuario.empresa_id,
        Produto.estoque <= 5
    ).count()


    total_vendas = db.query(
        Venda
    ).filter(
        Venda.empresa_id == usuario.empresa_id
    ).count()


    faturamento = db.query(
        func.sum(Venda.total)
    ).filter(
        Venda.empresa_id == usuario.empresa_id
    ).scalar()


    return {
        "total_produtos": total_produtos,
        "total_clientes": total_clientes,
        "estoque_baixo": estoque_baixo,
        "total_vendas": total_vendas,
        "faturamento": faturamento or 0
    }