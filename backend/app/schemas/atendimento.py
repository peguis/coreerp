from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from app.core.enums import FormaPagamento


class AtendimentoCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profissional_id: int | None = Field(default=None, gt=0)
    servico_id: int = Field(gt=0)
    cliente_id: int | None = Field(default=None, gt=0)
    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    percentual_profissional_override: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    forma_pagamento: FormaPagamento
    observacao: str | None = None
    realizado_em: datetime | None = None

    @field_validator("valor")
    @classmethod
    def validar_valor_finito(cls, value: Decimal) -> Decimal:
        if not value.is_finite():
            raise ValueError("O valor deve ser finito.")
        return value

    @field_validator("percentual_profissional_override")
    @classmethod
    def validar_override_finito(cls, value: Decimal | None) -> Decimal | None:
        if value is not None and not value.is_finite():
            raise ValueError("O override deve ser um percentual finito.")
        return value


class AtendimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    profissional_id: int
    servico_id: int
    cliente_id: int | None
    valor: Decimal
    percentual_profissional: Decimal
    valor_profissional: Decimal
    valor_casa: Decimal
    forma_pagamento: FormaPagamento
    observacao: str | None
    realizado_em: datetime
    created_at: datetime
    updated_at: datetime

    @field_serializer(
        "valor",
        "percentual_profissional",
        "valor_profissional",
        "valor_casa",
    )
    def serializar_valor(self, value: Decimal) -> float:
        return float(value)
