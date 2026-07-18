from pydantic import BaseModel
from datetime import datetime

from app.schemas.item_venda import ItemVendaResponse


class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int



class VendaCreate(BaseModel):
    cliente_id: int
    itens: list[ItemVendaCreate]



class VendaResponse(BaseModel):

    id: int
    cliente_id: int
    usuario_id: int
    total: float
    status: str
    created_at: datetime

    itens: list[ItemVendaResponse]


    class Config:
        from_attributes = True

class ClienteVendaResponse(BaseModel):

    id: int
    nome: str

    class Config:
        from_attributes = True