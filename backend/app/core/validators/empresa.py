from fastapi import HTTPException


def validar_empresa(empresa):

    if len(empresa.nome.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Nome da empresa deve possuir no mínimo 3 caracteres."
        )

    return True