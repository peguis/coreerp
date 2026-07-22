from pydantic import BaseModel
from datetime import datetime



class MovimentoEstoqueCreate(BaseModel):

    produto_id: int

    tipo: str

    quantidade: float

    observacao: str | None = None





class MovimentoEstoqueResponse(BaseModel):

    id: int

    empresa_id: int

    produto_id: int

    usuario_id: int

    tipo: str

    quantidade: float

    observacao: str | None = None

    created_at: datetime



    class Config:

        from_attributes = True