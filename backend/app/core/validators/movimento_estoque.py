from fastapi import HTTPException


def validar_movimento(
    quantidade,
    tipo
):

    if isinstance(quantidade, bool) or not isinstance(quantidade, int):
        raise HTTPException(
            status_code=400,
            detail="Quantidade deve ser um inteiro."
        )


    tipos_validos = [
        "ENTRADA",
        "SAIDA",
        "AJUSTE"
    ]


    if not isinstance(tipo, str) or tipo.upper() not in tipos_validos:
        raise HTTPException(
            status_code=400,
            detail="Tipo de movimento inválido."
        )


    tipo_normalizado = tipo.upper()


    if tipo_normalizado == "AJUSTE":

        if quantidade < 0:
            raise HTTPException(
                status_code=400,
                detail="Saldo de ajuste n\u00e3o pode ser negativo."
            )

    elif quantidade <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantidade deve ser maior que zero."
        )


    return True
