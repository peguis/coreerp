from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class MovimentoEstoqueCreate(BaseModel):

    produto_id: int

    tipo: str

    quantidade: float

    observacao: Optional[str] = None



class MovimentoEstoqueResponse(BaseModel):

    id: int

    produto_id: int

    tipo: str

    quantidade: float

    observacao: Optional[str]

    created_at: datetime


    class Config:
        from_attributes = True