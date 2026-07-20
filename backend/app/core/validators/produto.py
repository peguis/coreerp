from fastapi import HTTPException


def validar_produto(produto):

    if len(produto.nome.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Nome do produto deve ter no mínimo 3 caracteres"
        )

    if produto.preco <= 0:
        raise HTTPException(
            status_code=400,
            detail="Preço deve ser maior que zero"
        )

    if produto.estoque < 0:
        raise HTTPException(
            status_code=400,
            detail="Estoque não pode ser negativo"
        )

    return True