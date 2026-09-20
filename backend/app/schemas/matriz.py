from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.empresa import EmpresaResponse
from app.schemas.modulo import ModuloResponse
from app.schemas.usuario import UsuarioResponse
from app.core.enums import PerfilUsuario


class MatrizTenantResumo(EmpresaResponse):
    modulos_ativos: int = 0
    administrador_principal: UsuarioResponse | None = None
    protegido: bool = False


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
