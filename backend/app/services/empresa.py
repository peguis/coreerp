from sqlalchemy.orm import Session

from app.repositories import empresa as repository
from app.schemas.empresa import EmpresaCreate


from app.repositories.empresa import (
    criar_empresa,
    listar_empresas,
    buscar_empresa_por_id,
    atualizar_empresa,
    deletar_empresa
)



def criar_empresa_service(db, empresa):
    return criar_empresa(db, empresa)

def listar_empresas_service(db):
    return listar_empresas(db)

def buscar_empresa_por_id_service(db, empresa_id):
    return buscar_empresa_por_id(db, empresa_id)

def atualizar_empresa_service(db, empresa_db, empresa):
    return atualizar_empresa(db, empresa_db, empresa)

def deletar_empresa_service(db, empresa_db):
    deletar_empresa(db, empresa_db)