from app.repositories.venda import (
    criar_venda,
    listar_vendas,
    buscar_venda_por_id,
    buscar_venda_por_chave_idempotencia,
    atualizar_venda,
    deletar_venda
)


from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.produto import Produto
from app.models.cliente import Cliente

from app.services.movimento_estoque import movimentar_estoque


from app.core.validators.venda import (
    validar_venda,
    validar_status_venda,
    status_baixa_estoque
)

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def _movimentar_itens_venda(
    db,
    venda,
    empresa_id,
    usuario_id,
    tipo
):
    """Registra a baixa/entrada de todos os itens de uma venda."""

    for item in venda.itens:
        produto = (
            db.query(Produto)
            .filter(
                Produto.id == item.produto_id,
                Produto.empresa_id == empresa_id
            )
            .first()
        )

        if not produto:
            raise HTTPException(
                status_code=400,
                detail="Produto da venda não encontrado."
            )

        movimento = movimentar_estoque(
            db=db,
            empresa_id=empresa_id,
            produto_id=item.produto_id,
            tipo=tipo,
            quantidade=item.quantidade,
            usuario_id=usuario_id,
            observacao=(
                f"Baixa da venda #{venda.id}"
                if tipo == "SAIDA"
                else f"Estorno da venda #{venda.id}"
            ),
            produto=produto
        )

        if not movimento:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível atualizar o estoque da venda."
            )



def criar_venda_service(
    db,
    dados,
    empresa_id,
    usuario_id
):

    total = 0

    itens = []

    status = validar_status_venda(
        getattr(dados, "status", "ABERTA")
    )

    baixa_estoque = status_baixa_estoque(status)

    chave_idempotencia = getattr(
        dados,
        "chave_idempotencia",
        None
    )

    if chave_idempotencia:
        existente = buscar_venda_por_chave_idempotencia(
            db,
            empresa_id,
            chave_idempotencia,
            bloquear=True
        )

        if existente:
            pedido_externo_id = getattr(
                dados,
                "pedido_externo_id",
                None
            )
            if (
                pedido_externo_id
                and existente.pedido_externo_id
                and pedido_externo_id != existente.pedido_externo_id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="A chave de idempotência já pertence a outro pedido."
                )
            return existente



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

        venda = Venda(

            empresa_id=empresa_id,

            cliente_id=dados.cliente_id,

            usuario_id=usuario_id,

            total=0,

            status=status,

            estoque_baixado=baixa_estoque,

            origem=getattr(dados, "origem", "ERP"),

            pedido_externo_id=getattr(
                dados,
                "pedido_externo_id",
                None
            ),

            chave_idempotencia=chave_idempotencia,

            observacoes=getattr(dados, "observacoes", None),

            endereco_entrega=getattr(
                dados,
                "endereco_entrega",
                None
            )

        )


        db.add(venda)

        db.flush()


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
                db.rollback()
                return None



            subtotal = produto.preco * quantidade

            total += subtotal


            if baixa_estoque:
                movimento = movimentar_estoque(
                    db=db,
                    empresa_id=empresa_id,
                    produto_id=produto_id,
                    tipo="SAIDA",
                    quantidade=quantidade,
                    usuario_id=usuario_id,
                    observacao=f"Venda #{venda.id}",
                    produto=produto
                )


                if not movimento:

                    db.rollback()

                    return None



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




        for item in itens:


            item.venda_id = venda.id

            db.add(item)







        venda.total = total

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            if chave_idempotencia:
                existente = buscar_venda_por_chave_idempotencia(
                    db,
                    empresa_id,
                    chave_idempotencia
                )
                if existente:
                    return existente
            raise

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
        empresa_id,
        bloquear=True
    )


    if not venda:
        return None



    dados = dict(dados)

    if "status" not in dados:
        return atualizar_venda(db, venda, dados)

    novo_status = validar_status_venda(dados["status"])
    status_atual = venda.status.upper()

    if status_atual == "CANCELADA" and novo_status != "CANCELADA":
        raise HTTPException(
            status_code=400,
            detail="Uma venda cancelada não pode voltar ao fluxo ativo."
        )

    if novo_status == "PENDENTE" and status_atual != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="Somente novos pedidos podem iniciar como PENDENTE."
        )

    try:
        if (
            status_baixa_estoque(novo_status)
            and not venda.estoque_baixado
        ):
            _movimentar_itens_venda(
                db=db,
                venda=venda,
                empresa_id=empresa_id,
                usuario_id=venda.usuario_id,
                tipo="SAIDA"
            )
            dados["estoque_baixado"] = True

        elif novo_status == "CANCELADA" and venda.estoque_baixado:
            _movimentar_itens_venda(
                db=db,
                venda=venda,
                empresa_id=empresa_id,
                usuario_id=venda.usuario_id,
                tipo="ENTRADA"
            )
            dados["estoque_baixado"] = False

        dados["status"] = novo_status

        return atualizar_venda(
            db,
            venda,
            dados
        )

    except Exception:
        db.rollback()
        raise







def deletar_venda_service(
    db,
    venda_id,
    empresa_id,
    usuario_id=None
):


    venda = buscar_venda_por_id(
        db,
        venda_id,
        empresa_id
    )


    if not venda:
        return False


    usuario_movimento = (
        usuario_id
        if usuario_id is not None
        else venda.usuario_id
    )


def criar_pedido_ecommerce_service(
    db,
    dados,
    empresa_id,
    usuario_id
):
    """Recebe um pedido externo sempre como pendente e sem baixa."""

    if not dados.pedido_externo_id:
        raise HTTPException(
            status_code=400,
            detail="pedido_externo_id é obrigatório na integração."
        )

    if not dados.chave_idempotencia:
        raise HTTPException(
            status_code=400,
            detail="chave_idempotencia é obrigatória na integração."
        )

    dados_pedido = dados.model_copy(
        update={
            "status": "PENDENTE",
            "origem": "ECOMMERCE"
        }
    )

    return criar_venda_service(
        db,
        dados_pedido,
        empresa_id,
        usuario_id
    )




    if venda.estoque_baixado:
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

                try:

                    movimento = movimentar_estoque(
                        db=db,
                        empresa_id=empresa_id,
                        produto_id=item.produto_id,
                        tipo="ENTRADA",
                        quantidade=item.quantidade,
                        usuario_id=usuario_movimento,
                        observacao=f"Estorno da venda #{venda.id}",
                        produto=produto
                    )


                    if not movimento:

                        db.rollback()

                        return False

                except Exception:

                    db.rollback()

                    raise


            else:

                db.rollback()

                return False




    deletar_venda(
        db,
        venda
    )


    try:

        db.commit()

    except Exception:

        db.rollback()

        raise


    return True
