from sqlalchemy.orm import Session

from app.repositories import empresa as repository
from app.schemas.empresa import EmpresaCreate
from app.core.validators.empresa import validar_empresa


from app.repositories.empresa import (
    criar_empresa,
    listar_empresas,
    buscar_empresa_por_id,
    atualizar_empresa,
    deletar_empresa
)



def criar_empresa_service(
    db,
    empresa
):

    validar_empresa(empresa)

    return criar_empresa(
        db,
        empresa
    )

def listar_empresas_service(db):
    return listar_empresas(db)

def buscar_empresa_por_id_service(db, empresa_id):
    return buscar_empresa_por_id(db, empresa_id)

def atualizar_empresa_service(
    db,
    empresa_id,
    dados
):

    empresa = buscar_empresa_por_id(
        db,
        empresa_id
    )

    if not empresa:
        return None

    if "nome" in dados:
        if len(dados["nome"].strip()) < 3:
            return None

    return atualizar_empresa(
        db,
        empresa,
        dados
    )

def deletar_empresa_service(db, empresa_db):
    deletar_empresa(db, empresa_db)