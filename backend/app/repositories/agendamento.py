from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.agendamento import Agendamento
from app.models.recurso_agenda import RecursoAgenda


STATUS_NAO_OCUPA = ("CANCELADO", "NAO_COMPARECEU")


def criar_agendamento(db: Session, **dados) -> Agendamento:
    agendamento = Agendamento(**dados)
    db.add(agendamento)
    db.flush()
    return agendamento


def buscar_agendamento_por_id(
    db: Session,
    agendamento_id: int,
    empresa_id: int,
) -> Agendamento | None:
    return (
        db.query(Agendamento)
        .filter(
            Agendamento.id == agendamento_id,
            Agendamento.empresa_id == empresa_id,
        )
        .first()
    )


def listar_agendamentos(
    db: Session,
    empresa_id: int,
    inicio_de: datetime | None = None,
    inicio_ate: datetime | None = None,
    profissional_id: int | None = None,
    recurso_id: int | None = None,
    status: str | None = None,
) -> list[Agendamento]:
    query = db.query(Agendamento).filter(
        Agendamento.empresa_id == empresa_id
    )
    if inicio_de is not None:
        query = query.filter(Agendamento.fim_em > inicio_de)
    if inicio_ate is not None:
        query = query.filter(Agendamento.inicio_em < inicio_ate)
    if profissional_id is not None:
        query = query.filter(Agendamento.profissional_id == profissional_id)
    if recurso_id is not None:
        query = query.filter(Agendamento.recurso_id == recurso_id)
    if status is not None:
        query = query.filter(Agendamento.status == status)
    return query.order_by(Agendamento.inicio_em.asc(), Agendamento.id.asc()).all()


def buscar_conflitos(
    db: Session,
    empresa_id: int,
    profissional_id: int,
    inicio_em: datetime,
    fim_em: datetime,
    recurso_id: int | None = None,
    ignorar_id: int | None = None,
) -> list[Agendamento]:
    query = db.query(Agendamento).filter(
        Agendamento.empresa_id == empresa_id,
        Agendamento.status.notin_(STATUS_NAO_OCUPA),
        Agendamento.inicio_em < fim_em,
        Agendamento.fim_em > inicio_em,
        or_(
            Agendamento.profissional_id == profissional_id,
            (
                recurso_id is not None
                and Agendamento.recurso_id == recurso_id
            ),
        ),
    )
    if ignorar_id is not None:
        query = query.filter(Agendamento.id != ignorar_id)
    return query.all()


def listar_recursos_livres(
    db: Session,
    empresa_id: int,
    tipo: str,
    inicio_em: datetime,
    fim_em: datetime,
) -> list[RecursoAgenda]:
    tipo_normalizado = " ".join(tipo.strip().upper().split())
    recursos = (
        db.query(RecursoAgenda)
        .filter(
            RecursoAgenda.empresa_id == empresa_id,
            or_(
                func.upper(RecursoAgenda.tipo) == tipo_normalizado,
                func.upper(RecursoAgenda.tipo).like(f"{tipo_normalizado} %"),
                func.upper(RecursoAgenda.tipo).like(f"% {tipo_normalizado}"),
            ),
            RecursoAgenda.ativo.is_(True),
            RecursoAgenda.status == "ATIVO",
        )
        .order_by(RecursoAgenda.nome.asc(), RecursoAgenda.id.asc())
        .all()
    )
    livres = []
    for recurso in recursos:
        conflito = (
            db.query(Agendamento.id)
            .filter(
                Agendamento.empresa_id == empresa_id,
                Agendamento.recurso_id == recurso.id,
                Agendamento.status.notin_(STATUS_NAO_OCUPA),
                Agendamento.inicio_em < fim_em,
                Agendamento.fim_em > inicio_em,
            )
            .first()
        )
        if conflito is None:
            livres.append(recurso)
    return livres
