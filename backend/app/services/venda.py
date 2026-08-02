from app.repositories.venda import (
    criar_venda,
    listar_vendas,
    buscar_venda_por_id,
    atualizar_venda,
    deletar_venda
)


from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.movimento_estoque import MovimentoEstoque


from app.core.validators.venda import (
    validar_venda,
    validar_status_venda
)



def criar_venda_service(
    db,
    dados,
    empresa_id,
    usuario_id
):

    total = 0

    itens = []



    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == dados.cliente_id,
            Cliente.empresa_id == empresa_id
        )
        .first()
    )


    if not cliente:
        return None



    try:


        for item in dados.itens:


            if isinstance(item, dict):

                produto_id = item["produto_id"]
                quantidade = item["quantidade"]

            else:

                produto_id = item.produto_id
                quantidade = item.quantidade




            produto = (
                db.query(Produto)
                .filter(
                    Produto.id == produto_id,
                    Produto.empresa_id == empresa_id
                )
                .first()
            )


            if not produto:
                return None



            if produto.estoque < quantidade:
                return None



            subtotal = produto.preco * quantidade

            total += subtotal


            produto.estoque -= quantidade



            novo_item = ItemVenda(

                empresa_id=empresa_id,

                produto_id=produto_id,

                quantidade=quantidade,

                preco_unitario=produto.preco,

                subtotal=subtotal

            )


            itens.append(novo_item)




        validar_venda(
            itens=itens,
            valor_total=total,
            cliente_id=dados.cliente_id
        )




        venda = Venda(

            empresa_id=empresa_id,

            cliente_id=dados.cliente_id,

            usuario_id=usuario_id,

            total=total,

            status="ABERTA"

        )



        db.add(venda)

        db.flush()




        for item in itens:


            item.venda_id = venda.id

            db.add(item)



            movimento = MovimentoEstoque(

                empresa_id=empresa_id,

                produto_id=item.produto_id,

                usuario_id=usuario_id,

                tipo="SAIDA",

                quantidade=item.quantidade,

                observacao=f"Venda #{venda.id}"

            )


            db.add(movimento)




        db.commit()

        db.refresh(venda)


        return venda




    except Exception:

        db.rollback()

        raise






def listar_vendas_service(
    db,
    empresa_id
):

    return listar_vendas(
        db,
        empresa_id
    )






def buscar_venda_service(
    db,
    venda_id,
    empresa_id
):

    return buscar_venda_por_id(
        db,
        venda_id,
        empresa_id
    )







def atualizar_venda_service(
    db,
    venda_id,
    dados,
    empresa_id
):

    venda = buscar_venda_por_id(
        db,
        venda_id,
        empresa_id
    )


    if not venda:
        return None



    if "status" in dados:

        dados["status"] = validar_status_venda(
            dados["status"]
        )



    return atualizar_venda(
        db,
        venda,
        dados
    )







def deletar_venda_service(
    db,
    venda_id,
    empresa_id
):


    venda = buscar_venda_por_id(
        db,
        venda_id,
        empresa_id
    )


    if not venda:
        return False




    for item in venda.itens:


        produto = (
            db.query(Produto)
            .filter(
                Produto.id == item.produto_id,
                Produto.empresa_id == empresa_id
            )
            .first()
        )


        if produto:

            produto.estoque += item.quantidade




    deletar_venda(
        db,
        venda
    )


    return True