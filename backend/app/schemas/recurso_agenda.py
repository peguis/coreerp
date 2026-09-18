from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import StatusRecursoAgenda


class RecursoAgendaCreate(BaseModel):
    nome: str
    tipo: str
    status: StatusRecursoAgenda = StatusRecursoAgenda.ATIVO

    @field_validator("nome", "tipo")
    @classmethod
    def normalizar_texto(cls, value: str) -> str:
        texto = value.strip()
        if not texto:
            raise ValueError("O campo nao pode ser vazio.")
        return texto


class RecursoAgendaUpdate(BaseModel):
    nome: str | None = None
    tipo: str | None = None
    ativo: bool | None = None
    status: StatusRecursoAgenda | None = None

    @field_validator("nome", "tipo")
    @classmethod
    def validar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        texto = value.strip()
        if not texto:
            raise ValueError("O campo nao pode ser vazio.")
        return texto


class RecursoAgendaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    empresa_id: int
    nome: str
    tipo: str
    ativo: bool
    status: StatusRecursoAgenda
    disponivel: bool
    created_at: datetime
    updated_at: datetime
