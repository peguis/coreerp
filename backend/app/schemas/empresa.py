from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class EmpresaCreate(BaseModel):

    nome: str
    identidade_codigo: str | None = None
    cnpj: str
    email: str
    telefone: str | None = None


class EmpresaProvisionamentoCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    identidade_codigo: str | None = Field(default=None, max_length=40)
    cnpj: str = Field(min_length=1, max_length=18)
    email: EmailStr
    telefone: str | None = None
    administrador_nome: str = Field(min_length=3, max_length=150)
    administrador_email: EmailStr
    administrador_senha: str = Field(min_length=6, max_length=128)
    tipo_negocio: str | None = None
    cor_primaria: str | None = None
    cor_secundaria: str | None = None
    logo_url: str | None = None
    modulos_iniciais: list[str] | None = None


class EmpresaConfiguracaoUpdate(BaseModel):
    nome_exibicao: str | None = None
    logo_url: str | None = None
    cor_primaria: str | None = None
    cor_secundaria: str | None = None
    tema: str | None = None
    tipo_negocio: str | None = None


class EmpresaOnboardingItem(BaseModel):
    codigo: str
    titulo: str
    descricao: str
    concluido: bool
    obrigatorio: bool = True


class EmpresaOnboardingResponse(BaseModel):
    percentual_concluido: int
    concluido: bool
    itens: list[EmpresaOnboardingItem]



class EmpresaResponse(BaseModel):

    id: int
    nome: str
    identidade_codigo: str | None
    cnpj: str
    email: str
    telefone: str | None
    logo_url: str | None
    cor_primaria: str | None
    cor_secundaria: str | None
    tema: str | None
    tipo_negocio: str | None
    ativo: bool
    created_at: datetime | None

    class Config:
        from_attributes = True
