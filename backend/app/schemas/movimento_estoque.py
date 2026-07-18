from datetime import datetime

from pydantic import BaseModel


class MovimentoEstoqueCreate(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int
    observacao: str | None = None


class MovimentoEstoqueResponse(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    observacao: str | None
    created_at: datetime

    class Config:
        from_attributes = True