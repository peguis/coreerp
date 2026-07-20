from fastapi import HTTPException
import re


def validar_usuario(usuario):

    if len(usuario.nome.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Nome deve possuir no mínimo 3 caracteres."
        )

    email = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(email, usuario.email):
        raise HTTPException(
            status_code=400,
            detail="E-mail inválido."
        )

    if len(usuario.senha) < 6:
        raise HTTPException(
            status_code=400,
            detail="A senha deve possuir no mínimo 6 caracteres."
        )

    return True