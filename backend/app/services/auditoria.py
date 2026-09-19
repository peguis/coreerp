from typing import Any

from sqlalchemy.orm import Session

from app.models.auditoria import RegistroAuditoria


def registrar_auditoria(
    db: Session,
    *,
    empresa_id: int,
    acao: str,
    recurso: str,
    usuario_id: int | None = None,
    recurso_id: int | None = None,
    detalhes: dict[str, Any] | None = None,
    commit: bool = True,
) -> RegistroAuditoria:
    registro = RegistroAuditoria(
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        acao=acao,
        recurso=recurso,
        recurso_id=recurso_id,
        detalhes=detalhes,
    )
    db.add(registro)
    if commit:
        db.commit()
        db.refresh(registro)
    return registro
