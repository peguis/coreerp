from app.repositories.cliente import (
    criar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    deletar_cliente
)

from app.core.validators.cliente import validar_cliente



def criar_cliente_service(
    db,
    cliente,
    empresa_id
):

    validar_cliente(
        cliente.nome,
        cliente.email,
        cliente.telefone
    )


    return criar_cliente(
        db,
        cliente,
        empresa_id
    )



def listar_clientes_service(
    db,
    empresa_id
):

    return listar_clientes(
        db,
        empresa_id
    )



def buscar_cliente_service(
    db,
    cliente_id,
    empresa_id
):

    return buscar_cliente_por_id(
        db,
        cliente_id,
        empresa_id
    )



def atualizar_cliente_service(
    db,
    cliente_id,
    dados,
    empresa_id
):

    cliente = buscar_cliente_por_id(
        db,
        cliente_id,
        empresa_id
    )


    if not cliente:

        return None



    campos_permitidos = [

        "nome",
        "email",
        "telefone",
        "cpf_cnpj",
        "ativo"

    ]



    dados_filtrados = {

        campo: valor

        for campo, valor in dados.items()

        if campo in campos_permitidos

    }



    if (
        "nome" in dados_filtrados
        or "email" in dados_filtrados
        or "telefone" in dados_filtrados
    ):

        validar_cliente(

            dados_filtrados.get(
                "nome",
                cliente.nome
            ),

            dados_filtrados.get(
                "email",
                cliente.email
            ),

            dados_filtrados.get(
                "telefone",
                cliente.telefone
            )

        )



    return atualizar_cliente(
        db,
        cliente,
        dados_filtrados
    )



def deletar_cliente_service(
    db,
    cliente_id,
    empresa_id
):

    cliente = buscar_cliente_por_id(
        db,
        cliente_id,
        empresa_id
    )


    if not cliente:

        return False



    deletar_cliente(
        db,
        cliente
    )


    return True