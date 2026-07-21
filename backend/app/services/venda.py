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


from app.core.validators.venda import validar_venda



STATUS_VALIDOS = [
    "ABERTA",
    "SEPARACAO",
    "FATURADA",
    "PAGA",
    "CANCELADA"
]




def criar_venda_service(
    db,
    dados,
    usuario
):


    total = 0

    itens = []



    cliente = db.query(Cliente).filter(

        Cliente.id == dados.cliente_id,

        Cliente.empresa_id == usuario.empresa_id

    ).first()



    if not cliente:

        return None





    for item in dados.itens:


        # compatibilidade caso venha como dict ou objeto Pydantic
        if isinstance(item, dict):

            produto_id = item["produto_id"]
            quantidade = item["quantidade"]

        else:

            produto_id = item.produto_id
            quantidade = item.quantidade





        produto = db.query(Produto).filter(

            Produto.id == produto_id,

            Produto.empresa_id == usuario.empresa_id

        ).first()



        if not produto:

            return None





        if produto.estoque < quantidade:

            return None





        subtotal = produto.preco * quantidade


        total += subtotal





        produto.estoque -= quantidade





        novo_item = ItemVenda(

            empresa_id=usuario.empresa_id,

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

        empresa_id=usuario.empresa_id,

        cliente_id=dados.cliente_id,

        usuario_id=usuario.id,

        total=total,

        status="ABERTA"

    )





    db.add(venda)

    db.commit()

    db.refresh(venda)







    for item in itens:


        item.venda_id = venda.id

        db.add(item)







    for item in itens:



        movimento = MovimentoEstoque(

            empresa_id=usuario.empresa_id,

            produto_id=item.produto_id,

            usuario_id=usuario.id,

            tipo="SAIDA",

            quantidade=item.quantidade,

            observacao=f"Venda #{venda.id}"

        )


        db.add(movimento)







    db.commit()

    db.refresh(venda)



    return venda







def listar_vendas_service(
    db,
    usuario
):

    return listar_vendas(

        db,

        usuario.empresa_id

    )







def buscar_venda_service(
    db,
    venda_id,
    usuario
):

    return buscar_venda_por_id(

        db,

        venda_id,

        usuario.empresa_id

    )







def atualizar_venda_service(
    db,
    venda_id,
    dados,
    usuario
):


    venda = buscar_venda_por_id(

        db,

        venda_id,

        usuario.empresa_id

    )



    if not venda:

        return None





    from app.core.validators.venda import validar_status_venda



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
    usuario
):


    venda = buscar_venda_por_id(

        db,

        venda_id,

        usuario.empresa_id

    )



    if not venda:

        return False





    itens = db.query(ItemVenda).filter(

        ItemVenda.venda_id == venda.id

    ).all()






    for item in itens:



        produto = db.query(Produto).filter(

            Produto.id == item.produto_id

        ).first()



        if produto:

            produto.estoque += item.quantidade






    deletar_venda(

        db,

        venda

    )



    return True