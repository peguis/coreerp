from datetime import datetime

from pydantic import BaseModel
from app.schemas.usuario import UsuarioResponse

class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    email: str
    telefone: str


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    email: str
    telefone: str
    ativo: bool
    created_at: datetime | None
    usuarios: list[UsuarioResponse] = []


    class Config:
        from_attributes = True

from pydantic import BaseModel


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    email: str
    telefone: str | None
    ativo: bool

    class Config:
        from_attributes = True