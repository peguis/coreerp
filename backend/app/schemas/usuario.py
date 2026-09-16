from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.core.enums import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: int
    perfil: PerfilUsuario = PerfilUsuario.OPERADOR


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    perfil: PerfilUsuario | None = None
    ativo: bool | None = None

    @field_validator("nome", "email", "senha", "perfil", "ativo")
    @classmethod
    def rejeitar_nulo(cls, value):
        if value is None:
            raise ValueError("O campo informado nao pode ser nulo.")
        return value

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, value):
        if value is not None and len(value) < 6:
            raise ValueError("A nova senha deve possuir no minimo 6 caracteres.")
        return value


class UsuarioResponse(BaseModel):

    id: int
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime | None
    empresa_id: int
    perfil: PerfilUsuario

    class Config:
        from_attributes = True
