from fastapi import HTTPException
import re


def validar_cliente(
    nome,
    email=None,
    telefone=None
):

    if len(nome.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Nome do cliente deve ter no mínimo 3 caracteres."
        )


    if email:

        formato_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(formato_email, email):
            raise HTTPException(
                status_code=400,
                detail="E-mail inválido."
            )


    if telefone:

        somente_numeros = re.sub(
            r"\D",
            "",
            telefone
        )

        if len(somente_numeros) < 10:
            raise HTTPException(
                status_code=400,
                detail="Telefone inválido."
            )


    return True