from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)

from app.core.enums import AreaAtuacao


class ProfissionalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usuario_id: int = Field(gt=0)
    area_atuacao: AreaAtuacao
    percentual_padrao: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )


class ProfissionalUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    area_atuacao: AreaAtuacao | None = None
    percentual_padrao: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )
    ativo: bool | None = None

    @field_validator("area_atuacao", "percentual_padrao", "ativo")
    @classmethod
    def rejeitar_nulo(cls, value):
        if value is None:
            raise ValueError("O campo informado nao pode ser nulo.")
        return value


class ProfissionalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    usuario_id: int
    area_atuacao: AreaAtuacao
    percentual_padrao: Decimal
    ativo: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("percentual_padrao")
    def serializar_percentual(self, value: Decimal) -> float:
        return float(value)
