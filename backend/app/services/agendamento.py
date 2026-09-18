from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import PerfilUsuario, StatusAgendamento
from app.models.agendamento import Agendamento
from app.repositories.agendamento import (
    buscar_agendamento_por_id,
    buscar_conflitos,
    criar_agendamento,
    listar_agendamentos,
    listar_recursos_livres,
)
from app.repositories.cliente import buscar_cliente_por_id
from app.repositories.profissional import (
    buscar_profissional_por_id,
    buscar_profissional_por_usuario,
)
from app.repositories.recurso_agenda import buscar_recurso_por_id
from app.repositories.servico import buscar_servico_por_id
from app.utils.recurso import tipos_recurso_compativeis
from app.utils.operacao import servico_compativel_com_area, servico_e_tattoo


PERFIS_AGENDA = {
    PerfilUsuario.ADMIN.value,
    PerfilUsuario.GERENTE.value,
    PerfilUsuario.PROFISSIONAL.value,
}
STATUS_ATIVOS = {
    StatusAgendamento.AGENDADO.value,
    StatusAgendamento.CONFIRMADO.value,
    StatusAgendamento.CONCLUIDO.value,
}


def _validar_perfil(usuario) -> None:
    if usuario.perfil not in PERFIS_AGENDA:
        raise HTTPException(
            status_code=403,
            detail="Sem permissao para acessar a agenda.",
        )


def _profissional_do_usuario(db: Session, usuario):
    profissional = buscar_profissional_por_usuario(
        db, usuario.id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(
            status_code=403,
            detail="Usuario sem profissional vinculado.",
        )
    return profissional


def _resolver_profissional(db: Session, dados, usuario, atual=None):
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        profissional = _profissional_do_usuario(db, usuario)
        informado = dados.get("profissional_id")
        if informado is not None and informado != profissional.id:
            raise HTTPException(
                status_code=403,
                detail="Profissional so pode agendar para si proprio.",
            )
        return profissional

    profissional_id = dados.get(
        "profissional_id",
        atual.profissional_id if atual is not None else None,
    )
    if profissional_id is None:
        raise HTTPException(
            status_code=400,
            detail="profissional_id e obrigatorio para admin e gerente.",
        )
    profissional = buscar_profissional_por_id(
        db, profissional_id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado.")
    if not profissional.ativo:
        raise HTTPException(status_code=400, detail="Profissional inativo.")
    return profissional


def _resolver_servico(db: Session, servico_id: int, empresa_id: int):
    servico = buscar_servico_por_id(db, servico_id, empresa_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico nao encontrado.")
    if not servico.ativo:
        raise HTTPException(status_code=400, detail="Servico inativo.")
    if servico.duracao_minutos <= 0:
        raise HTTPException(status_code=400, detail="Servico sem duracao valida.")
    return servico


def _validar_servico_para_profissional(servico, profissional, usuario):
    if usuario.perfil != PerfilUsuario.PROFISSIONAL.value:
        return
    if not servico_compativel_com_area(
        profissional.area_atuacao,
        servico.categoria,
        servico.nome,
    ):
        raise HTTPException(
            status_code=403,
            detail="Este servico pertence a outra area de atuacao.",
        )


def _resolver_preco(servico, profissional, dados, usuario, atual=None):
    if "preco_aplicado" not in dados:
        if atual is not None and "servico_id" not in dados:
            return atual.preco_aplicado
        return Decimal(servico.preco_padrao)

    preco = dados.get("preco_aplicado")
    if preco is None:
        raise HTTPException(status_code=400, detail="O valor do atendimento nao pode ser vazio.")
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value and not servico_e_tattoo(servico.categoria, servico.nome):
        raise HTTPException(
            status_code=403,
            detail="Somente tattoos permitem que o profissional informe um valor no agendamento.",
        )
    return Decimal(str(preco))


def _normalizar_cliente(db: Session, dados: dict, empresa_id: int, atual=None):
    cliente_id = dados.get(
        "cliente_id",
        atual.cliente_id if atual is not None else None,
    )
    nome_avulso = dados.get(
        "cliente_avulso_nome",
        atual.cliente_avulso_nome if atual is not None else None,
    )
    if cliente_id is not None and nome_avulso:
        raise HTTPException(
            status_code=400,
            detail="Escolha um cliente cadastrado ou um cliente avulso.",
        )
    if cliente_id is not None:
        cliente = buscar_cliente_por_id(db, cliente_id, empresa_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente nao encontrado.")
        return cliente_id, None
    return None, nome_avulso.strip() if isinstance(nome_avulso, str) else None


def _resolver_periodo(inicio_em, duracao_minutos, atual=None):
    if inicio_em is None and atual is not None:
        inicio_em = atual.inicio_em
    if inicio_em is None:
        raise HTTPException(status_code=400, detail="inicio_em e obrigatorio.")
    if duracao_minutos is None and atual is not None:
        duracao_minutos = int(
            (atual.fim_em - atual.inicio_em).total_seconds() // 60
        )
    if duracao_minutos is None:
        raise HTTPException(status_code=400, detail="Duracao nao definida.")
    if duracao_minutos <= 0 or duracao_minutos > 1440:
        raise HTTPException(status_code=400, detail="Duracao invalida.")
    return inicio_em, inicio_em + timedelta(minutes=duracao_minutos)


def _validar_recurso(db, servico, dados, usuario, inicio_em, fim_em, atual=None):
    recurso_id_informado = dados.get("recurso_id")
    if not servico.requer_recurso:
        if recurso_id_informado is not None:
            raise HTTPException(
                status_code=400,
                detail="Este servico nao exige um recurso.",
            )
        return None

    if not servico.tipo_recurso:
        raise HTTPException(
            status_code=400,
            detail="Servico sem tipo de recurso configurado.",
        )

    modo = servico.modo_selecao_recurso or "AUTOMATICO"
    usar_recurso_manual = bool(dados.get("usar_recurso_manual")) or modo == "MANUAL"
    if usar_recurso_manual:
        if recurso_id_informado is None:
            if atual is not None and atual.recurso_id is not None:
                recurso_id_informado = atual.recurso_id
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Escolha um recurso para este servico.",
                )
        recurso = buscar_recurso_por_id(
            db, recurso_id_informado, usuario.empresa_id
        )
        if not recurso or not recurso.disponivel:
            raise HTTPException(
                status_code=409,
                detail="O recurso esta inativo ou em manutencao.",
            )
        if not tipos_recurso_compativeis(recurso.tipo, servico.tipo_recurso):
            raise HTTPException(
                status_code=400,
                detail="O recurso escolhido nao atende ao tipo do servico.",
            )
        return recurso

    if recurso_id_informado is not None:
        raise HTTPException(
            status_code=400,
            detail="Este servico seleciona o recurso automaticamente.",
        )
    livres = listar_recursos_livres(
        db,
        usuario.empresa_id,
        servico.tipo_recurso,
        inicio_em,
        fim_em,
    )
    if atual is not None and atual.recurso_id is not None:
        atual_recurso = buscar_recurso_por_id(
            db, atual.recurso_id, usuario.empresa_id
        )
        if (
            atual_recurso
            and atual_recurso.disponivel
            and tipos_recurso_compativeis(atual_recurso.tipo, servico.tipo_recurso)
            and all(recurso.id != atual_recurso.id for recurso in livres)
        ):
            conflitos = buscar_conflitos(
                db,
                usuario.empresa_id,
                atual.profissional_id,
                inicio_em,
                fim_em,
                atual_recurso.id,
                atual.id,
            )
            if not conflitos:
                return atual_recurso
        elif atual_recurso and atual_recurso.disponivel and any(
            recurso.id == atual_recurso.id for recurso in livres
        ):
            return atual_recurso
    if not livres:
        raise HTTPException(
            status_code=409,
            detail="Nao ha recurso disponivel neste horario.",
        )
    return livres[0]


def _validar_conflitos(
    db,
    usuario,
    profissional_id,
    inicio_em,
    fim_em,
    recurso_id,
    ignorar_id=None,
):
    conflitos = buscar_conflitos(
        db,
        usuario.empresa_id,
        profissional_id,
        inicio_em,
        fim_em,
        recurso_id,
        ignorar_id,
    )
    if not conflitos:
        return
    conflito_recurso = recurso_id is not None and any(
        item.recurso_id == recurso_id for item in conflitos
    )
    if conflito_recurso:
        raise HTTPException(
            status_code=409,
            detail="O profissional ou recurso ja esta reservado neste horario.",
        )
    raise HTTPException(
        status_code=409,
        detail="O profissional ja possui um agendamento neste horario.",
    )


def criar_agendamento_service(db: Session, dados, usuario):
    _validar_perfil(usuario)
    dados_dict = dados.model_dump(exclude_unset=True)
    profissional = _resolver_profissional(db, dados_dict, usuario)
    servico = _resolver_servico(
        db, dados_dict["servico_id"], usuario.empresa_id
    )
    _validar_servico_para_profissional(servico, profissional, usuario)
    cliente_id, cliente_avulso_nome = _normalizar_cliente(
        db, dados_dict, usuario.empresa_id
    )
    duracao = dados_dict.get("duracao_minutos", servico.duracao_minutos)
    inicio_em, fim_em = _resolver_periodo(dados_dict.get("inicio_em"), duracao)
    recurso = _validar_recurso(
        db, servico, dados_dict, usuario, inicio_em, fim_em
    )
    preco_aplicado = _resolver_preco(servico, profissional, dados_dict, usuario)
    _validar_conflitos(
        db,
        usuario,
        profissional.id,
        inicio_em,
        fim_em,
        recurso.id if recurso else None,
    )

    try:
        agendamento = criar_agendamento(
            db,
            empresa_id=usuario.empresa_id,
            profissional_id=profissional.id,
            servico_id=servico.id,
            cliente_id=cliente_id,
            cliente_avulso_nome=cliente_avulso_nome,
            recurso_id=recurso.id if recurso else None,
            criado_por_usuario_id=usuario.id,
            inicio_em=inicio_em,
            fim_em=fim_em,
            duracao_minutos=int(duracao),
            preco_aplicado=preco_aplicado,
            status=StatusAgendamento.AGENDADO.value,
            observacao=dados_dict.get("observacao"),
        )
        db.commit()
        db.refresh(agendamento)
        return agendamento
    except Exception:
        db.rollback()
        raise


def _pode_alterar(agendamento: Agendamento, usuario) -> bool:
    if usuario.perfil in {
        PerfilUsuario.ADMIN.value,
        PerfilUsuario.GERENTE.value,
    }:
        return True
    return (
        usuario.perfil == PerfilUsuario.PROFISSIONAL.value
        and agendamento.criado_por_usuario_id == usuario.id
    )


def atualizar_agendamento_service(db: Session, agendamento_id: int, dados, usuario):
    _validar_perfil(usuario)
    agendamento = buscar_agendamento_por_id(
        db, agendamento_id, usuario.empresa_id
    )
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento nao encontrado.")
    if not _pode_alterar(agendamento, usuario):
        raise HTTPException(
            status_code=403,
            detail="Voce so pode alterar agendamentos reservados por voce.",
        )

    dados_dict = dados.model_dump(exclude_unset=True)
    profissional = _resolver_profissional(
        db, dados_dict, usuario, atual=agendamento
    )
    servico_id = dados_dict.get("servico_id", agendamento.servico_id)
    servico = _resolver_servico(db, servico_id, usuario.empresa_id)
    _validar_servico_para_profissional(servico, profissional, usuario)
    cliente_id, cliente_avulso_nome = _normalizar_cliente(
        db, dados_dict, usuario.empresa_id, atual=agendamento
    )
    duracao = dados_dict.get("duracao_minutos")
    if duracao is None:
        duracao = (
            servico.duracao_minutos
            if "servico_id" in dados_dict
            else agendamento.duracao_minutos
        )
    inicio_em, fim_em = _resolver_periodo(
        dados_dict.get("inicio_em"), duracao, atual=agendamento
    )
    recurso = _validar_recurso(
        db,
        servico,
        dados_dict,
        usuario,
        inicio_em,
        fim_em,
        atual=agendamento,
    )
    preco_aplicado = _resolver_preco(
        servico,
        profissional,
        dados_dict,
        usuario,
        atual=agendamento,
    )
    status = dados_dict.get("status", agendamento.status)
    status = status.value if isinstance(status, StatusAgendamento) else status
    motivo = dados_dict.get(
        "motivo_cancelamento", agendamento.motivo_cancelamento
    )
    if status == StatusAgendamento.CANCELADO.value:
        cancelado_em = datetime.now(timezone.utc)
        cancelado_por = usuario.id
    else:
        cancelado_em = None
        cancelado_por = None
        motivo = None

    if status in STATUS_ATIVOS:
        _validar_conflitos(
            db,
            usuario,
            profissional.id,
            inicio_em,
            fim_em,
            recurso.id if recurso else None,
            ignorar_id=agendamento.id,
        )

    try:
        agendamento.profissional_id = profissional.id
        agendamento.servico_id = servico.id
        agendamento.cliente_id = cliente_id
        agendamento.cliente_avulso_nome = cliente_avulso_nome
        agendamento.recurso_id = recurso.id if recurso else None
        agendamento.inicio_em = inicio_em
        agendamento.fim_em = fim_em
        agendamento.duracao_minutos = int(duracao)
        agendamento.preco_aplicado = preco_aplicado
        agendamento.status = status
        agendamento.observacao = dados_dict.get(
            "observacao", agendamento.observacao
        )
        agendamento.motivo_cancelamento = motivo
        agendamento.cancelado_em = cancelado_em
        agendamento.cancelado_por_usuario_id = cancelado_por
        db.commit()
        db.refresh(agendamento)
        return agendamento
    except Exception:
        db.rollback()
        raise


def _resposta_agendamento(agendamento: Agendamento, usuario, area_atuacao=None):
    profissional_restrito = usuario.perfil == PerfilUsuario.PROFISSIONAL.value
    e_proprio = (
        not profissional_restrito
        or agendamento.criado_por_usuario_id == usuario.id
        or agendamento.profissional.usuario_id == usuario.id
    )
    if profissional_restrito and not e_proprio:
        if not servico_compativel_com_area(
            area_atuacao,
            agendamento.servico.categoria if agendamento.servico else None,
            agendamento.servico.nome if agendamento.servico else None,
        ):
            return None
        if agendamento.recurso_id is None or agendamento.status not in STATUS_ATIVOS:
            return None
        return {
            "id": agendamento.id,
            "empresa_id": agendamento.empresa_id,
            "profissional_id": None,
            "servico_id": None,
            "cliente_id": None,
            "cliente_nome": None,
            "cliente_avulso_nome": None,
            "recurso_id": agendamento.recurso_id,
            "recurso_nome": agendamento.recurso.nome if agendamento.recurso else None,
            "inicio_em": agendamento.inicio_em,
            "fim_em": agendamento.fim_em,
            "duracao_minutos": int(
                (agendamento.fim_em - agendamento.inicio_em).total_seconds() // 60
            ),
            "preco_aplicado": None,
            "status": agendamento.status,
            "observacao": None,
            "motivo_cancelamento": None,
            "criado_por_usuario_id": None,
            "detalhes_restritos": True,
            "created_at": agendamento.created_at,
            "updated_at": agendamento.updated_at,
        }
    return {
        "id": agendamento.id,
        "empresa_id": agendamento.empresa_id,
        "profissional_id": agendamento.profissional_id,
        "servico_id": agendamento.servico_id,
        "cliente_id": agendamento.cliente_id,
        "cliente_nome": agendamento.cliente.nome if agendamento.cliente else None,
        "cliente_avulso_nome": agendamento.cliente_avulso_nome,
        "recurso_id": agendamento.recurso_id,
        "recurso_nome": agendamento.recurso.nome if agendamento.recurso else None,
        "inicio_em": agendamento.inicio_em,
        "fim_em": agendamento.fim_em,
        "duracao_minutos": int(
            agendamento.duracao_minutos
        ),
        "preco_aplicado": agendamento.preco_aplicado,
        "status": agendamento.status,
        "observacao": agendamento.observacao,
        "motivo_cancelamento": agendamento.motivo_cancelamento,
        "criado_por_usuario_id": agendamento.criado_por_usuario_id,
        "detalhes_restritos": False,
        "created_at": agendamento.created_at,
        "updated_at": agendamento.updated_at,
    }


def listar_agendamentos_service(db: Session, usuario, **filtros):
    _validar_perfil(usuario)
    area_atuacao = None
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        profissional = _profissional_do_usuario(db, usuario)
        area_atuacao = profissional.area_atuacao
        solicitado = filtros.get("profissional_id")
        if solicitado is not None and solicitado != profissional.id:
            raise HTTPException(
                status_code=403,
                detail="Profissional so pode consultar sua propria agenda.",
            )
    itens = listar_agendamentos(db, usuario.empresa_id, **filtros)
    respostas = []
    for item in itens:
        resposta = _resposta_agendamento(item, usuario, area_atuacao)
        if resposta is not None:
            respostas.append(resposta)
    return respostas


def buscar_agendamento_service(db: Session, agendamento_id: int, usuario):
    _validar_perfil(usuario)
    item = buscar_agendamento_por_id(db, agendamento_id, usuario.empresa_id)
    if not item:
        return None
    area_atuacao = None
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        area_atuacao = _profissional_do_usuario(db, usuario).area_atuacao
    return _resposta_agendamento(item, usuario, area_atuacao)
