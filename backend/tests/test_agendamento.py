from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.jwt import criar_token
from app.database import Base, get_db
from app.main import app
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.empresa import Empresa
from app.models.profissional import Profissional
from app.models.recurso_agenda import RecursoAgenda
from app.models.servico import Servico
from app.models.usuario import Usuario


@pytest.fixture
def agenda_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    empresa = Empresa(
        nome="Empresa Agenda",
        cnpj="77777777777777",
        email="agenda@teste.local",
    )
    db.add(empresa)
    db.flush()

    usuarios = {}
    for chave, perfil in (
        ("admin", "admin"),
        ("gerente", "gerente"),
        ("prof1", "profissional"),
        ("prof2", "profissional"),
    ):
        usuario = Usuario(
            nome=chave.title(),
            email=f"{chave}@agenda.local",
            senha="nao usada",
            perfil=perfil,
            empresa_id=empresa.id,
        )
        usuarios[chave] = usuario
    db.add_all(usuarios.values())
    db.flush()

    profissionais = {
        "p1": Profissional(
            empresa_id=empresa.id,
            usuario_id=usuarios["prof1"].id,
            area_atuacao="TATTOO",
            percentual_padrao=50,
            ativo=True,
        ),
        "p2": Profissional(
            empresa_id=empresa.id,
            usuario_id=usuarios["prof2"].id,
            area_atuacao="TATTOO",
            percentual_padrao=50,
            ativo=True,
        ),
    }
    servicos = {
        "tattoo": Servico(
            empresa_id=empresa.id,
            nome="Tattoo",
            preco_padrao=100,
            duracao_minutos=90,
            requer_recurso=True,
            tipo_recurso="MACA",
            modo_selecao_recurso="AUTOMATICO",
            ativo=True,
        ),
        "tattoo_manual": Servico(
            empresa_id=empresa.id,
            nome="Tattoo manual",
            preco_padrao=100,
            duracao_minutos=60,
            requer_recurso=True,
            tipo_recurso="MACA",
            modo_selecao_recurso="MANUAL",
            ativo=True,
        ),
    }
    recursos = {
        "maca1": RecursoAgenda(
            empresa_id=empresa.id,
            nome="Maca 1",
            tipo="MACA",
            ativo=True,
        ),
        "maca2": RecursoAgenda(
            empresa_id=empresa.id,
            nome="Maca 2",
            tipo="MACA",
            ativo=True,
        ),
    }
    cliente = Cliente(empresa_id=empresa.id, nome="Cliente Agenda")
    db.add_all([*profissionais.values(), *servicos.values(), *recursos.values(), cliente])
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    def headers(chave):
        token = criar_token({"sub": usuarios[chave].email})
        return {"Authorization": f"Bearer {token}"}

    try:
        yield {
            "client": client,
            "db": db,
            "usuarios": usuarios,
            "profissionais": profissionais,
            "servicos": servicos,
            "recursos": recursos,
            "cliente": cliente,
            "headers": headers,
        }
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def horario(offset_horas=0):
    return (
        datetime(2030, 1, 10, 10, 0, tzinfo=timezone.utc)
        + timedelta(hours=offset_horas)
    ).isoformat()


def payload(ctx, **alteracoes):
    dados = {
        "servico_id": ctx["servicos"]["tattoo"].id,
        "cliente_avulso_nome": "Cliente avulso",
        "inicio_em": horario(),
    }
    dados.update(alteracoes)
    return dados


def test_profissional_cria_para_si_com_duracao_e_maca_automaticas(agenda_client):
    ctx = agenda_client
    resposta = ctx["client"].post(
        "/agendamentos/",
        json=payload(ctx),
        headers=ctx["headers"]("prof1"),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["profissional_id"] == ctx["profissionais"]["p1"].id
    assert corpo["cliente_avulso_nome"] == "Cliente avulso"
    assert corpo["duracao_minutos"] == 90
    assert corpo["preco_aplicado"] == 100.0
    assert corpo["recurso_nome"] == "Maca 1"


def test_recurso_com_nome_especifico_atende_tipo_base_do_servico(agenda_client):
    ctx = agenda_client
    ctx["recursos"]["maca1"].tipo = "MACA DE TATOO"
    ctx["recursos"]["maca2"].tipo = "MACA DE TATOO"
    ctx["db"].commit()

    resposta = ctx["client"].post(
        "/agendamentos/",
        json=payload(ctx),
        headers=ctx["headers"]("prof1"),
    )

    assert resposta.status_code == 200
    assert resposta.json()["recurso_nome"] == "Maca 1"


def test_profissional_nao_agenda_para_outro_e_gerente_pode(agenda_client):
    ctx = agenda_client
    negado = ctx["client"].post(
        "/agendamentos/",
        json=payload(
            ctx,
            profissional_id=ctx["profissionais"]["p2"].id,
        ),
        headers=ctx["headers"]("prof1"),
    )
    permitido = ctx["client"].post(
        "/agendamentos/",
        json=payload(
            ctx,
            profissional_id=ctx["profissionais"]["p2"].id,
            inicio_em=horario(2),
        ),
        headers=ctx["headers"]("gerente"),
    )

    assert negado.status_code == 403
    assert permitido.status_code == 200
    assert permitido.json()["profissional_id"] == ctx["profissionais"]["p2"].id


def test_impede_conflito_de_profissional_e_exige_maca_no_modo_manual(agenda_client):
    ctx = agenda_client
    primeira = ctx["client"].post(
        "/agendamentos/",
        json=payload(ctx),
        headers=ctx["headers"]("prof1"),
    )
    conflito_profissional = ctx["client"].post(
        "/agendamentos/",
        json=payload(ctx, inicio_em=horario(0)),
        headers=ctx["headers"]("prof1"),
    )
    sem_maca = ctx["client"].post(
        "/agendamentos/",
        json=payload(
            ctx,
            servico_id=ctx["servicos"]["tattoo_manual"].id,
            inicio_em=horario(3),
        ),
        headers=ctx["headers"]("prof2"),
    )

    assert primeira.status_code == 200
    assert conflito_profissional.status_code == 409
    assert sem_maca.status_code == 400


def test_profissional_enxerga_apenas_ocupacao_da_maca_de_outro(agenda_client):
    ctx = agenda_client
    proprio = ctx["client"].post(
        "/agendamentos/",
        json=payload(ctx),
        headers=ctx["headers"]("prof1"),
    )
    outro = ctx["client"].post(
        "/agendamentos/",
        json=payload(
            ctx,
            profissional_id=ctx["profissionais"]["p2"].id,
            inicio_em=horario(2),
        ),
        headers=ctx["headers"]("gerente"),
    )
    agenda = ctx["client"].get(
        "/agendamentos/",
        headers=ctx["headers"]("prof1"),
    )

    assert proprio.status_code == 200
    assert outro.status_code == 200
    itens = agenda.json()
    reservado = next(item for item in itens if item["id"] == outro.json()["id"])
    assert reservado["detalhes_restritos"] is True
    assert reservado["recurso_nome"] == "Maca 1"
    assert reservado["cliente_avulso_nome"] is None
    assert reservado["servico_id"] is None


def test_somente_quem_reservou_ou_gerente_pode_editar_e_cancelar(agenda_client):
    ctx = agenda_client
    criado_por_gerente = ctx["client"].post(
        "/agendamentos/",
        json=payload(
            ctx,
            profissional_id=ctx["profissionais"]["p1"].id,
        ),
        headers=ctx["headers"]("gerente"),
    ).json()
    tentativa_profissional = ctx["client"].patch(
        f"/agendamentos/{criado_por_gerente['id']}",
        json={"observacao": "nao permitido"},
        headers=ctx["headers"]("prof1"),
    )
    cancelamento = ctx["client"].patch(
        f"/agendamentos/{criado_por_gerente['id']}",
        json={"status": "CANCELADO"},
        headers=ctx["headers"]("gerente"),
    )

    assert tentativa_profissional.status_code == 403
    assert cancelamento.status_code == 200
    assert cancelamento.json()["status"] == "CANCELADO"
    assert cancelamento.json()["motivo_cancelamento"] is None


def test_configuracao_gerencial_preserva_snapshot_e_bloqueia_manutencao(agenda_client):
    ctx = agenda_client
    recurso = ctx["client"].post(
        "/recursos-agenda/",
        json={"nome": "Cadeira 1", "tipo": "CADEIRA"},
        headers=ctx["headers"]("gerente"),
    )
    servico = ctx["client"].post(
        "/servicos/",
        json={
            "nome": "Corte",
            "categoria": "Barbearia",
            "preco_padrao": 45,
            "duracao_minutos": 40,
            "requer_recurso": True,
            "tipo_recurso": "CADEIRA",
            "modo_selecao_recurso": "AUTOMATICO",
        },
        headers=ctx["headers"]("gerente"),
    )
    assert recurso.status_code == 200
    assert recurso.json()["status"] == "ATIVO"
    assert servico.status_code == 200

    agendamento = ctx["client"].post(
        "/agendamentos/",
        json={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "servico_id": servico.json()["id"],
            "cliente_avulso_nome": "Cliente do corte",
            "inicio_em": horario(4),
        },
        headers=ctx["headers"]("gerente"),
    )
    assert agendamento.status_code == 200
    criado = agendamento.json()
    assert criado["duracao_minutos"] == 40
    assert criado["preco_aplicado"] == 45.0

    atualizado_servico = ctx["client"].put(
        f"/servicos/{servico.json()['id']}",
        json={"preco_padrao": 55, "duracao_minutos": 50},
        headers=ctx["headers"]("gerente"),
    )
    assert atualizado_servico.status_code == 200

    historico = ctx["client"].get(
        f"/agendamentos/{criado['id']}",
        headers=ctx["headers"]("gerente"),
    )
    assert historico.status_code == 200
    assert historico.json()["duracao_minutos"] == 40
    assert historico.json()["preco_aplicado"] == 45.0

    manutencao = ctx["client"].put(
        f"/recursos-agenda/{recurso.json()['id']}",
        json={"status": "MANUTENCAO"},
        headers=ctx["headers"]("gerente"),
    )
    assert manutencao.status_code == 200
    assert manutencao.json()["ativo"] is False
    assert manutencao.json()["disponivel"] is False

    bloqueado = ctx["client"].post(
        "/agendamentos/",
        json={
            "profissional_id": ctx["profissionais"]["p2"].id,
            "servico_id": servico.json()["id"],
            "cliente_avulso_nome": "Outro corte",
            "inicio_em": horario(5),
        },
        headers=ctx["headers"]("gerente"),
    )
    assert bloqueado.status_code == 409

    reativado = ctx["client"].put(
        f"/recursos-agenda/{recurso.json()['id']}",
        json={"status": "ATIVO"},
        headers=ctx["headers"]("gerente"),
    )
    assert reativado.status_code == 200
    novo = ctx["client"].post(
        "/agendamentos/",
        json={
            "profissional_id": ctx["profissionais"]["p2"].id,
            "servico_id": servico.json()["id"],
            "cliente_avulso_nome": "Novo corte",
            "inicio_em": horario(5),
        },
        headers=ctx["headers"]("gerente"),
    )
    assert novo.status_code == 200
    assert novo.json()["duracao_minutos"] == 50
    assert novo.json()["preco_aplicado"] == 55.0


def test_configuracao_nao_apaga_recurso_usado_e_profissional_nao_edita(agenda_client):
    ctx = agenda_client
    criado_por_profissional = ctx["client"].post(
        "/recursos-agenda/",
        json={"nome": "Estacao 1", "tipo": "ESTACAO"},
        headers=ctx["headers"]("prof1"),
    )
    assert criado_por_profissional.status_code == 403

    recurso = ctx["client"].post(
        "/recursos-agenda/",
        json={"nome": "Estacao 1", "tipo": "ESTACAO"},
        headers=ctx["headers"]("gerente"),
    )
    assert recurso.status_code == 200
    desativado = ctx["client"].delete(
        f"/recursos-agenda/{recurso.json()['id']}",
        headers=ctx["headers"]("gerente"),
    )
    assert desativado.status_code == 200
    assert desativado.json()["status"] == "INATIVO"
    assert ctx["db"].get(RecursoAgenda, recurso.json()["id"]) is not None

    servico = ctx["client"].post(
        "/servicos/",
        json={
            "nome": "Serviço gerencial",
            "categoria": "Tattoo",
            "preco_padrao": 80,
            "duracao_minutos": 40,
        },
        headers=ctx["headers"]("prof1"),
    )
    assert servico.status_code == 403
