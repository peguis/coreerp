from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.item_venda import ItemVendaResponse



class ClienteResumo(BaseModel):

    id: int

    nome: str


    class Config:
        from_attributes = True



class VendaItemCreate(BaseModel):

    produto_id: int

    quantidade: int



class VendaCreate(BaseModel):

    cliente_id: int

    itens: list[VendaItemCreate]



class VendaResponse(BaseModel):

    id: int

    empresa_id: int

    cliente_id: int

    usuario_id: int

    total: float

    status: str

    created_at: datetime


    cliente: ClienteResumo | None = None

    itens: list[ItemVendaResponse] = Field(
        default_factory=list
    )


    class Config:
        from_attributes = True