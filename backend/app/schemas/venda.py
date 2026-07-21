from pydantic import BaseModel
from datetime import datetime

from app.schemas.item_venda import ItemVendaResponse


class ClienteResumo(BaseModel):

    id: int
    nome: str


    class Config:
        from_attributes = True



class VendaCreate(BaseModel):

    cliente_id: int
    itens: list



class VendaResponse(BaseModel):

    id: int

    cliente_id: int

    usuario_id: int

    total: float

    status: str

    created_at: datetime


    cliente: ClienteResumo | None = None

    itens: list[ItemVendaResponse] = []


    class Config:
        from_attributes = True