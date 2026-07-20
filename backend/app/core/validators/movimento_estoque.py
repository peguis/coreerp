from fastapi import HTTPException


def validar_movimento(
    quantidade,
    tipo
):

    if quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantidade deve ser maior que zero."
        )


    tipos_validos = [
        "ENTRADA",
        "SAIDA",
        "AJUSTE"
    ]


    if tipo.upper() not in tipos_validos:
        raise HTTPException(
            status_code=400,
            detail="Tipo de movimento inválido."
        )


    return True