import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
from threading import Barrier
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.jwt import criar_token
from app.database import Base, get_db
from app.main import app
from app.models.atendimento import Atendimento
from app.models.cliente import Cliente
from app.models.categoria_financeira import CategoriaFinanceira
from app.models.empresa import Empresa
from app.models.financeiro import LancamentoFinanceiro
from app.models.movimento_estoque import MovimentoEstoque
from app.models.profissional import Profissional
from app.models.repasse import Repasse, RepasseItem
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.models.venda import Venda
from app.schemas.repasse import RepasseCreate
from app.schemas.atendimento import AtendimentoCreate
from app.services.atendimento import criar_atendimento_service
from app.services.integracao_financeira import (
    registrar_entrada_atendimento,
    registrar_saida_repasse,
)
from app.services.repasse import criar_repasse_service


@pytest.fixture
def repasse_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    tabelas = [
        Empresa.__table__,
        Usuario.__table__,
        Cliente.__table__,
        Servico.__table__,
        Profissional.__table__,
        Atendimento.__table__,
        Repasse.__table__,
        RepasseItem.__table__,
        CategoriaFinanceira.__table__,
        MovimentoEstoque.__table__,
        Venda.__table__,
        LancamentoFinanceiro.__table__,
    ]
    Base.metadata.create_all(engine, tables=tabelas)
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    empresa_a = Empresa(
        nome="Empresa Repasse A",
        cnpj="77777777777777",
        email="repasse-a@teste.local",
    )
    empresa_b = Empresa(
        nome="Empresa Repasse B",
        cnpj="88888888888888",
        email="repasse-b@teste.local",
    )
    db.add_all([empresa_a, empresa_b])
    db.flush()

    usuarios = {}
    for chave, perfil, empresa in (
        ("admin", "admin", empresa_a),
        ("gerente", "gerente", empresa_a),
        ("prof1", "profissional", empresa_a),
        ("prof2", "profissional", empresa_a),
        ("admin_b", "admin", empresa_b),
        ("prof_b", "profissional", empresa_b),
    ):
        usuarios[chave] = Usuario(
            nome=chave,
            email=f"{chave}-repasse@example.com",
            senha="nao usada",
            perfil=perfil,
            empresa_id=empresa.id,
        )
    db.add_all(usuarios.values())
    db.flush()

    profissionais = {
        "p1": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["prof1"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=70,
            ativo=True,
        ),
        "p2": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["prof2"].id,
            area_atuacao="TATTOO",
            percentual_padrao=60,
            ativo=True,
        ),
        "pb": Profissional(
            empresa_id=empresa_b.id,
            usuario_id=usuarios["prof_b"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=50,
            ativo=True,
        ),
    }
    servicos = {
        "a": Servico(
            empresa_id=empresa_a.id,
            nome="Corte Repasse",
            preco_padrao=100,
            ativo=True,
        ),
        "b": Servico(
            empresa_id=empresa_b.id,
            nome="Corte Repasse B",
            preco_padrao=100,
            ativo=True,
        ),
    }
    db.add_all([*profissionais.values(), *servicos.values()])
    db.commit()

    def atendimento(profissional, servico, valor="100.00", devido="70.00"):
        registro = Atendimento(
            empresa_id=profissional.empresa_id,
            profissional_id=profissional.id,
            servico_id=servico.id,
            cliente_id=None,
            valor=Decimal(valor),
            percentual_profissional=Decimal("70.00"),
            valor_profissional=Decimal(devido),
            valor_casa=Decimal(valor) - Decimal(devido),
            forma_pagamento="PIX",
            realizado_em=datetime.now(timezone.utc),
        )
        db.add(registro)
        db.commit()
        return registro

    atendimentos = {
        "a1": atendimento(profissionais["p1"], servicos["a"]),
        "a2": atendimento(
            profissionais["p1"], servicos["a"], "50.00", "35.00"
        ),
        "outro_prof": atendimento(
            profissionais["p2"], servicos["a"], "100.00", "60.00"
        ),
        "outra_empresa": atendimento(
            profissionais["pb"], servicos["b"], "100.00", "50.00"
        ),
    }

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
            "empresa_a": empresa_a,
            "empresa_b": empresa_b,
            "usuarios": usuarios,
            "profissionais": profissionais,
            "servicos": servicos,
            "atendimentos": atendimentos,
            "headers": headers,
        }
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(engine, tables=list(reversed(tabelas)))
        engine.dispose()


def post_repasse(ctx, itens, perfil="admin", profissional="p1", **extras):
    dados = {
        "profissional_id": ctx["profissionais"][profissional].id,
        "forma_pagamento": "PIX",
        "itens": itens,
    }
    dados.update(extras)
    return ctx["client"].post(
        "/repasses/", json=dados, headers=ctx["headers"](perfil)
    )


def item(ctx, atendimento="a1", valor=70):
    return {
        "atendimento_id": ctx["atendimentos"][atendimento].id,
        "valor": valor,
    }


def post_atendimento(ctx, valor=100, perfil="admin"):
    return ctx["client"].post(
        "/atendimentos/",
        json={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "servico_id": ctx["servicos"]["a"].id,
            "cliente_id": None,
            "valor": valor,
            "forma_pagamento": "PIX",
        },
        headers=ctx["headers"](perfil),
    )


def pendencia(ctx, perfil="admin", profissional="p1"):
    resposta = ctx["client"].get(
        "/repasses/pendencias",
        params={"profissional_id": ctx["profissionais"][profissional].id},
        headers=ctx["headers"](perfil),
    )
    assert resposta.status_code == 200
    return resposta.json()[0]


def test_pendencia_sem_repasse_usa_snapshot_p4(repasse_client):
    ctx = repasse_client
    resumo = pendencia(ctx)
    detalhe = next(
        item
        for item in resumo["atendimentos"]
        if item["atendimento_id"] == ctx["atendimentos"]["a1"].id
    )

    assert Decimal(resumo["total_devido"]) == Decimal("105.00")
    assert Decimal(resumo["total_repassado"]) == Decimal("0.00")
    assert Decimal(resumo["total_pendente"]) == Decimal("105.00")
    assert Decimal(detalhe["valor_profissional"]) == Decimal("70.00")
    assert Decimal(detalhe["valor_pendente"]) == Decimal("70.00")


def test_repasse_total_zerando_pendencia(repasse_client):
    ctx = repasse_client
    resposta = post_repasse(ctx, [item(ctx)])
    resumo = pendencia(ctx)

    assert resposta.status_code == 200
    assert Decimal(resposta.json()["valor"]) == Decimal("70.00")
    assert Decimal(resumo["total_repassado"]) == Decimal("70.00")
    assert Decimal(resumo["total_pendente"]) == Decimal("35.00")


def test_dois_repasses_parciais_e_bloqueio_de_excesso(repasse_client):
    ctx = repasse_client
    primeiro = post_repasse(ctx, [item(ctx, valor=40)])
    parcial = pendencia(ctx)
    segundo = post_repasse(ctx, [item(ctx, valor=30)], perfil="gerente")
    final = pendencia(ctx)
    excesso = post_repasse(ctx, [item(ctx, valor=0.01)])

    assert primeiro.status_code == 200
    assert Decimal(parcial["total_repassado"]) == Decimal("40.00")
    assert Decimal(parcial["total_pendente"]) == Decimal("65.00")
    assert segundo.status_code == 200
    assert Decimal(final["total_repassado"]) == Decimal("70.00")
    assert Decimal(final["total_pendente"]) == Decimal("35.00")
    assert excesso.status_code == 409
    assert ctx["db"].query(Repasse).count() == 2


def test_um_repasse_quita_multiplos_atendimentos_e_totaliza_itens(
    repasse_client,
):
    ctx = repasse_client
    resposta = post_repasse(
        ctx,
        [item(ctx, "a1", 70), item(ctx, "a2", 35)],
        forma_pagamento="TRANSFERENCIA",
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert Decimal(corpo["valor"]) == Decimal("105.00")
    assert sum(Decimal(str(i["valor"])) for i in corpo["itens"]) == Decimal(
        "105.00"
    )
    assert len(corpo["itens"]) == 2


def test_rejeita_atendimento_alheio_cross_tenant_e_profissional_cross_tenant(
    repasse_client,
):
    ctx = repasse_client
    outro_prof = post_repasse(ctx, [item(ctx, "outro_prof", 10)])
    outra_empresa = post_repasse(ctx, [item(ctx, "outra_empresa", 10)])
    profissional_b = post_repasse(
        ctx, [item(ctx, "a1", 10)], profissional="pb"
    )

    assert outro_prof.status_code == 400
    assert outra_empresa.status_code == 404
    assert profissional_b.status_code == 404
    assert ctx["db"].query(Repasse).count() == 0


def test_permissoes_de_criacao_admin_gerente_profissional(repasse_client):
    ctx = repasse_client
    admin = post_repasse(ctx, [item(ctx, valor=10)], perfil="admin")
    gerente = post_repasse(ctx, [item(ctx, valor=10)], perfil="gerente")
    profissional = post_repasse(ctx, [item(ctx, valor=10)], perfil="prof1")

    assert admin.status_code == 200
    assert gerente.status_code == 200
    assert profissional.status_code == 403


def test_visibilidade_profissional_e_isolamento_cross_tenant(repasse_client):
    ctx = repasse_client
    proprio = post_repasse(ctx, [item(ctx, valor=10)]).json()
    alheio = post_repasse(
        ctx,
        [item(ctx, "outro_prof", 10)],
        profissional="p2",
    ).json()

    lista = ctx["client"].get(
        "/repasses/", headers=ctx["headers"]("prof1")
    )
    detalhe_alheio = ctx["client"].get(
        f"/repasses/{alheio['id']}", headers=ctx["headers"]("prof1")
    )
    bypass = ctx["client"].get(
        "/repasses/",
        params={"profissional_id": ctx["profissionais"]["p2"].id},
        headers=ctx["headers"]("prof1"),
    )
    cross = ctx["client"].get(
        f"/repasses/{proprio['id']}", headers=ctx["headers"]("admin_b")
    )

    assert [registro["id"] for registro in lista.json()] == [proprio["id"]]
    assert detalhe_alheio.status_code == 404
    assert bypass.status_code == 403
    assert cross.status_code == 404


def test_admin_e_gerente_listam_apenas_empresa_e_filtros(repasse_client):
    ctx = repasse_client
    criado = post_repasse(ctx, [item(ctx, valor=10)]).json()
    for perfil in ("admin", "gerente"):
        resposta = ctx["client"].get(
            "/repasses/",
            params={
                "profissional_id": ctx["profissionais"]["p1"].id,
                "pago_de": "2000-01-01T00:00:00Z",
                "limite": 1,
            },
            headers=ctx["headers"](perfil),
        )
        assert resposta.status_code == 200
        assert [registro["id"] for registro in resposta.json()] == [criado["id"]]


def test_pendencia_permanece_historica_apos_mudancas(repasse_client):
    ctx = repasse_client
    antes = pendencia(ctx)
    profissional = ctx["profissionais"]["p1"]
    profissional.percentual_padrao = Decimal("5.00")
    profissional.ativo = False
    ctx["servicos"]["a"].preco_padrao = Decimal("999.00")
    ctx["db"].commit()
    depois = pendencia(ctx)

    assert antes == depois
    resposta = post_repasse(ctx, [item(ctx, valor=10)])
    assert resposta.status_code == 200


def test_valores_invalidos_payload_inconsistente_e_item_duplicado(repasse_client):
    ctx = repasse_client
    zero = post_repasse(ctx, [item(ctx, valor=0)])
    negativo = post_repasse(ctx, [item(ctx, valor=-1)])
    total_forjado = post_repasse(ctx, [item(ctx, valor=10)], valor=999)
    duplicado = post_repasse(ctx, [item(ctx, valor=10), item(ctx, valor=10)])

    assert zero.status_code == 422
    assert negativo.status_code == 422
    assert total_forjado.status_code == 422
    assert duplicado.status_code == 400
    assert ctx["db"].query(Repasse).count() == 0


def test_falha_em_item_faz_rollback_integral(repasse_client, monkeypatch):
    ctx = repasse_client
    dados = RepasseCreate(
        profissional_id=ctx["profissionais"]["p1"].id,
        forma_pagamento="PIX",
        itens=[item(ctx, "a1", 10), item(ctx, "a2", 10)],
    )
    from app.repositories.repasse import criar_repasse_item as criar_real

    chamadas = 0

    def falhar_no_segundo(db, **kwargs):
        nonlocal chamadas
        chamadas += 1
        if chamadas == 2:
            raise RuntimeError("falha simulada")
        return criar_real(db, **kwargs)

    monkeypatch.setattr(
        "app.services.repasse.criar_repasse_item", falhar_no_segundo
    )
    with pytest.raises(RuntimeError, match="falha simulada"):
        criar_repasse_service(ctx["db"], dados, ctx["usuarios"]["admin"])

    assert ctx["db"].query(Repasse).count() == 0
    assert ctx["db"].query(RepasseItem).count() == 0


def test_criacao_gera_so_financeiro_sem_venda_ou_estoque(repasse_client):
    ctx = repasse_client
    resposta = post_repasse(ctx, [item(ctx, valor=10)])

    assert resposta.status_code == 200
    lancamentos = ctx["db"].query(LancamentoFinanceiro).all()
    assert len(lancamentos) == 1
    assert lancamentos[0].tipo == "DESPESA"
    assert lancamentos[0].valor == Decimal("10.00")
    assert ctx["db"].query(Venda).count() == 0
    assert ctx["db"].query(MovimentoEstoque).count() == 0


def test_atendimento_cria_entrada_bruta_unica_sem_saida(repasse_client):
    ctx = repasse_client
    resposta = post_atendimento(ctx, 100)
    lancamentos = ctx["db"].query(LancamentoFinanceiro).all()

    assert resposta.status_code == 200
    assert len(lancamentos) == 1
    entrada = lancamentos[0]
    assert entrada.tipo == "RECEITA"
    assert entrada.status == "RECEBIDO"
    assert entrada.valor == Decimal("100.00")
    assert entrada.origem_tipo == "ATENDIMENTO"
    assert entrada.origem_id == resposta.json()["id"]
    assert entrada.forma_pagamento == "PIX"
    assert ctx["db"].query(Repasse).count() == 0


def test_fluxo_atendimento_100_repasse_70_resulta_liquido_30(repasse_client):
    ctx = repasse_client
    atendimento = post_atendimento(ctx, 100).json()
    atendimento_db = ctx["db"].get(Atendimento, atendimento["id"])
    snapshot_antes = (
        atendimento_db.valor,
        atendimento_db.percentual_profissional,
        atendimento_db.valor_profissional,
        atendimento_db.valor_casa,
    )
    repasse = post_repasse(
        ctx,
        [{"atendimento_id": atendimento["id"], "valor": 70}],
    )
    lancamentos = ctx["db"].query(LancamentoFinanceiro).all()

    assert repasse.status_code == 200
    receitas = sum(
        lancamento.valor for lancamento in lancamentos
        if lancamento.tipo == "RECEITA"
    )
    despesas = sum(
        lancamento.valor for lancamento in lancamentos
        if lancamento.tipo == "DESPESA"
    )
    saida = next(item for item in lancamentos if item.tipo == "DESPESA")
    assert receitas == Decimal("100.00")
    assert despesas == Decimal("70.00")
    assert receitas - despesas == Decimal("30.00")
    assert saida.status == "PAGO"
    assert saida.origem_tipo == "REPASSE"
    assert saida.origem_id == repasse.json()["id"]
    ctx["db"].refresh(atendimento_db)
    assert snapshot_antes == (
        atendimento_db.valor,
        atendimento_db.percentual_profissional,
        atendimento_db.valor_profissional,
        atendimento_db.valor_casa,
    )


def test_repasses_parciais_criam_saidas_pelos_valores_pagos(repasse_client):
    ctx = repasse_client
    atendimento = post_atendimento(ctx, 100).json()
    primeiro = post_repasse(
        ctx, [{"atendimento_id": atendimento["id"], "valor": 40}]
    )
    segundo = post_repasse(
        ctx, [{"atendimento_id": atendimento["id"], "valor": 30}]
    )
    despesas = (
        ctx["db"].query(LancamentoFinanceiro)
        .filter(LancamentoFinanceiro.tipo == "DESPESA")
        .order_by(LancamentoFinanceiro.id.asc())
        .all()
    )

    assert primeiro.status_code == 200
    assert segundo.status_code == 200
    assert [registro.valor for registro in despesas] == [
        Decimal("40.00"),
        Decimal("30.00"),
    ]


def test_lancamento_historico_nao_muda_com_percentual_ou_preco(repasse_client):
    ctx = repasse_client
    atendimento = post_atendimento(ctx, "33.33").json()
    entrada = (
        ctx["db"].query(LancamentoFinanceiro)
        .filter(LancamentoFinanceiro.origem_tipo == "ATENDIMENTO")
        .one()
    )
    ctx["profissionais"]["p1"].percentual_padrao = Decimal("1.00")
    ctx["servicos"]["a"].preco_padrao = Decimal("999.00")
    ctx["db"].commit()
    ctx["db"].refresh(entrada)

    assert entrada.valor == Decimal("33.33")
    assert entrada.origem_id == atendimento["id"]


def test_falha_financeira_reverte_atendimento(repasse_client, monkeypatch):
    ctx = repasse_client
    antes = ctx["db"].query(Atendimento).count()
    dados = AtendimentoCreate(
        profissional_id=ctx["profissionais"]["p1"].id,
        servico_id=ctx["servicos"]["a"].id,
        valor=100,
        forma_pagamento="PIX",
    )

    def falhar(*args, **kwargs):
        raise RuntimeError("financeiro indisponivel")

    monkeypatch.setattr(
        "app.services.atendimento.registrar_entrada_atendimento", falhar
    )
    with pytest.raises(RuntimeError, match="financeiro indisponivel"):
        criar_atendimento_service(ctx["db"], dados, ctx["usuarios"]["admin"])

    assert ctx["db"].query(Atendimento).count() == antes
    assert ctx["db"].query(LancamentoFinanceiro).count() == 0


def test_falha_financeira_reverte_repasse_e_itens(repasse_client, monkeypatch):
    ctx = repasse_client
    dados = RepasseCreate(
        profissional_id=ctx["profissionais"]["p1"].id,
        forma_pagamento="PIX",
        itens=[item(ctx, valor=10)],
    )

    def falhar(*args, **kwargs):
        raise RuntimeError("financeiro indisponivel")

    monkeypatch.setattr("app.services.repasse.registrar_saida_repasse", falhar)
    with pytest.raises(RuntimeError, match="financeiro indisponivel"):
        criar_repasse_service(ctx["db"], dados, ctx["usuarios"]["admin"])

    assert ctx["db"].query(Repasse).count() == 0
    assert ctx["db"].query(RepasseItem).count() == 0
    assert ctx["db"].query(LancamentoFinanceiro).count() == 0


def test_integracao_automatica_e_idempotente(repasse_client):
    ctx = repasse_client
    atendimento = post_atendimento(ctx, 100).json()
    atendimento_db = ctx["db"].get(Atendimento, atendimento["id"])
    registrar_entrada_atendimento(
        ctx["db"], atendimento_db, ctx["usuarios"]["admin"]
    )
    ctx["db"].commit()
    assert (
        ctx["db"].query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.origem_tipo == "ATENDIMENTO",
            LancamentoFinanceiro.origem_id == atendimento["id"],
        )
        .count()
        == 1
    )

    repasse = post_repasse(
        ctx, [{"atendimento_id": atendimento["id"], "valor": 10}]
    ).json()
    repasse_db = ctx["db"].get(Repasse, repasse["id"])
    registrar_saida_repasse(ctx["db"], repasse_db, ctx["usuarios"]["admin"])
    ctx["db"].commit()
    assert (
        ctx["db"].query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.origem_tipo == "REPASSE",
            LancamentoFinanceiro.origem_id == repasse["id"],
        )
        .count()
        == 1
    )


def test_financeiro_manual_legado_e_permissoes_preservados(repasse_client):
    ctx = repasse_client
    manual = ctx["client"].post(
        "/financeiro/lancamentos",
        json={
            "descricao": "Lancamento manual",
            "valor": "10.10",
            "tipo": "RECEITA",
            "data_vencimento": "2026-09-16",
        },
        headers=ctx["headers"]("admin"),
    )
    manual_gerente = ctx["client"].post(
        "/financeiro/lancamentos",
        json={
            "descricao": "Lancamento gerente",
            "valor": "0.01",
            "tipo": "DESPESA",
            "data_vencimento": "2026-09-16",
        },
        headers=ctx["headers"]("gerente"),
    )
    lista_admin = ctx["client"].get(
        "/financeiro/lancamentos", headers=ctx["headers"]("admin")
    )
    lista_b = ctx["client"].get(
        "/financeiro/lancamentos", headers=ctx["headers"]("admin_b")
    )
    lista_profissional = ctx["client"].get(
        "/financeiro/lancamentos", headers=ctx["headers"]("prof1")
    )

    assert manual.status_code == 201
    assert manual_gerente.status_code == 201
    assert manual.json()["valor"] == "10.10"
    assert manual.json()["origem_tipo"] is None
    assert len(lista_admin.json()) == 2
    assert lista_b.json() == []
    assert lista_profissional.status_code == 403


def test_lancamento_automatico_nao_pode_ser_editado_ou_removido(repasse_client):
    ctx = repasse_client
    post_atendimento(ctx, 100)
    lancamento = ctx["db"].query(LancamentoFinanceiro).one()

    edicao = ctx["client"].put(
        f"/financeiro/lancamentos/{lancamento.id}",
        json={"valor": "1.00"},
        headers=ctx["headers"]("admin"),
    )
    exclusao = ctx["client"].delete(
        f"/financeiro/lancamentos/{lancamento.id}",
        headers=ctx["headers"]("admin"),
    )

    assert edicao.status_code == 409
    assert exclusao.status_code == 409


@pytest.mark.parametrize("valor", ["0.01", "10.10", "33.33"])
def test_centavos_sao_preservados_no_financeiro(repasse_client, valor):
    ctx = repasse_client
    resposta = post_atendimento(ctx, valor)
    lancamento = ctx["db"].query(LancamentoFinanceiro).one()

    assert resposta.status_code == 200
    assert isinstance(lancamento.valor, Decimal)
    assert lancamento.valor == Decimal(valor)


def test_integracao_rejeita_origem_de_outra_empresa(repasse_client):
    ctx = repasse_client
    atendimento = ctx["atendimentos"]["a1"]

    with pytest.raises(HTTPException) as erro:
        registrar_entrada_atendimento(
            ctx["db"], atendimento, ctx["usuarios"]["admin_b"]
        )
    assert erro.value.status_code == 400
    ctx["db"].rollback()
    assert ctx["db"].query(LancamentoFinanceiro).count() == 0


def test_categorias_automaticas_sao_idempotentes_e_tenant_safe(repasse_client):
    ctx = repasse_client
    primeiro = post_atendimento(ctx, 100).json()
    segundo = post_atendimento(ctx, 100).json()
    post_repasse(
        ctx, [{"atendimento_id": primeiro["id"], "valor": 10}]
    )
    post_repasse(
        ctx, [{"atendimento_id": segundo["id"], "valor": 10}]
    )

    categorias = ctx["db"].query(CategoriaFinanceira).all()
    assert sorted(item.chave_sistema for item in categorias) == [
        "RECEITA_SERVICOS",
        "REPASSE_PROFISSIONAIS",
    ]
    assert {item.empresa_id for item in categorias} == {ctx["empresa_a"].id}


@pytest.mark.skipif(
    not os.getenv("TEST_POSTGRES_URL"),
    reason="TEST_POSTGRES_URL nao configurada",
)
def test_concorrencia_postgresql_nao_ultrapassa_saldo():
    engine = create_engine(os.environ["TEST_POSTGRES_URL"])
    tabelas = [
        Empresa.__table__,
        Usuario.__table__,
        Cliente.__table__,
        Servico.__table__,
        Profissional.__table__,
        Atendimento.__table__,
        Repasse.__table__,
        RepasseItem.__table__,
        CategoriaFinanceira.__table__,
        LancamentoFinanceiro.__table__,
    ]
    Base.metadata.drop_all(engine, tables=list(reversed(tabelas)))
    Base.metadata.create_all(engine, tables=tabelas)
    factory = sessionmaker(bind=engine)
    db = factory()
    empresa = Empresa(
        nome="Concorrencia",
        cnpj="99999999999999",
        email="concorrencia@teste.local",
    )
    db.add(empresa)
    db.flush()
    admin = Usuario(
        empresa_id=empresa.id,
        nome="Admin",
        email="admin-concorrencia@teste.local",
        senha="x",
        perfil="admin",
    )
    usuario_prof = Usuario(
        empresa_id=empresa.id,
        nome="Prof",
        email="prof-concorrencia@teste.local",
        senha="x",
        perfil="profissional",
    )
    db.add_all([admin, usuario_prof])
    db.flush()
    profissional = Profissional(
        empresa_id=empresa.id,
        usuario_id=usuario_prof.id,
        area_atuacao="BARBEARIA",
        percentual_padrao=70,
        ativo=True,
    )
    servico = Servico(
        empresa_id=empresa.id,
        nome="Servico concorrente",
        preco_padrao=100,
        ativo=True,
    )
    db.add_all([profissional, servico])
    db.flush()
    atendimento = Atendimento(
        empresa_id=empresa.id,
        profissional_id=profissional.id,
        servico_id=servico.id,
        valor=Decimal("100.00"),
        percentual_profissional=Decimal("70.00"),
        valor_profissional=Decimal("70.00"),
        valor_casa=Decimal("30.00"),
        forma_pagamento="PIX",
        realizado_em=datetime.now(timezone.utc),
    )
    db.add(atendimento)
    db.commit()
    ids = (empresa.id, admin.id, profissional.id, atendimento.id)
    db.close()
    barreira = Barrier(2)

    def tentar():
        sessao = factory()
        empresa_id, admin_id, profissional_id, atendimento_id = ids
        usuario = SimpleNamespace(
            id=admin_id, empresa_id=empresa_id, perfil="admin"
        )
        dados = RepasseCreate(
            profissional_id=profissional_id,
            forma_pagamento="PIX",
            itens=[{"atendimento_id": atendimento_id, "valor": 50}],
        )
        barreira.wait()
        try:
            criar_repasse_service(sessao, dados, usuario)
            return 200
        except HTTPException as exc:
            return exc.status_code
        finally:
            sessao.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(lambda _: tentar(), range(2)))

    verificacao = factory()
    total = verificacao.query(RepasseItem.valor).all()
    repasse_id = verificacao.query(Repasse.id).scalar()
    verificacao.query(LancamentoFinanceiro).filter(
        LancamentoFinanceiro.origem_tipo == "REPASSE",
        LancamentoFinanceiro.origem_id == repasse_id,
    ).delete(synchronize_session=False)
    verificacao.commit()
    verificacao.close()

    barreira_origem = Barrier(2)

    def tentar_mesma_origem():
        sessao = factory()
        empresa_id, admin_id, _, _ = ids
        usuario = SimpleNamespace(
            id=admin_id, empresa_id=empresa_id, perfil="admin"
        )
        repasse = sessao.get(Repasse, repasse_id)
        barreira_origem.wait()
        try:
            registrar_saida_repasse(sessao, repasse, usuario)
            sessao.commit()
            return "ok"
        except Exception:
            sessao.rollback()
            return "conflito"
        finally:
            sessao.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados_origem = list(
            executor.map(lambda _: tentar_mesma_origem(), range(2))
        )

    verificacao = factory()
    total_origens = (
        verificacao.query(LancamentoFinanceiro)
        .filter(
            LancamentoFinanceiro.origem_tipo == "REPASSE",
            LancamentoFinanceiro.origem_id == repasse_id,
        )
        .count()
    )
    verificacao.close()
    Base.metadata.drop_all(engine, tables=list(reversed(tabelas)))
    engine.dispose()

    assert sorted(resultados) == [200, 409]
    assert sum(valor for (valor,) in total) == Decimal("50.00")
    assert "ok" in resultados_origem
    assert total_origens == 1
