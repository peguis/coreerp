from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.core.enums import FormaPagamentoRepasse


class RepasseItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    atendimento_id: int = Field(gt=0)
    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class RepasseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profissional_id: int = Field(gt=0)
    forma_pagamento: FormaPagamentoRepasse
    observacao: str | None = None
    pago_em: datetime | None = None
    itens: list[RepasseItemCreate] = Field(min_length=1)


class RepasseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    repasse_id: int
    atendimento_id: int
    valor: Decimal
    created_at: datetime

    @field_serializer("valor")
    def serializar_valor(self, value: Decimal) -> str:
        return format(value, ".2f")


class RepasseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    profissional_id: int
    created_by_usuario_id: int
    valor: Decimal
    forma_pagamento: FormaPagamentoRepasse
    observacao: str | None
    pago_em: datetime
    created_at: datetime
    itens: list[RepasseItemResponse]

    @field_serializer("valor")
    def serializar_valor(self, value: Decimal) -> str:
        return format(value, ".2f")


class AtendimentoPendenteResponse(BaseModel):
    atendimento_id: int
    realizado_em: datetime
    valor: Decimal
    valor_profissional: Decimal
    valor_repassado: Decimal
    valor_pendente: Decimal

    @field_serializer(
        "valor",
        "valor_profissional",
        "valor_repassado",
        "valor_pendente",
    )
    def serializar_valores(self, value: Decimal) -> str:
        return format(value, ".2f")


class PendenciaProfissionalResponse(BaseModel):
    profissional_id: int
    total_devido: Decimal
    total_repassado: Decimal
    total_pendente: Decimal
    atendimentos: list[AtendimentoPendenteResponse]

    @field_serializer("total_devido", "total_repassado", "total_pendente")
    def serializar_totais(self, value: Decimal) -> str:
        return format(value, ".2f")
