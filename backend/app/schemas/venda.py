from pydantic import BaseModel, Field, StrictInt
from datetime import datetime

from app.schemas.item_venda import ItemVendaResponse



class ClienteResumo(BaseModel):

    id: int

    nome: str


    class Config:
        from_attributes = True



class VendaItemCreate(BaseModel):

    produto_id: int

    quantidade: StrictInt = Field(gt=0)



class VendaCreate(BaseModel):

    cliente_id: int

    itens: list[VendaItemCreate]

    # A venda manual continua iniciando como ABERTA. A integração do
    # e-commerce pode criar o pedido como PENDENTE, sem baixar estoque.
    status: str = "ABERTA"

    origem: str = Field(default="ERP", max_length=30)

    pedido_externo_id: str | None = Field(default=None, max_length=100)

    chave_idempotencia: str | None = Field(default=None, max_length=80)

    observacoes: str | None = None

    endereco_entrega: str | None = None



class VendaResponse(BaseModel):

    id: int

    empresa_id: int

    cliente_id: int

    usuario_id: int

    total: float

    status: str

    estoque_baixado: bool

    origem: str

    pedido_externo_id: str | None = None

    chave_idempotencia: str | None = None

    observacoes: str | None = None

    endereco_entrega: str | None = None

    created_at: datetime


    cliente: ClienteResumo | None = None

    itens: list[ItemVendaResponse] = Field(
        default_factory=list
    )


    class Config:
        from_attributes = True
