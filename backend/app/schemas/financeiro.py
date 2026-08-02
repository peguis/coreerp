from datetime import date, datetime

from typing import Optional

from pydantic import BaseModel



class LancamentoCreate(BaseModel):

    descricao: str

    valor: float

    tipo: str

    categoria_id: Optional[int] = None

    data_vencimento: date

    status: Optional[str] = "PENDENTE"

    observacoes: Optional[str] = None





class LancamentoUpdate(BaseModel):

    descricao: Optional[str] = None

    valor: Optional[float] = None

    tipo: Optional[str] = None

    categoria_id: Optional[int] = None

    data_vencimento: Optional[date] = None

    data_pagamento: Optional[datetime] = None

    status: Optional[str] = None

    observacoes: Optional[str] = None





class BaixaLancamento(BaseModel):

    data_pagamento: Optional[datetime] = None





class LancamentoResponse(BaseModel):

    id: int

    empresa_id: int

    usuario_id: int


    descricao: str

    valor: float

    tipo: str


    categoria_id: Optional[int] = None


    data_vencimento: date

    data_pagamento: Optional[datetime] = None


    status: str


    observacoes: Optional[str] = None


    created_at: datetime



    class Config:

        from_attributes = True