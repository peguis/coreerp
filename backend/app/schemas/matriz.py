from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.empresa import EmpresaResponse
from app.schemas.modulo import ModuloResponse
from app.schemas.usuario import UsuarioResponse
from app.core.enums import PerfilUsuario


class MatrizTenantResumo(EmpresaResponse):
    modulos_ativos: int = 0
    administrador_principal: UsuarioResponse | None = None
    protegido: bool = False
    eh_matriz: bool = False
    eh_demo: bool = False
    criado_por_usuario_id: int | None = None
    demo_expira_em: datetime | None = None


class MatrizModuloUso(BaseModel):
    codigo: str
    nome: str
    empresas_ativas: int
    ativo: bool = True


class MatrizModuloCatalogo(BaseModel):
    codigo: str
    nome: str
    descricao: str | None = None
    obrigatorio: bool
    ordem: int


class MatrizModuloStatusUpdate(BaseModel):
    ativo: bool


class MatrizUsuarioUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=150)
    email: str | None = None
    perfil: PerfilUsuario | None = None
    ativo: bool | None = None


class MatrizVendedorResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool


class MatrizOportunidadeCreate(BaseModel):
    nome_negocio_contato: str = Field(min_length=2, max_length=150)
    pessoa_responsavel: str | None = Field(default=None, max_length=150)
    telefone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=150)
    canal_contato: str | None = Field(default=None, max_length=80)
    cidade_regiao: str | None = Field(default=None, max_length=120)
    tipo_negocio: str | None = Field(default=None, max_length=80)
    vendedor_id: int | None = None
    origem: str | None = Field(default=None, max_length=100)
    status: str = Field(default="NOVO", max_length=40)
    proxima_acao: str | None = Field(default=None, max_length=180)
    proximo_contato: date | None = None
    observacoes: str | None = None
    modulos_interesse: list[str] = Field(default_factory=list, max_length=30)
    tenant_demo_id: int | None = None


class MatrizOportunidadeUpdate(BaseModel):
    nome_negocio_contato: str | None = Field(default=None, min_length=2, max_length=150)
    pessoa_responsavel: str | None = Field(default=None, max_length=150)
    telefone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=150)
    canal_contato: str | None = Field(default=None, max_length=80)
    cidade_regiao: str | None = Field(default=None, max_length=120)
    tipo_negocio: str | None = Field(default=None, max_length=80)
    vendedor_id: int | None = None
    origem: str | None = Field(default=None, max_length=100)
    status: str | None = Field(default=None, max_length=40)
    proxima_acao: str | None = Field(default=None, max_length=180)
    proximo_contato: date | None = None
    observacoes: str | None = None
    modulos_interesse: list[str] | None = Field(default=None, max_length=30)
    tenant_demo_id: int | None = None


class MatrizInteracaoCreate(BaseModel):
    descricao: str = Field(min_length=2, max_length=5000)
    proxima_acao: str | None = Field(default=None, max_length=180)
    proximo_contato: date | None = None
    status: str | None = Field(default=None, max_length=40)


class MatrizOportunidadeInteracaoResponse(BaseModel):
    id: int
    usuario_id: int
    usuario_nome: str | None = None
    descricao: str
    proxima_acao: str | None = None
    proximo_contato: date | None = None
    criado_em: datetime


class MatrizOportunidadeResponse(BaseModel):
    id: int
    empresa_id: int
    vendedor_id: int
    vendedor_nome: str | None = None
    nome_negocio_contato: str
    pessoa_responsavel: str | None = None
    telefone: str | None = None
    email: str | None = None
    canal_contato: str | None = None
    cidade_regiao: str | None = None
    tipo_negocio: str | None = None
    origem: str | None = None
    status: str
    proxima_acao: str | None = None
    proximo_contato: date | None = None
    observacoes: str | None = None
    modulos_interesse: list[str] = Field(default_factory=list)
    tenant_demo_id: int | None = None
    tenant_demo_nome: str | None = None
    tenant_demo_ativo: bool | None = None
    tenant_demo_eh_demo: bool | None = None
    ultima_interacao_em: datetime | None = None
    conversao_solicitada_em: datetime | None = None
    convertido_em: datetime | None = None
    criado_em: datetime
    interacoes: list[MatrizOportunidadeInteracaoResponse] = Field(default_factory=list)


class MatrizPreviaDemonstracaoResponse(BaseModel):
    id: int
    nome: str
    identidade_codigo: str | None = None
    logo_url: str | None = None
    cor_primaria: str | None = None
    cor_secundaria: str | None = None
    tipo_negocio: str | None = None
    ativo: bool
    eh_demo: bool
    criado_por_usuario_id: int | None = None
    criado_por_usuario_nome: str | None = None
    modulos_ativos: list[str] = Field(default_factory=list)


class MatrizAprovarConversao(BaseModel):
    confirmar: bool = False


class MatrizAlerta(BaseModel):
    severidade: str
    titulo: str
    descricao: str
    empresa_id: int | None = None


class MatrizAuditoriaResponse(BaseModel):
    id: int
    empresa_id: int
    empresa_nome: str | None = None
    usuario_id: int | None = None
    usuario_nome: str | None = None
    acao: str
    recurso: str
    recurso_id: int | None = None
    detalhes: dict | None = None
    criado_em: datetime


class MatrizDashboardResponse(BaseModel):
    total_empresas: int
    empresas_ativas: int
    empresas_inativas: int
    modulos_mais_utilizados: list[MatrizModuloUso]
    empresas_recentes: list[MatrizTenantResumo]
    alertas: list[MatrizAlerta]
    ultimas_auditorias: list[MatrizAuditoriaResponse]


class MatrizTenantDetalhe(BaseModel):
    empresa: MatrizTenantResumo
    modulos: list[ModuloResponse]
    usuarios: list[UsuarioResponse]
    auditoria: list[MatrizAuditoriaResponse]


class MatrizIdentidadeUpdate(BaseModel):
    nome_exibicao: str | None = Field(default=None, min_length=3, max_length=100)
    identidade_codigo: str | None = Field(default=None, max_length=40)
    logo_url: str | None = None
    cor_primaria: str | None = None
    cor_secundaria: str | None = None
    tema: str | None = Field(default=None, max_length=20)
    tipo_negocio: str | None = Field(default=None, max_length=80)
    ativo: bool | None = None

    @field_validator("cor_primaria", "cor_secundaria")
    @classmethod
    def validar_cor(cls, value):
        if value is None or value == "":
            return value
        value = value.strip()
        if not value.startswith("#") or len(value) != 7:
            raise ValueError("A cor deve estar no formato hexadecimal #RRGGBB.")
        try:
            int(value[1:], 16)
        except ValueError as exc:
            raise ValueError("A cor deve estar no formato hexadecimal #RRGGBB.") from exc
        return value


class MatrizAuditoriaQuery(BaseModel):
    empresa_id: int | None = None
    acao: str | None = None
    limite: int = Field(default=50, ge=1, le=200)
