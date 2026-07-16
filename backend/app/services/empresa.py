from sqlalchemy.orm import Session

from app.repositories import empresa as repository
from app.schemas.empresa import EmpresaCreate


def criar_empresa(
    db: Session,
    dados: EmpresaCreate
):
    return repository.criar_empresa(
        db,
        dados
    )