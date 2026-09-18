from sqlalchemy.orm import Session

from app.models.recurso_agenda import RecursoAgenda


def criar_recurso(
    db: Session,
    empresa_id: int,
    nome: str,
    tipo: str,
    status: str = "ATIVO",
) -> RecursoAgenda:
    recurso = RecursoAgenda(
        empresa_id=empresa_id,
        nome=nome,
        tipo=tipo,
        ativo=status == "ATIVO",
        status=status,
    )
    db.add(recurso)
    db.flush()
    return recurso


def listar_recursos(
    db: Session,
    empresa_id: int,
    tipo: str | None = None,
    ativo: bool | None = None,
    status: str | None = None,
) -> list[RecursoAgenda]:
    query = db.query(RecursoAgenda).filter(
        RecursoAgenda.empresa_id == empresa_id
    )
    if tipo:
        query = query.filter(RecursoAgenda.tipo == tipo)
    if ativo is not None:
        query = query.filter(RecursoAgenda.ativo == ativo)
    if status:
        query = query.filter(RecursoAgenda.status == status)
    return query.order_by(RecursoAgenda.nome.asc(), RecursoAgenda.id.asc()).all()


def buscar_recurso_por_id(
    db: Session,
    recurso_id: int,
    empresa_id: int,
) -> RecursoAgenda | None:
    return (
        db.query(RecursoAgenda)
        .filter(
            RecursoAgenda.id == recurso_id,
            RecursoAgenda.empresa_id == empresa_id,
        )
        .first()
    )


def atualizar_recurso(
    db: Session,
    recurso: RecursoAgenda,
    dados: dict,
) -> RecursoAgenda:
    for campo in ("nome", "tipo", "ativo", "status"):
        if campo in dados:
            setattr(recurso, campo, dados[campo])
    return recurso
