from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate


def criar_empresa(
    db: Session,
    empresa: EmpresaCreate
):
    nova_empresa = Empresa(
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        email=empresa.email,
        telefone=empresa.telefone,
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa

def listar_empresas(db: Session):
    return db.query(Empresa).all()

def buscar_empresa_por_id(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def atualizar_empresa(db: Session, empresa_db, empresa_dados):
    dados = empresa_dados.model_dump()

    for campo, valor in dados.items():
        setattr(empresa_db, campo, valor)

    db.commit()
    db.refresh(empresa_db)

    return empresa_db


def deletar_empresa(db: Session, empresa_db):
    db.delete(empresa_db)
    db.commit()