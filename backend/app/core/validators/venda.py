from fastapi import HTTPException


STATUS_VALIDOS = [
    "PENDENTE",
    "ABERTA",
    "SEPARACAO",
    "FATURADA",
    "PAGA",
    "CONCLUIDA",
    "FINALIZADA",
    "CANCELADA"
]


STATUS_COM_BAIXA_DE_ESTOQUE = {
    "ABERTA",
    "SEPARACAO",
    "FATURADA",
    "PAGA",
    "CONCLUIDA",
    "FINALIZADA",
}


def validar_venda(
    itens,
    valor_total,
    cliente_id
):

    if not itens:
        raise HTTPException(
            status_code=400,
            detail="A venda deve possuir ao menos um item."
        )

    for item in itens:
        quantidade = item.quantidade

        if isinstance(quantidade, bool) or not isinstance(quantidade, int):
            raise HTTPException(
                status_code=400,
                detail="Quantidade deve ser um inteiro."
            )

        if quantidade <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantidade deve ser maior que zero."
            )

    if valor_total <= 0:
        raise HTTPException(
            status_code=400,
            detail="O valor total deve ser maior que zero."
        )

    if cliente_id is None:
        raise HTTPException(
            status_code=400,
            detail="Cliente obrigatório."
        )

    return True



def validar_status_venda(status):

    if not isinstance(status, str) or status.upper() not in STATUS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Status da venda inválido."
        )

    return status.upper()


def status_baixa_estoque(status):
    """Indica se o status representa uma venda que já ocupa o estoque."""

    return status in STATUS_COM_BAIXA_DE_ESTOQUE
