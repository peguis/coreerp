from datetime import datetime

from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cnpj: str
    email: str
    telefone: str | None = None



class EmpresaResponse(BaseModel):

    id: int
    nome: str
    cnpj: str
    email: str
    telefone: str | None
    ativo: bool
    created_at: datetime | None

    class Config:
        from_attributes = True