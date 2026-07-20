from fastapi import HTTPException


STATUS_VALIDOS = [
    "ABERTA",
    "SEPARACAO",
    "FATURADA",
    "PAGA",
    "CANCELADA"
]


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

    if status.upper() not in STATUS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Status da venda inválido."
        )

    return status.upper()