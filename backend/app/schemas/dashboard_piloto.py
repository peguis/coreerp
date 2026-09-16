from datetime import date
from decimal import Decimal

from pydantic import BaseModel, field_serializer

from app.core.enums import AreaAtuacao, FormaPagamento


class _ValoresDecimais(BaseModel):
    @field_serializer("*", check_fields=False)
    def serializar_decimal(self, value):
        if isinstance(value, Decimal):
            return format(value, ".2f")
        return value


class DesempenhoProfissionalResponse(_ValoresDecimais):
    profissional_id: int
    nome: str
    area_atuacao: AreaAtuacao
    quantidade_atendimentos: int
    faturamento_bruto: Decimal
    valor_profissional: Decimal
    valor_casa: Decimal
    valor_repassado: Decimal
    valor_pendente: Decimal


class DesempenhoServicoResponse(_ValoresDecimais):
    servico_id: int
    nome: str
    quantidade: int
    faturamento_bruto: Decimal


class DesempenhoFormaPagamentoResponse(_ValoresDecimais):
    forma_pagamento: FormaPagamento
    quantidade_atendimentos: int
    valor_total: Decimal


class DashboardPilotoResponse(_ValoresDecimais):
    data_inicio: date
    data_fim: date
    total_atendimentos: int
    faturamento_bruto: Decimal
    valor_casa: Decimal
    valor_profissionais: Decimal
    total_repassado: Decimal
    total_pendente_repasses: Decimal
    entradas_caixa_piloto: Decimal
    saidas_caixa_piloto: Decimal
    saldo_caixa_piloto: Decimal
    por_profissional: list[DesempenhoProfissionalResponse]
    por_servico: list[DesempenhoServicoResponse]
    por_forma_pagamento: list[DesempenhoFormaPagamentoResponse]


class DashboardProfissionalResponse(_ValoresDecimais):
    data_inicio: date
    data_fim: date
    profissional_id: int
    nome: str
    area_atuacao: AreaAtuacao
    quantidade_atendimentos: int
    faturamento_bruto: Decimal
    valor_profissional: Decimal
    valor_repassado: Decimal
    valor_pendente: Decimal
