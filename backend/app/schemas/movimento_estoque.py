from pydantic import BaseModel
from datetime import datetime


class ProdutoResumo(BaseModel):

    id: int
    nome: str

    class Config:
        from_attributes = True



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

    produto: ProdutoResumo | None = None



    class Config:

        from_attributes = True