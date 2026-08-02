from datetime import datetime, date

from pydantic import BaseModel

from app.schemas.categoria_financeira import (
    CategoriaFinanceiraResumo
)



class LancamentoFinanceiroBase(BaseModel):

    descricao: str

    valor: float

    tipo: str

    data_vencimento: date

    categoria_id: int | None = None

    observacoes: str | None = None





class LancamentoFinanceiroCreate(
    LancamentoFinanceiroBase
):

    pass





class LancamentoFinanceiroUpdate(BaseModel):

    descricao: str | None = None

    valor: float | None = None

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


    class Config:
        from_attributes = True