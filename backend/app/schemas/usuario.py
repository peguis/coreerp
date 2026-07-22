from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.core.enums import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: int
    perfil: PerfilUsuario = PerfilUsuario.OPERADOR


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime | None
    empresa_id: int | None
    perfil: PerfilUsuario

    class Config:
        from_attributes = True