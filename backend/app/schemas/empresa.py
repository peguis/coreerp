from datetime import datetime

from pydantic import BaseModel


class EmpresaCreate(BaseModel):

    nome: str
    cnpj: str
    email: str
    telefone: str | None = None


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
