from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.schemas.categoria_financeira import (
    CategoriaFinanceiraResumo
)



class LancamentoFinanceiroBase(BaseModel):

    model_config = ConfigDict(extra="forbid")

    descricao: str

    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

    tipo: str

    data_vencimento: date

    categoria_id: int | None = None

    observacoes: str | None = None





class LancamentoFinanceiroCreate(
    LancamentoFinanceiroBase
):

    pass





class LancamentoFinanceiroUpdate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    descricao: str | None = None

    valor: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    tipo: str | None = None

    data_vencimento: date | None = None

    data_pagamento: datetime | None = None

    status: str | None = None

    categoria_id: int | None = None

    observacoes: str | None = None





class LancamentoFinanceiroResponse(
    LancamentoFinanceiroBase
):

    id: int

    empresa_id: int

    usuario_id: int

    status: str

    data_pagamento: datetime | None

    created_at: datetime

    categoria: CategoriaFinanceiraResumo | None = None

    origem_tipo: str | None = None

    origem_id: int | None = None

    forma_pagamento: str | None = None


    model_config = ConfigDict(from_attributes=True)

    @field_serializer("valor")
    def serializar_valor(self, value: Decimal) -> str:
        return format(value, ".2f")
