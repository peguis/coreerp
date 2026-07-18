from pydantic import BaseModel


class ProdutoResumo(BaseModel):

    id: int
    nome: str
    preco: float

    class Config:
        from_attributes = True



class ItemVendaResponse(BaseModel):

    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float
    produto: ProdutoResumo


    class Config:
        from_attributes = True