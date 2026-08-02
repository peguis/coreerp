from datetime import datetime

from pydantic import BaseModel



class CategoriaFinanceiraBase(BaseModel):

    nome: str

    tipo: str





class CategoriaFinanceiraCreate(
    CategoriaFinanceiraBase
):

    ativo: bool = True





class CategoriaFinanceiraUpdate(BaseModel):

    nome: str | None = None

    tipo: str | None = None

    ativo: bool | None = None





class CategoriaFinanceiraResponse(
    CategoriaFinanceiraBase
):

    id: int

    empresa_id: int

    ativo: bool

    created_at: datetime


    class Config:
        from_attributes = True





class CategoriaFinanceiraResumo(BaseModel):

    id: int

    nome: str

    tipo: str


    class Config:
        from_attributes = True