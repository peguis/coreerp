from pydantic import BaseModel


class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    estoque: int


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool

    class Config:
        from_attributes = True