from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.hash import gerar_hash
from app.repositories import empresa as repository
from app.schemas.empresa import EmpresaCreate, EmpresaProvisionamentoCreate
from app.core.validators.empresa import validar_empresa
from app.services.modulo import inicializar_modulos_empresa
from app.models.agendamento import Agendamento
from app.models.empresa import Empresa
from app.models.modulo import Modulo, EmpresaModulo
from app.models.profissional import Profissional
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.core.enums import PerfilUsuario


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

    nova_empresa = criar_empresa(
        db,
        empresa
    )
    inicializar_modulos_empresa(db, nova_empresa.id)
    return nova_empresa


def provisionar_empresa_service(
    db: Session,
    dados: EmpresaProvisionamentoCreate,
):
    validar_empresa(dados)
    email_empresa = str(dados.email).lower()
    email_admin = str(dados.administrador_email).lower()
    if db.query(Empresa).filter(Empresa.cnpj == dados.cnpj).first():
        raise HTTPException(status_code=409, detail="CNPJ da empresa já cadastrado.")
    if db.query(Empresa).filter(Empresa.email == email_empresa).first():
        raise HTTPException(status_code=409, detail="E-mail da empresa já cadastrado.")
    if db.query(Usuario).filter(Usuario.email == email_admin).first():
        raise HTTPException(status_code=409, detail="E-mail do administrador já cadastrado.")

    empresa = Empresa(
        nome=dados.nome.strip(),
        cnpj=dados.cnpj.strip(),
        email=email_empresa,
        telefone=dados.telefone.strip() if dados.telefone else None,
        tipo_negocio=dados.tipo_negocio.strip() if dados.tipo_negocio else None,
        cor_primaria=dados.cor_primaria.strip() if dados.cor_primaria else None,
        cor_secundaria=dados.cor_secundaria.strip() if dados.cor_secundaria else None,
        ativo=True,
    )
    db.add(empresa)
    db.flush()
    db.add(
        Usuario(
            empresa_id=empresa.id,
            nome=dados.administrador_nome.strip(),
            email=email_admin,
            senha=gerar_hash(dados.administrador_senha),
            perfil=PerfilUsuario.ADMIN.value,
            ativo=True,
        )
    )
    inicializar_modulos_empresa(db, empresa.id, commit=False)
    try:
        db.commit()
        db.refresh(empresa)
        return empresa
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não foi possível provisionar a empresa com os dados informados.",
        ) from exc

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


def obter_onboarding_empresa_service(db: Session, empresa_id: int):
    empresa = buscar_empresa_por_id(db, empresa_id)
    if not empresa:
        return None

    tem_admin = db.query(Usuario.id).filter(
        Usuario.empresa_id == empresa_id,
        Usuario.perfil == "admin",
        Usuario.ativo.is_(True),
    ).first() is not None
    tem_servico = db.query(Servico.id).filter(
        Servico.empresa_id == empresa_id,
        Servico.ativo.is_(True),
    ).first() is not None
    tem_profissional = db.query(Profissional.id).filter(
        Profissional.empresa_id == empresa_id,
        Profissional.ativo.is_(True),
    ).first() is not None
    tem_agendamento = db.query(Agendamento.id).filter(
        Agendamento.empresa_id == empresa_id,
    ).first() is not None
    catalogo_modulos_existe = db.query(Modulo.id).first() is not None
    modulos_configurados = (
        not catalogo_modulos_existe
        or db.query(EmpresaModulo.id).filter(
            EmpresaModulo.empresa_id == empresa_id,
            EmpresaModulo.ativo.is_(True),
        ).first() is not None
    )

    itens = [
        {
            "codigo": "identidade",
            "titulo": "Identidade da empresa",
            "descricao": "Nome e identidade visual prontos para o shell da empresa.",
            "concluido": bool(empresa.nome and empresa.nome.strip()),
        },
        {
            "codigo": "administrador",
            "titulo": "Administrador ativo",
            "descricao": "Existe um administrador ativo para concluir a configuração.",
            "concluido": tem_admin,
        },
        {
            "codigo": "modulos",
            "titulo": "Módulos configurados",
            "descricao": "A empresa possui módulos disponíveis para sua operação.",
            "concluido": modulos_configurados,
        },
        {
            "codigo": "servicos",
            "titulo": "Serviço cadastrado",
            "descricao": "Cadastre ao menos um serviço ativo com duração e preço reais.",
            "concluido": tem_servico,
        },
        {
            "codigo": "profissionais",
            "titulo": "Profissional vinculado",
            "descricao": "Vincule ao menos um profissional ativo à empresa.",
            "concluido": tem_profissional,
        },
        {
            "codigo": "primeiro_agendamento",
            "titulo": "Primeiro agendamento",
            "descricao": "Opcional: registre um agendamento para validar a operação.",
            "concluido": tem_agendamento,
            "obrigatorio": False,
        },
    ]
    obrigatorios = [item for item in itens if item["obrigatorio"]]
    concluidos = sum(item["concluido"] for item in obrigatorios)
    percentual = round((concluidos / len(obrigatorios)) * 100) if obrigatorios else 100
    return {
        "percentual_concluido": percentual,
        "concluido": concluidos == len(obrigatorios),
        "itens": itens,
    }
