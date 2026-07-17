from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str | None
    ativo: bool

    class Config:
        from_attributes = True