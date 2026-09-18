from enum import Enum


class PerfilUsuario(str, Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    OPERADOR = "operador"
    CONSULTA = "consulta"
    USUARIO = "usuario"
    PROFISSIONAL = "profissional"


class AreaAtuacao(str, Enum):
    BARBEARIA = "BARBEARIA"
    TATTOO = "TATTOO"


class FormaPagamento(str, Enum):
    PIX = "PIX"
    DINHEIRO = "DINHEIRO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    CARTAO_CREDITO = "CARTAO_CREDITO"


class FormaPagamentoRepasse(str, Enum):
    PIX = "PIX"
    DINHEIRO = "DINHEIRO"
    TRANSFERENCIA = "TRANSFERENCIA"


class OrigemLancamento(str, Enum):
    ATENDIMENTO = "ATENDIMENTO"
    REPASSE = "REPASSE"


class StatusAgendamento(str, Enum):
    AGENDADO = "AGENDADO"
    CONFIRMADO = "CONFIRMADO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"
    NAO_COMPARECEU = "NAO_COMPARECEU"


class ModoReservaRecurso(str, Enum):
    AUTOMATICO = "AUTOMATICO"
    MANUAL = "MANUAL"


class StatusRecursoAgenda(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    MANUTENCAO = "MANUTENCAO"
