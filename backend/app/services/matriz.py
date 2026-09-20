from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.identidade import IDENTIDADE_HYPE, resolver_identidade_codigo
from app.models.auditoria import RegistroAuditoria
from app.models.empresa import Empresa
from app.models.modulo import EmpresaModulo, Modulo
from app.models.usuario import Usuario
from app.schemas.matriz import MatrizIdentidadeUpdate
from app.schemas.matriz import MatrizUsuarioUpdate
from app.services.auditoria import registrar_auditoria
from app.services.modulo import atualizar_modulo_empresa, listar_modulos_empresa


def _empresa_protegida(empresa: Empresa) -> bool:
    return empresa.identidade_codigo == IDENTIDADE_HYPE


def _administrador_principal(db: Session, empresa_id: int):
    return (
        db.query(Usuario)
        .filter(
            Usuario.empresa_id == empresa_id,
            Usuario.perfil == "admin",
            Usuario.ativo.is_(True),
        )
        .order_by(Usuario.created_at, Usuario.id)
        .first()
    )


def _resumo_empresa(db: Session, empresa: Empresa):
    modulos_ativos = (
        db.query(func.count(EmpresaModulo.id))
        .filter(
            EmpresaModulo.empresa_id == empresa.id,
            EmpresaModulo.ativo.is_(True),
        )
        .scalar()
        or 0
    )
    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "identidade_codigo": empresa.identidade_codigo,
        "cnpj": empresa.cnpj,
        "email": empresa.email,
        "telefone": empresa.telefone,
        "logo_url": empresa.logo_url,
        "cor_primaria": empresa.cor_primaria,
        "cor_secundaria": empresa.cor_secundaria,
        "tema": empresa.tema,
        "tipo_negocio": empresa.tipo_negocio,
        "ativo": empresa.ativo,
        "created_at": empresa.created_at,
        "modulos_ativos": int(modulos_ativos),
        "administrador_principal": _administrador_principal(db, empresa.id),
        "protegido": _empresa_protegida(empresa),
    }


def listar_empresas_matriz(
    db: Session,
    *,
    busca: str | None = None,
    status: str | None = None,
    tipo_negocio: str | None = None,
):
    consulta = db.query(Empresa).order_by(Empresa.created_at.desc(), Empresa.id.desc())
    if busca:
        termo = f"%{busca.strip()}%"
        consulta = consulta.filter(
            (Empresa.nome.ilike(termo))
            | (Empresa.email.ilike(termo))
            | (Empresa.cnpj.ilike(termo))
        )
    if status == "ativo":
        consulta = consulta.filter(Empresa.ativo.is_(True))
    elif status == "inativo":
        consulta = consulta.filter(Empresa.ativo.is_(False))
    if tipo_negocio:
        consulta = consulta.filter(Empresa.tipo_negocio == tipo_negocio)
    return [_resumo_empresa(db, empresa) for empresa in consulta.all()]


def listar_auditoria_matriz(
    db: Session,
    *,
    empresa_id: int | None = None,
    acao: str | None = None,
    limite: int = 50,
):
    consulta = (
        db.query(RegistroAuditoria, Empresa.nome, Usuario.nome)
        .join(Empresa, Empresa.id == RegistroAuditoria.empresa_id)
        .outerjoin(Usuario, Usuario.id == RegistroAuditoria.usuario_id)
        .order_by(RegistroAuditoria.criado_em.desc(), RegistroAuditoria.id.desc())
    )
    if empresa_id is not None:
        consulta = consulta.filter(RegistroAuditoria.empresa_id == empresa_id)
    if acao:
        consulta = consulta.filter(RegistroAuditoria.acao == acao)
    return [
        {
            "id": registro.id,
            "empresa_id": registro.empresa_id,
            "empresa_nome": empresa_nome,
            "usuario_id": registro.usuario_id,
            "usuario_nome": usuario_nome,
            "acao": registro.acao,
            "recurso": registro.recurso,
            "recurso_id": registro.recurso_id,
            "detalhes": registro.detalhes,
            "criado_em": registro.criado_em,
        }
        for registro, empresa_nome, usuario_nome in consulta.limit(limite).all()
    ]


def obter_dashboard_matriz(db: Session):
    empresas = db.query(Empresa).order_by(Empresa.created_at.desc(), Empresa.id.desc()).all()
    modulos_mais_utilizados = []
    for modulo in db.query(Modulo).order_by(Modulo.ordem, Modulo.nome).all():
        empresas_ativas = (
            db.query(func.count(EmpresaModulo.empresa_id))
            .join(Empresa, Empresa.id == EmpresaModulo.empresa_id)
            .filter(
                EmpresaModulo.modulo_id == modulo.id,
                EmpresaModulo.ativo.is_(True),
                Empresa.ativo.is_(True),
            )
            .scalar()
            or 0
        )
        modulos_mais_utilizados.append(
            {
                "codigo": modulo.codigo,
                "nome": modulo.nome,
                "empresas_ativas": int(empresas_ativas),
                "ativo": True,
            }
        )

    alertas = [
        {
            "severidade": "warning",
            "titulo": "Empresa inativa",
            "descricao": f"{empresa.nome} não recebe novas operações enquanto estiver inativa.",
            "empresa_id": empresa.id,
        }
        for empresa in empresas
        if not empresa.ativo
    ][:5]

    return {
        "total_empresas": len(empresas),
        "empresas_ativas": sum(1 for empresa in empresas if empresa.ativo),
        "empresas_inativas": sum(1 for empresa in empresas if not empresa.ativo),
        "modulos_mais_utilizados": sorted(
            modulos_mais_utilizados,
            key=lambda modulo: (-modulo["empresas_ativas"], modulo["nome"]),
        ),
        "empresas_recentes": [_resumo_empresa(db, empresa) for empresa in empresas[:5]],
        "alertas": alertas,
        "ultimas_auditorias": listar_auditoria_matriz(db, limite=8),
    }


def listar_catalogo_modulos_matriz(db: Session):
    return db.query(Modulo).order_by(Modulo.ordem, Modulo.nome).all()


def obter_detalhe_empresa_matriz(db: Session, empresa_id: int):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    usuarios = (
        db.query(Usuario)
        .filter(Usuario.empresa_id == empresa_id)
        .order_by(Usuario.ativo.desc(), Usuario.nome)
        .all()
    )
    return {
        "empresa": _resumo_empresa(db, empresa),
        "modulos": listar_modulos_empresa(db, empresa_id),
        "usuarios": usuarios,
        "auditoria": listar_auditoria_matriz(db, empresa_id=empresa_id, limite=30),
    }


def atualizar_identidade_empresa_matriz(
    db: Session,
    empresa_id: int,
    dados: MatrizIdentidadeUpdate,
    usuario_id: int,
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    if _empresa_protegida(empresa):
        raise HTTPException(
            status_code=409,
            detail="A identidade da HYPE STUDIO está protegida nesta etapa.",
        )

    valores = dados.model_dump(exclude_unset=True)
    if "nome_exibicao" in valores:
        empresa.nome = valores.pop("nome_exibicao").strip()
    if "identidade_codigo" in valores:
        identidade = resolver_identidade_codigo(
            valores.pop("identidade_codigo"),
            nome=empresa.nome,
            email=empresa.email,
        )
        if not identidade:
            raise HTTPException(status_code=400, detail="Identidade visual inválida.")
        if identidade == IDENTIDADE_HYPE:
            raise HTTPException(
                status_code=400,
                detail="A identidade HYPE STUDIO é reservada ao tenant real existente.",
            )
        empresa.identidade_codigo = identidade
    for campo, valor in valores.items():
        setattr(empresa, campo, valor.strip() if isinstance(valor, str) and valor else valor)

    registrar_auditoria(
        db,
        empresa_id=empresa.id,
        usuario_id=usuario_id,
        acao="ATUALIZAR_IDENTIDADE",
        recurso="empresa",
        recurso_id=empresa.id,
        detalhes={"campos": sorted(dados.model_dump(exclude_unset=True).keys())},
        commit=False,
    )
    db.commit()
    db.refresh(empresa)
    return _resumo_empresa(db, empresa)


def atualizar_modulo_empresa_matriz(
    db: Session,
    empresa_id: int,
    codigo: str,
    ativo: bool,
    usuario_id: int,
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    if _empresa_protegida(empresa):
        raise HTTPException(
            status_code=409,
            detail="Os módulos da HYPE STUDIO estão protegidos nesta etapa.",
        )
    resposta = atualizar_modulo_empresa(db, empresa_id, codigo, ativo)
    registrar_auditoria(
        db,
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        acao="ATIVAR_MODULO" if ativo else "DESATIVAR_MODULO",
        recurso="modulo",
        detalhes={"codigo": codigo, "origem": "matriz_pegs"},
    )
    return resposta


def atualizar_usuario_empresa_matriz(
    db: Session,
    empresa_id: int,
    usuario_id_alvo: int,
    dados: MatrizUsuarioUpdate,
    usuario_responsavel_id: int,
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    if _empresa_protegida(empresa):
        raise HTTPException(
            status_code=409,
            detail="Os usuários da HYPE STUDIO estão protegidos nesta etapa.",
        )
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id_alvo, Usuario.empresa_id == empresa_id)
        .first()
    )
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    valores = dados.model_dump(exclude_unset=True)
    perfil = valores.get("perfil")
    if perfil == "pegs_admin" or getattr(perfil, "value", None) == "pegs_admin":
        raise HTTPException(status_code=400, detail="pegs_admin pertence somente à Matriz Pegs.")
    if "email" in valores:
        valores["email"] = str(valores["email"]).lower()
    if "perfil" in valores and hasattr(valores["perfil"], "value"):
        valores["perfil"] = valores["perfil"].value
    for campo, valor in valores.items():
        setattr(usuario, campo, valor)

    registrar_auditoria(
        db,
        empresa_id=empresa_id,
        usuario_id=usuario_responsavel_id,
        acao="ATUALIZAR_USUARIO",
        recurso="usuario",
        recurso_id=usuario.id,
        detalhes={"campos": sorted(valores.keys())},
        commit=False,
    )
    db.commit()
    db.refresh(usuario)
    return usuario
