from datetime import datetime

from pydantic import BaseModel


class ModuloResponse(BaseModel):
    codigo: str
    nome: str
    descricao: str | None
    obrigatorio: bool
    ordem: int
    ativo: bool
    ativado_em: datetime | None
    desativado_em: datetime | None


class ModuloStatusUpdate(BaseModel):
    ativo: bool
