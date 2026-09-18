from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import StatusAgendamento


class AgendamentoCreate(BaseModel):
    profissional_id: int | None = Field(default=None, gt=0)
    servico_id: int = Field(gt=0)
    cliente_id: int | None = Field(default=None, gt=0)
    cliente_avulso_nome: str | None = None
    recurso_id: int | None = Field(default=None, gt=0)
    inicio_em: datetime
    duracao_minutos: int | None = Field(default=None, gt=0, le=1440)
    observacao: str | None = None

    @field_validator("cliente_avulso_nome", "observacao")
    @classmethod
    def normalizar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        texto = value.strip()
        return texto or None


class AgendamentoUpdate(BaseModel):
    profissional_id: int | None = Field(default=None, gt=0)
    servico_id: int | None = Field(default=None, gt=0)
    cliente_id: int | None = Field(default=None, gt=0)
    cliente_avulso_nome: str | None = None
    recurso_id: int | None = Field(default=None, gt=0)
    inicio_em: datetime | None = None
    duracao_minutos: int | None = Field(default=None, gt=0, le=1440)
    status: StatusAgendamento | None = None
    observacao: str | None = None
    motivo_cancelamento: str | None = None

    @field_validator(
        "cliente_avulso_nome",
        "observacao",
        "motivo_cancelamento",
    )
    @classmethod
    def normalizar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        texto = value.strip()
        return texto or None


class AgendamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    profissional_id: int | None
    servico_id: int | None
    cliente_id: int | None
    cliente_nome: str | None
    cliente_avulso_nome: str | None
    recurso_id: int | None
    recurso_nome: str | None
    inicio_em: datetime
    fim_em: datetime
    duracao_minutos: int
    status: StatusAgendamento
    observacao: str | None
    motivo_cancelamento: str | None
    criado_por_usuario_id: int | None
    detalhes_restritos: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
