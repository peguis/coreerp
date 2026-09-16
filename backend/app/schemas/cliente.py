from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):

    nome: str

    email: EmailStr | None = None

    telefone: str | None = None

    cpf_cnpj: str | None = None


class ClienteProfissionalResponse(BaseModel):

    id: int

    nome: str

    class Config:
        from_attributes = True



class ClienteResponse(BaseModel):

    id: int

    empresa_id: int

    nome: str

    email: EmailStr | None = None

    telefone: str | None = None

    cpf_cnpj: str | None = None

    ativo: bool

    class Config:
        from_attributes = True
