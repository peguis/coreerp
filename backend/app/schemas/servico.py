from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)

from app.core.enums import ModoReservaRecurso


class ServicoCreate(BaseModel):
    nome: str
    descricao: str | None = None
    preco_padrao: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
    )
    duracao_minutos: int = Field(default=60, gt=0, le=1440)
    requer_recurso: bool = False
    tipo_recurso: str | None = None
    modo_selecao_recurso: ModoReservaRecurso = ModoReservaRecurso.AUTOMATICO

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        nome = value.strip()
        if not nome:
            raise ValueError("O nome do servico nao pode ser vazio.")
        return nome


class ServicoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco_padrao: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )
    duracao_minutos: int | None = Field(default=None, gt=0, le=1440)
    requer_recurso: bool | None = None
    tipo_recurso: str | None = None
    modo_selecao_recurso: ModoReservaRecurso | None = None
    ativo: bool | None = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("O nome do servico nao pode ser nulo.")
        nome = value.strip()
        if not nome:
            raise ValueError("O nome do servico nao pode ser vazio.")
        return nome

    @field_validator("preco_padrao")
    @classmethod
    def validar_preco(cls, value: Decimal | None) -> Decimal:
        if value is None:
            raise ValueError("O preco_padrao nao pode ser nulo.")
        return value

    @field_validator("ativo")
    @classmethod
    def validar_ativo(cls, value: bool | None) -> bool:
        if value is None:
            raise ValueError("O campo ativo nao pode ser nulo.")
        return value


class ServicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    nome: str
    descricao: str | None = None
    preco_padrao: Decimal
    duracao_minutos: int
    requer_recurso: bool
    tipo_recurso: str | None
    modo_selecao_recurso: ModoReservaRecurso | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("preco_padrao")
    def serializar_preco(self, value: Decimal) -> float:
        return float(value)
