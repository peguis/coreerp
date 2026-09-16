from pydantic import BaseModel, Field, StrictInt


class ProdutoResumo(BaseModel):

    id: int

    nome: str

    preco: float


    class Config:
        from_attributes = True



class ItemVendaResponse(BaseModel):

    id: int

    empresa_id: int

    produto_id: int

    quantidade: StrictInt = Field(gt=0)

    preco_unitario: float

    subtotal: float

    produto: ProdutoResumo | None = None


    class Config:
        from_attributes = True
