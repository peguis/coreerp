from __future__ import annotations

from datetime import date, datetime, timezone

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.enums import PerfilUsuario
from app.models.empresa import Empresa
from app.models.modulo import EmpresaModulo, Modulo
from app.models.oportunidade import Oportunidade, OportunidadeInteracao
from app.models.usuario import Usuario
from app.schemas.empresa import MatrizDemonstracaoCreate
from app.schemas.matriz import (
    MatrizAprovarConversao,
    MatrizInteracaoCreate,
    MatrizOportunidadeCreate,
    MatrizOportunidadeUpdate,
)
from app.services.auditoria import registrar_auditoria
from app.services.empresa import provisionar_empresa_service


STATUS_OPORTUNIDADE = {
    "NOVO",
    "CONTATO_PENDENTE",
    "EM_DEMONSTRACAO",
    "PROPOSTA_ENVIADA",
    "CONVERTIDO",
    "RECUSADO",
    "PERDIDO",
}


def _is_admin(usuario: Usuario) -> bool:
    return usuario.perfil == PerfilUsuario.PEGS_ADMIN.value


def _obter_empresa_matriz(db: Session, usuario: Usuario) -> Empresa:
    empresa = db.query(Empresa).filter(Empresa.id == usuario.empresa_id).first()
    if not empresa or (usuario.perfil == PerfilUsuario.VENDEDOR_PEGS.value and not empresa.eh_matriz):
        raise HTTPException(status_code=403, detail="Acesso restrito à Matriz Pegs.")
    return empresa


def _validar_status(status: str | None) -> str:
    valor = (status or "NOVO").strip().upper()
    if valor not in STATUS_OPORTUNIDADE:
        raise HTTPException(status_code=400, detail="Status comercial inválido.")
    return valor


def _obter_vendedor(db: Session, vendedor_id: int, empresa_matriz_id: int) -> Usuario:
    vendedor = (
        db.query(Usuario)
        .filter(
            Usuario.id == vendedor_id,
            Usuario.empresa_id == empresa_matriz_id,
            Usuario.perfil == PerfilUsuario.VENDEDOR_PEGS.value,
            Usuario.ativo.is_(True),
        )
        .first()
    )
    if not vendedor:
        raise HTTPException(status_code=400, detail="Vendedor Pegs não encontrado ou inativo.")
    return vendedor


def _obter_demo(
    db: Session,
    usuario: Usuario,
    tenant_demo_id: int,
) -> Empresa:
    demo = (
        db.query(Empresa)
        .filter(Empresa.id == tenant_demo_id, Empresa.eh_demo.is_(True))
        .first()
    )
    if not demo:
        raise HTTPException(status_code=404, detail="Tenant de demonstração não encontrado.")
    if not _is_admin(usuario) and demo.criado_por_usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não pode acessar esta demonstração.")
    return demo


def _obter_oportunidade(db: Session, usuario: Usuario, oportunidade_id: int) -> Oportunidade:
    consulta = db.query(Oportunidade).filter(
        Oportunidade.id == oportunidade_id,
        Oportunidade.empresa_id == usuario.empresa_id,
    )
    if not _is_admin(usuario):
        consulta = consulta.filter(Oportunidade.vendedor_id == usuario.id)
    oportunidade = consulta.first()
    if not oportunidade:
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada.")
    return oportunidade


def _interacao_dict(interacao: OportunidadeInteracao) -> dict:
    return {
        "id": interacao.id,
        "usuario_id": interacao.usuario_id,
        "usuario_nome": interacao.usuario.nome if interacao.usuario else None,
        "descricao": interacao.descricao,
        "proxima_acao": interacao.proxima_acao,
        "proximo_contato": interacao.proximo_contato,
        "criado_em": interacao.criado_em,
    }


def _oportunidade_dict(oportunidade: Oportunidade) -> dict:
    demo = oportunidade.tenant_demo
    return {
        "id": oportunidade.id,
        "empresa_id": oportunidade.empresa_id,
        "vendedor_id": oportunidade.vendedor_id,
        "vendedor_nome": oportunidade.vendedor.nome if oportunidade.vendedor else None,
        "nome_negocio_contato": oportunidade.nome_negocio_contato,
        "pessoa_responsavel": oportunidade.pessoa_responsavel,
        "telefone": oportunidade.telefone,
        "email": oportunidade.email,
        "canal_contato": oportunidade.canal_contato,
        "cidade_regiao": oportunidade.cidade_regiao,
        "tipo_negocio": oportunidade.tipo_negocio,
        "origem": oportunidade.origem,
        "status": oportunidade.status,
        "proxima_acao": oportunidade.proxima_acao,
        "proximo_contato": oportunidade.proximo_contato,
        "observacoes": oportunidade.observacoes,
        "modulos_interesse": oportunidade.modulos_interesse or [],
        "tenant_demo_id": oportunidade.tenant_demo_id,
        "tenant_demo_nome": demo.nome if demo else None,
        "tenant_demo_ativo": demo.ativo if demo else None,
        "tenant_demo_eh_demo": demo.eh_demo if demo else None,
        "ultima_interacao_em": oportunidade.ultima_interacao_em,
        "conversao_solicitada_em": oportunidade.conversao_solicitada_em,
        "convertido_em": oportunidade.convertido_em,
        "criado_em": oportunidade.criado_em,
        "interacoes": [_interacao_dict(item) for item in oportunidade.interacoes],
    }


def listar_vendedores_matriz(db: Session, usuario: Usuario):
    empresa_matriz = _obter_empresa_matriz(db, usuario)
    consulta = db.query(Usuario).filter(
        Usuario.empresa_id == empresa_matriz.id,
        Usuario.perfil == PerfilUsuario.VENDEDOR_PEGS.value,
        Usuario.ativo.is_(True),
    )
    if not _is_admin(usuario):
        consulta = consulta.filter(Usuario.id == usuario.id)
    return [
        {"id": item.id, "nome": item.nome, "email": item.email, "ativo": item.ativo}
        for item in consulta.order_by(Usuario.nome).all()
    ]


def listar_oportunidades_matriz(
    db: Session,
    usuario: Usuario,
    *,
    busca: str | None = None,
    vendedor_id: int | None = None,
    status: str | None = None,
    proxima_acao: str | None = None,
    proximo_contato: date | None = None,
):
    _obter_empresa_matriz(db, usuario)
    consulta = db.query(Oportunidade).filter(Oportunidade.empresa_id == usuario.empresa_id)
    if not _is_admin(usuario):
        consulta = consulta.filter(Oportunidade.vendedor_id == usuario.id)
    elif vendedor_id is not None:
        consulta = consulta.filter(Oportunidade.vendedor_id == vendedor_id)
    if busca:
        termo = f"%{busca.strip()}%"
        consulta = consulta.filter(
            or_(
                Oportunidade.nome_negocio_contato.ilike(termo),
                Oportunidade.pessoa_responsavel.ilike(termo),
                Oportunidade.telefone.ilike(termo),
                Oportunidade.email.ilike(termo),
            )
        )
    if status:
        consulta = consulta.filter(Oportunidade.status == _validar_status(status))
    if proxima_acao:
        consulta = consulta.filter(Oportunidade.proxima_acao.ilike(f"%{proxima_acao.strip()}%"))
    if proximo_contato:
        consulta = consulta.filter(Oportunidade.proximo_contato == proximo_contato)
    return [
        _oportunidade_dict(item)
        for item in consulta.order_by(Oportunidade.criado_em.desc(), Oportunidade.id.desc()).all()
    ]


def criar_oportunidade_matriz(
    db: Session,
    usuario: Usuario,
    dados: MatrizOportunidadeCreate,
):
    empresa_matriz = _obter_empresa_matriz(db, usuario)
    vendedor_id = usuario.id if not _is_admin(usuario) else dados.vendedor_id
    if not vendedor_id:
        raise HTTPException(status_code=400, detail="Informe o vendedor responsável.")
    vendedor = _obter_vendedor(db, vendedor_id, empresa_matriz.id)
    if not _is_admin(usuario) and vendedor.id != usuario.id:
        raise HTTPException(status_code=403, detail="Você só pode criar oportunidades próprias.")
    if dados.tenant_demo_id is not None:
        _obter_demo(db, usuario, dados.tenant_demo_id)
    oportunidade = Oportunidade(
        empresa_id=empresa_matriz.id,
        vendedor_id=vendedor.id,
        nome_negocio_contato=dados.nome_negocio_contato.strip(),
        pessoa_responsavel=dados.pessoa_responsavel.strip() if dados.pessoa_responsavel else None,
        telefone=dados.telefone.strip() if dados.telefone else None,
        email=dados.email.strip().lower() if dados.email else None,
        canal_contato=dados.canal_contato.strip() if dados.canal_contato else None,
        cidade_regiao=dados.cidade_regiao.strip() if dados.cidade_regiao else None,
        tipo_negocio=dados.tipo_negocio.strip() if dados.tipo_negocio else None,
        origem=dados.origem.strip() if dados.origem else None,
        status=_validar_status(dados.status),
        proxima_acao=dados.proxima_acao.strip() if dados.proxima_acao else None,
        proximo_contato=dados.proximo_contato,
        observacoes=dados.observacoes.strip() if dados.observacoes else None,
        modulos_interesse=dados.modulos_interesse,
        tenant_demo_id=dados.tenant_demo_id,
    )
    db.add(oportunidade)
    db.flush()
    registrar_auditoria(
        db,
        empresa_id=empresa_matriz.id,
        usuario_id=usuario.id,
        acao="CRIAR_OPORTUNIDADE",
        recurso="oportunidade",
        recurso_id=oportunidade.id,
        detalhes={"vendedor_id": vendedor.id},
        commit=False,
    )
    db.commit()
    db.refresh(oportunidade)
    return _oportunidade_dict(oportunidade)


def atualizar_oportunidade_matriz(
    db: Session,
    usuario: Usuario,
    oportunidade_id: int,
    dados: MatrizOportunidadeUpdate,
):
    oportunidade = _obter_oportunidade(db, usuario, oportunidade_id)
    valores = dados.model_dump(exclude_unset=True)
    if "status" in valores:
        valores["status"] = _validar_status(valores["status"])
    if "vendedor_id" in valores:
        if not _is_admin(usuario):
            raise HTTPException(status_code=403, detail="Somente a Matriz pode redistribuir oportunidades.")
        vendedor = _obter_vendedor(db, valores["vendedor_id"], usuario.empresa_id)
        valores["vendedor_id"] = vendedor.id
    if "tenant_demo_id" in valores and valores["tenant_demo_id"] is not None:
        _obter_demo(db, usuario, valores["tenant_demo_id"])
    for campo, valor in valores.items():
        if isinstance(valor, str):
            valor = valor.strip() or None
        setattr(oportunidade, campo, valor)
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="ATUALIZAR_OPORTUNIDADE",
        recurso="oportunidade",
        recurso_id=oportunidade.id,
        detalhes={"campos": sorted(valores.keys())},
        commit=False,
    )
    db.commit()
    db.refresh(oportunidade)
    return _oportunidade_dict(oportunidade)


def registrar_interacao_matriz(
    db: Session,
    usuario: Usuario,
    oportunidade_id: int,
    dados: MatrizInteracaoCreate,
):
    oportunidade = _obter_oportunidade(db, usuario, oportunidade_id)
    interacao = OportunidadeInteracao(
        oportunidade_id=oportunidade.id,
        usuario_id=usuario.id,
        descricao=dados.descricao.strip(),
        proxima_acao=dados.proxima_acao.strip() if dados.proxima_acao else None,
        proximo_contato=dados.proximo_contato,
    )
    db.add(interacao)
    oportunidade.ultima_interacao_em = datetime.now(timezone.utc)
    if dados.proxima_acao is not None:
        oportunidade.proxima_acao = dados.proxima_acao.strip() or None
    if dados.proximo_contato is not None:
        oportunidade.proximo_contato = dados.proximo_contato
    if dados.status is not None:
        oportunidade.status = _validar_status(dados.status)
    db.flush()
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="REGISTRAR_INTERACAO_OPORTUNIDADE",
        recurso="oportunidade",
        recurso_id=oportunidade.id,
        detalhes={"interacao_id": interacao.id, "status": oportunidade.status},
        commit=False,
    )
    db.commit()
    db.refresh(oportunidade)
    return _oportunidade_dict(oportunidade)


def criar_demonstracao_matriz(
    db: Session,
    usuario: Usuario,
    dados: MatrizDemonstracaoCreate,
):
    _obter_empresa_matriz(db, usuario)
    vendedor_id = usuario.id if not _is_admin(usuario) else dados.vendedor_id
    if vendedor_id is not None:
        _obter_vendedor(db, vendedor_id, usuario.empresa_id)
    if dados.oportunidade_id is not None:
        oportunidade = _obter_oportunidade(db, usuario, dados.oportunidade_id)
        if vendedor_id is not None and oportunidade.vendedor_id != vendedor_id:
            raise HTTPException(status_code=400, detail="A oportunidade não pertence ao vendedor selecionado.")
        vendedor_id = oportunidade.vendedor_id

    empresa = provisionar_empresa_service(
        db,
        dados,
        usuario_id=usuario.id,
        eh_demo=True,
        criado_por_usuario_id=vendedor_id,
        origem="vendedor_pegs" if not _is_admin(usuario) else "matriz_pegs",
    )
    if dados.oportunidade_id is not None:
        oportunidade = _obter_oportunidade(db, usuario, dados.oportunidade_id)
        oportunidade.tenant_demo_id = empresa.id
        oportunidade.status = "EM_DEMONSTRACAO"
        registrar_auditoria(
            db,
            empresa_id=usuario.empresa_id,
            usuario_id=usuario.id,
            acao="VINCULAR_DEMONSTRACAO_OPORTUNIDADE",
            recurso="oportunidade",
            recurso_id=oportunidade.id,
            detalhes={"tenant_demo_id": empresa.id},
            commit=False,
        )
        db.commit()
    return obter_previa_demonstracao_matriz(db, usuario, empresa.id)


def obter_previa_demonstracao_matriz(db: Session, usuario: Usuario, empresa_id: int):
    demo = _obter_demo(db, usuario, empresa_id)
    modulos = (
        db.query(Modulo.codigo)
        .join(EmpresaModulo, EmpresaModulo.modulo_id == Modulo.id)
        .filter(EmpresaModulo.empresa_id == demo.id, EmpresaModulo.ativo.is_(True))
        .order_by(Modulo.ordem, Modulo.nome)
        .all()
    )
    criado_por = db.query(Usuario).filter(Usuario.id == demo.criado_por_usuario_id).first()
    return {
        "id": demo.id,
        "nome": demo.nome,
        "identidade_codigo": demo.identidade_codigo,
        "logo_url": demo.logo_url,
        "cor_primaria": demo.cor_primaria,
        "cor_secundaria": demo.cor_secundaria,
        "tipo_negocio": demo.tipo_negocio,
        "ativo": demo.ativo,
        "eh_demo": demo.eh_demo,
        "criado_por_usuario_id": demo.criado_por_usuario_id,
        "criado_por_usuario_nome": criado_por.nome if criado_por else None,
        "modulos_ativos": [codigo for (codigo,) in modulos],
    }


def solicitar_conversao_matriz(db: Session, usuario: Usuario, oportunidade_id: int):
    oportunidade = _obter_oportunidade(db, usuario, oportunidade_id)
    if oportunidade.status == "CONVERTIDO" or oportunidade.convertido_em:
        raise HTTPException(status_code=409, detail="Esta oportunidade já foi convertida.")
    if not oportunidade.tenant_demo_id:
        raise HTTPException(status_code=400, detail="Vincule uma demonstração antes de solicitar conversão.")
    _obter_demo(db, usuario, oportunidade.tenant_demo_id)
    oportunidade.conversao_solicitada_em = datetime.now(timezone.utc)
    oportunidade.conversao_solicitada_por_id = usuario.id
    oportunidade.status = "PROPOSTA_ENVIADA"
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="SOLICITAR_CONVERSAO_EMPRESA",
        recurso="oportunidade",
        recurso_id=oportunidade.id,
        detalhes={"tenant_demo_id": oportunidade.tenant_demo_id},
        commit=False,
    )
    db.commit()
    db.refresh(oportunidade)
    return _oportunidade_dict(oportunidade)


def aprovar_conversao_matriz(
    db: Session,
    usuario: Usuario,
    oportunidade_id: int,
    dados: MatrizAprovarConversao,
):
    if not _is_admin(usuario):
        raise HTTPException(status_code=403, detail="Somente pegs_admin pode aprovar empresas reais.")
    oportunidade = _obter_oportunidade(db, usuario, oportunidade_id)
    if not dados.confirmar:
        raise HTTPException(status_code=400, detail="Confirme a aprovação da conversão.")
    if not oportunidade.tenant_demo_id or not oportunidade.conversao_solicitada_em:
        raise HTTPException(status_code=400, detail="A oportunidade ainda não possui solicitação de conversão.")
    demo = db.query(Empresa).filter(Empresa.id == oportunidade.tenant_demo_id).first()
    if not demo or not demo.eh_demo:
        raise HTTPException(status_code=409, detail="O tenant relacionado não é uma demonstração ativa.")
    demo.eh_demo = False
    demo.ativo = True
    oportunidade.status = "CONVERTIDO"
    oportunidade.convertido_em = datetime.now(timezone.utc)
    oportunidade.convertido_por_id = usuario.id
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="CONVERTER_EMPRESA_REAL",
        recurso="empresa",
        recurso_id=demo.id,
        detalhes={"oportunidade_id": oportunidade.id, "tenant_demo_id": demo.id},
        commit=False,
    )
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="APROVAR_CONVERSAO_EMPRESA",
        recurso="oportunidade",
        recurso_id=oportunidade.id,
        detalhes={"empresa_id": demo.id},
        commit=False,
    )
    db.commit()
    db.refresh(oportunidade)
    return _oportunidade_dict(oportunidade)
