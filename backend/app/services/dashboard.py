from sqlalchemy import func, desc, extract

from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.financeiro import LancamentoFinanceiro



def buscar_dashboard_service(db, usuario):

    empresa_id = usuario.empresa_id



    total_produtos = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id
        )
        .count()
    )



    total_clientes = (
        db.query(Cliente)
        .filter(
            Cliente.empresa_id == empresa_id
        )
        .count()
    )



    estoque_baixo = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.estoque <= Produto.estoque_minimo
        )
        .count()
    )



    total_vendas = (
        db.query(Venda)
        .filter(
            Venda.empresa_id == empresa_id
        )
        .count()
    )



    faturamento = (
        db.query(
            func.coalesce(
                func.sum(Venda.total),
                0
            )
        )
        .filter(
            Venda.empresa_id == empresa_id
        )
        .scalar()
    )





    # FINANCEIRO


    total_receber = (
        db.query(
            func.coalesce(
                func.sum(LancamentoFinanceiro.valor),
                0
            )
        )
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.status == "PENDENTE"
        )
        .scalar()
    )



    total_pagar = (
        db.query(
            func.coalesce(
                func.sum(LancamentoFinanceiro.valor),
                0
            )
        )
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.tipo == "DESPESA",
            LancamentoFinanceiro.status == "PENDENTE"
        )
        .scalar()
    )



    receitas_recebidas = (
        db.query(
            func.coalesce(
                func.sum(LancamentoFinanceiro.valor),
                0
            )
        )
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.status == "RECEBIDO"
        )
        .scalar()
    )



    despesas_pagas = (
        db.query(
            func.coalesce(
                func.sum(LancamentoFinanceiro.valor),
                0
            )
        )
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.tipo == "DESPESA",
            LancamentoFinanceiro.status == "PAGO"
        )
        .scalar()
    )



    saldo_financeiro = (
        receitas_recebidas or 0
    ) - (
        despesas_pagas or 0
    )







    # VENDAS RECENTES


    ultimas_vendas = (
        db.query(Venda)
        .filter(
            Venda.empresa_id == empresa_id
        )
        .order_by(
            desc(Venda.created_at)
        )
        .limit(5)
        .all()
    )







    # ESTOQUE BAIXO


    produtos_baixo_estoque = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.estoque <= Produto.estoque_minimo
        )
        .limit(5)
        .all()
    )







    # PRODUTOS SEM GIRO


    produtos_sem_giro = (
        db.query(Produto)
        .outerjoin(
            ItemVenda,
            Produto.id == ItemVenda.produto_id
        )
        .filter(
            Produto.empresa_id == empresa_id
        )
        .group_by(
            Produto.id
        )
        .having(
            func.count(ItemVenda.id) == 0
        )
        .limit(5)
        .all()
    )







    # ESTOQUE PARADO


    estoque_parado = (
        db.query(Produto)
        .outerjoin(
            ItemVenda,
            Produto.id == ItemVenda.produto_id
        )
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.estoque > 10
        )
        .group_by(
            Produto.id
        )
        .having(
            func.count(ItemVenda.id) == 0
        )
        .limit(5)
        .all()
    )








    # VENDAS POR MÊS


    vendas_por_mes_query = (
        db.query(
            extract(
                "month",
                Venda.created_at
            ).label("mes"),
            func.sum(
                Venda.total
            ).label("valor")
        )
        .filter(
            Venda.empresa_id == empresa_id
        )
        .group_by(
            extract(
                "month",
                Venda.created_at
            )
        )
        .order_by(
            extract(
                "month",
                Venda.created_at
            )
        )
        .all()
    )



    meses = [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez"
    ]



    vendas_por_mes = [

        {
            "mes": meses[int(item.mes) - 1],
            "valor": float(item.valor)
        }

        for item in vendas_por_mes_query

    ]








    # PRODUTOS MAIS VENDIDOS


    produtos_mais_vendidos = (
        db.query(
            Produto.nome,
            func.sum(
                ItemVenda.quantidade
            ).label("quantidade")
        )
        .join(
            ItemVenda,
            Produto.id == ItemVenda.produto_id
        )
        .filter(
            Produto.empresa_id == empresa_id
        )
        .group_by(
            Produto.nome
        )
        .order_by(
            desc("quantidade")
        )
        .limit(5)
        .all()
    )







    # CLIENTES TOP


    clientes_top = (
        db.query(
            Cliente.nome,
            func.sum(
                Venda.total
            ).label("valor")
        )
        .join(
            Venda,
            Cliente.id == Venda.cliente_id
        )
        .filter(
            Cliente.empresa_id == empresa_id
        )
        .group_by(
            Cliente.nome
        )
        .order_by(
            desc("valor")
        )
        .limit(5)
        .all()
    )







    # ALERTAS


    produtos_zerados = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.estoque == 0
        )
        .limit(5)
        .all()
    )



    produtos_criticos = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.estoque > 0,
            Produto.estoque <= Produto.estoque_minimo
        )
        .limit(5)
        .all()
    )



    contas_pendentes = (
        db.query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.status == "PENDENTE"
        )
        .limit(5)
        .all()
    )






    return {


        "total_produtos": total_produtos,

        "total_clientes": total_clientes,

        "estoque_baixo": estoque_baixo,

        "total_vendas": total_vendas,


        "faturamento": float(
            faturamento or 0
        ),




        "financeiro": {

            "total_receber": float(total_receber or 0),

            "total_pagar": float(total_pagar or 0),

            "receitas_recebidas": float(receitas_recebidas or 0),

            "despesas_pagas": float(despesas_pagas or 0),

            "saldo": float(saldo_financeiro or 0)

        },




        "ultimas_vendas": [

            {
                "id": venda.id,
                "cliente": venda.cliente.nome if venda.cliente else None,
                "total": float(venda.total),
                "status": venda.status,
                "data": venda.created_at
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

        ],




        "produtos_sem_giro": [

            {
                "id": produto.id,
                "nome": produto.nome,
                "estoque": produto.estoque
            }

            for produto in produtos_sem_giro

        ],




        "estoque_parado": [

            {
                "id": produto.id,
                "nome": produto.nome,
                "estoque": produto.estoque
            }

            for produto in estoque_parado

        ],




        "vendas_por_mes": vendas_por_mes,




        "produtos_mais_vendidos": [

            {
                "nome": produto.nome,
                "quantidade": int(produto.quantidade)
            }

            for produto in produtos_mais_vendidos

        ],




        "clientes_top": [

            {
                "nome": cliente.nome,
                "valor": float(cliente.valor)
            }

            for cliente in clientes_top

        ],




        "alertas": {


            "produtos_zerados": [

                {
                    "id": produto.id,
                    "nome": produto.nome
                }

                for produto in produtos_zerados

            ],



            "produtos_criticos": [

                {
                    "id": produto.id,
                    "nome": produto.nome,
                    "estoque": produto.estoque
                }

                for produto in produtos_criticos

            ],



            "contas_pendentes": [

                {
                    "id": conta.id,
                    "descricao": getattr(
                        conta,
                        "descricao",
                        "Conta financeira"
                    ),
                    "valor": float(conta.valor)
                }

                for conta in contas_pendentes

            ]

        }

    }