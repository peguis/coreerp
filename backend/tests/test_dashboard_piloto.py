from calendar import monthrange
from datetime import date, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.jwt import criar_token
from app.database import Base, get_db
from app.main import app
from app.models.atendimento import Atendimento
from app.models.empresa import Empresa
from app.models.financeiro import LancamentoFinanceiro
from app.models.movimento_estoque import MovimentoEstoque
from app.models.profissional import Profissional
from app.models.repasse import Repasse, RepasseItem
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.models.venda import Venda


PERIODO = {"data_inicio": "2026-06-01", "data_fim": "2026-06-30"}


@pytest.fixture
def dashboard_piloto_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db = factory()

    empresa_a = Empresa(
        nome="Piloto A", cnpj="10101010101010", email="piloto-a@teste.local"
    )
    empresa_b = Empresa(
        nome="Piloto B", cnpj="20202020202020", email="piloto-b@teste.local"
    )
    db.add_all([empresa_a, empresa_b])
    db.flush()

    usuarios = {}
    for chave, nome, perfil, empresa in (
        ("admin", "Admin", "admin", empresa_a),
        ("gerente", "Gerente", "gerente", empresa_a),
        ("joao", "Joao", "profissional", empresa_a),
        ("maria", "Maria", "profissional", empresa_a),
        ("ana", "Ana", "profissional", empresa_a),
        ("sem_vinculo", "Sem Vinculo", "profissional", empresa_a),
        ("operador", "Operador", "operador", empresa_a),
        ("admin_b", "Admin B", "admin", empresa_b),
        ("prof_b", "Prof B", "profissional", empresa_b),
    ):
        usuarios[chave] = Usuario(
            empresa_id=empresa.id,
            nome=nome,
            email=f"{chave}-dashboard@teste.local",
            senha="x",
            perfil=perfil,
        )
    db.add_all(usuarios.values())
    db.flush()

    profissionais = {
        "joao": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["joao"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=Decimal("70.00"),
        ),
        "maria": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["maria"].id,
            area_atuacao="TATTOO",
            percentual_padrao=Decimal("60.00"),
        ),
        "ana": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["ana"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=Decimal("50.00"),
        ),
        "b": Profissional(
            empresa_id=empresa_b.id,
            usuario_id=usuarios["prof_b"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=Decimal("99.00"),
        ),
    }
    db.add_all(profissionais.values())
    db.flush()

    servicos = {
        "corte": Servico(
            empresa_id=empresa_a.id,
            nome="Corte",
            preco_padrao=Decimal("999.00"),
        ),
        "tattoo": Servico(
            empresa_id=empresa_a.id,
            nome="Tattoo",
            preco_padrao=Decimal("1.00"),
        ),
        "b": Servico(
            empresa_id=empresa_b.id,
            nome="Outro tenant",
            preco_padrao=Decimal("9000.00"),
        ),
    }
    db.add_all(servicos.values())
    db.flush()

    atendimentos = {
        "j100": Atendimento(
            empresa_id=empresa_a.id,
            profissional_id=profissionais["joao"].id,
            servico_id=servicos["corte"].id,
            valor=Decimal("100.00"),
            percentual_profissional=Decimal("70.00"),
            valor_profissional=Decimal("70.00"),
            valor_casa=Decimal("30.00"),
            forma_pagamento="PIX",
            realizado_em=datetime(2026, 6, 1, 0, 0),
        ),
        "j50": Atendimento(
            empresa_id=empresa_a.id,
            profissional_id=profissionais["joao"].id,
            servico_id=servicos["corte"].id,
            valor=Decimal("50.00"),
            percentual_profissional=Decimal("70.00"),
            valor_profissional=Decimal("35.00"),
            valor_casa=Decimal("15.00"),
            forma_pagamento="DINHEIRO",
            realizado_em=datetime(2026, 6, 30, 23, 59, 59),
        ),
        "m200": Atendimento(
            empresa_id=empresa_a.id,
            profissional_id=profissionais["maria"].id,
            servico_id=servicos["tattoo"].id,
            valor=Decimal("200.00"),
            percentual_profissional=Decimal("60.00"),
            valor_profissional=Decimal("120.00"),
            valor_casa=Decimal("80.00"),
            forma_pagamento="CARTAO_CREDITO",
            realizado_em=datetime(2026, 6, 15, 12, 0),
        ),
        "b": Atendimento(
            empresa_id=empresa_b.id,
            profissional_id=profissionais["b"].id,
            servico_id=servicos["b"].id,
            valor=Decimal("9000.00"),
            percentual_profissional=Decimal("99.00"),
            valor_profissional=Decimal("8910.00"),
            valor_casa=Decimal("90.00"),
            forma_pagamento="PIX",
            realizado_em=datetime(2026, 6, 10, 12, 0),
        ),
    }
    db.add_all(atendimentos.values())
    db.flush()

    repasse_joao = Repasse(
        empresa_id=empresa_a.id,
        profissional_id=profissionais["joao"].id,
        created_by_usuario_id=usuarios["admin"].id,
        valor=Decimal("70.00"),
        forma_pagamento="PIX",
        pago_em=datetime(2026, 6, 20, 10, 0),
    )
    repasse_maria = Repasse(
        empresa_id=empresa_a.id,
        profissional_id=profissionais["maria"].id,
        created_by_usuario_id=usuarios["admin"].id,
        valor=Decimal("20.00"),
        forma_pagamento="DINHEIRO",
        pago_em=datetime(2026, 6, 21, 10, 0),
    )
    db.add_all([repasse_joao, repasse_maria])
    db.flush()
    db.add_all(
        [
            RepasseItem(
                empresa_id=empresa_a.id,
                repasse_id=repasse_joao.id,
                atendimento_id=atendimentos["j100"].id,
                valor=Decimal("70.00"),
            ),
            RepasseItem(
                empresa_id=empresa_a.id,
                repasse_id=repasse_maria.id,
                atendimento_id=atendimentos["m200"].id,
                valor=Decimal("20.00"),
            ),
        ]
    )

    for atendimento in (
        atendimentos["j100"], atendimentos["j50"], atendimentos["m200"]
    ):
        db.add(
            LancamentoFinanceiro(
                empresa_id=empresa_a.id,
                usuario_id=usuarios["admin"].id,
                descricao="Entrada piloto",
                valor=atendimento.valor,
                origem_tipo="ATENDIMENTO",
                origem_id=atendimento.id,
                forma_pagamento=atendimento.forma_pagamento,
                tipo="RECEITA",
                data_vencimento=atendimento.realizado_em.date(),
                data_pagamento=atendimento.realizado_em,
                status="RECEBIDO",
            )
        )
    for repasse in (repasse_joao, repasse_maria):
        db.add(
            LancamentoFinanceiro(
                empresa_id=empresa_a.id,
                usuario_id=usuarios["admin"].id,
                descricao="Saida piloto",
                valor=repasse.valor,
                origem_tipo="REPASSE",
                origem_id=repasse.id,
                forma_pagamento=repasse.forma_pagamento,
                tipo="DESPESA",
                data_vencimento=repasse.pago_em.date(),
                data_pagamento=repasse.pago_em,
                status="PAGO",
            )
        )
    db.add(
        LancamentoFinanceiro(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["admin"].id,
            descricao="Manual fora do caixa piloto",
            valor=Decimal("99999.00"),
            tipo="RECEITA",
            data_vencimento=date(2026, 6, 1),
            data_pagamento=datetime(2026, 6, 1),
            status="RECEBIDO",
        )
    )
    db.commit()

    def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db
    client = TestClient(app)

    def headers(chave):
        token = criar_token({"sub": usuarios[chave].email})
        return {"Authorization": f"Bearer {token}"}

    yield {
        "client": client,
        "db": db,
        "engine": engine,
        "headers": headers,
        "empresa": empresa_a,
        "usuarios": usuarios,
        "profissionais": profissionais,
        "servicos": servicos,
        "atendimentos": atendimentos,
    }
    app.dependency_overrides.clear()
    db.close()
    engine.dispose()


def get_admin(ctx, perfil="admin", periodo=PERIODO):
    return ctx["client"].get(
        "/dashboard/piloto", params=periodo, headers=ctx["headers"](perfil)
    )


def get_me(ctx, perfil="joao", periodo=PERIODO):
    return ctx["client"].get(
        "/dashboard/profissional/me",
        params=periodo,
        headers=ctx["headers"](perfil),
    )


def test_dashboard_admin_totais_e_agregacoes_deterministicas(
    dashboard_piloto_client,
):
    resposta = get_admin(dashboard_piloto_client)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["total_atendimentos"] == 3
    assert dados["faturamento_bruto"] == "350.00"
    assert dados["valor_profissionais"] == "225.00"
    assert dados["valor_casa"] == "125.00"
    assert dados["total_repassado"] == "90.00"
    assert dados["total_pendente_repasses"] == "135.00"
    assert dados["entradas_caixa_piloto"] == "350.00"
    assert dados["saidas_caixa_piloto"] == "90.00"
    assert dados["saldo_caixa_piloto"] == "260.00"
    assert [item["nome"] for item in dados["por_profissional"]] == [
        "Maria",
        "Joao",
        "Ana",
    ]
    assert dados["por_servico"] == [
        {
            "servico_id": dashboard_piloto_client["servicos"]["tattoo"].id,
            "nome": "Tattoo",
            "quantidade": 1,
            "faturamento_bruto": "200.00",
        },
        {
            "servico_id": dashboard_piloto_client["servicos"]["corte"].id,
            "nome": "Corte",
            "quantidade": 2,
            "faturamento_bruto": "150.00",
        },
    ]
    assert {item["forma_pagamento"] for item in dados["por_forma_pagamento"]} == {
        "PIX",
        "DINHEIRO",
        "CARTAO_CREDITO",
    }
    assert dados["faturamento_por_dia_semana"] == [
        {"dia_semana": 0, "quantidade_atendimentos": 2, "faturamento_bruto": "300.00"},
        {"dia_semana": 1, "quantidade_atendimentos": 1, "faturamento_bruto": "50.00"},
        {"dia_semana": 2, "quantidade_atendimentos": 0, "faturamento_bruto": "0.00"},
        {"dia_semana": 3, "quantidade_atendimentos": 0, "faturamento_bruto": "0.00"},
        {"dia_semana": 4, "quantidade_atendimentos": 0, "faturamento_bruto": "0.00"},
        {"dia_semana": 5, "quantidade_atendimentos": 0, "faturamento_bruto": "0.00"},
        {"dia_semana": 6, "quantidade_atendimentos": 0, "faturamento_bruto": "0.00"},
    ]
    assert [item["servico_nome"] for item in dados["ultimos_atendimentos"]] == [
        "Corte",
        "Tattoo",
        "Corte",
    ]
    assert all(item["status"] == "CONCLUIDO" for item in dados["ultimos_atendimentos"])


def test_dashboard_profissional_me_minimo_e_sem_dados_globais(
    dashboard_piloto_client,
):
    resposta = get_me(dashboard_piloto_client)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados == {
        "data_inicio": "2026-06-01",
        "data_fim": "2026-06-30",
        "profissional_id": dashboard_piloto_client["profissionais"]["joao"].id,
        "nome": "Joao",
        "area_atuacao": "BARBEARIA",
        "quantidade_atendimentos": 2,
        "faturamento_bruto": "150.00",
        "valor_profissional": "105.00",
        "valor_repassado": "70.00",
        "valor_pendente": "35.00",
    }
    for campo_proibido in (
        "valor_casa",
        "valor_profissionais",
        "entradas_caixa_piloto",
        "saidas_caixa_piloto",
        "saldo_caixa_piloto",
        "por_profissional",
    ):
        assert campo_proibido not in dados


def test_permissoes_e_profissional_sem_vinculo(dashboard_piloto_client):
    ctx = dashboard_piloto_client
    assert get_admin(ctx, "gerente").status_code == 200
    assert get_admin(ctx, "joao").status_code == 403
    assert get_admin(ctx, "operador").status_code == 403
    assert get_me(ctx, "admin").status_code == 403
    assert get_me(ctx, "gerente").status_code == 403
    sem_vinculo = get_me(ctx, "sem_vinculo")
    assert sem_vinculo.status_code == 403
    assert "sem profissional vinculado" in sem_vinculo.json()["detail"].lower()


def test_visoes_maria_e_profissional_sem_atendimentos(dashboard_piloto_client):
    ctx = dashboard_piloto_client
    maria = get_me(ctx, "maria").json()
    ana = get_me(ctx, "ana").json()
    assert maria["nome"] == "Maria"
    assert maria["quantidade_atendimentos"] == 1
    assert maria["faturamento_bruto"] == "200.00"
    assert maria["valor_profissional"] == "120.00"
    assert maria["valor_repassado"] == "20.00"
    assert maria["valor_pendente"] == "100.00"
    assert ana["nome"] == "Ana"
    assert ana["quantidade_atendimentos"] == 0
    assert ana["faturamento_bruto"] == "0.00"
    assert ana["valor_profissional"] == "0.00"
    assert ana["valor_repassado"] == "0.00"
    assert ana["valor_pendente"] == "0.00"


def test_periodo_inclusivo_no_fim_invalido_e_periodo_vazio(
    dashboard_piloto_client,
):
    ctx = dashboard_piloto_client
    dia_final = get_admin(
        ctx, periodo={"data_inicio": "2026-06-30", "data_fim": "2026-06-30"}
    ).json()
    invalido = get_admin(
        ctx, periodo={"data_inicio": "2026-07-01", "data_fim": "2026-06-30"}
    )
    vazio = get_admin(
        ctx, periodo={"data_inicio": "2026-08-01", "data_fim": "2026-08-31"}
    ).json()
    assert dia_final["total_atendimentos"] == 1
    assert dia_final["faturamento_bruto"] == "50.00"
    assert invalido.status_code == 400
    assert vazio["total_atendimentos"] == 0
    assert vazio["faturamento_bruto"] == "0.00"
    assert vazio["total_repassado"] == "0.00"
    assert vazio["total_pendente_repasses"] == "0.00"
    assert vazio["por_servico"] == []


def test_periodo_padrao_e_mes_corrente(dashboard_piloto_client):
    hoje = date.today()
    resposta = dashboard_piloto_client["client"].get(
        "/dashboard/piloto",
        headers=dashboard_piloto_client["headers"]("admin"),
    )
    assert resposta.status_code == 200
    assert resposta.json()["data_inicio"] == hoje.replace(day=1).isoformat()
    assert resposta.json()["data_fim"] == hoje.replace(
        day=monthrange(hoje.year, hoje.month)[1]
    ).isoformat()


def test_repassado_por_data_pagamento_e_pendente_pelo_atendimento(
    dashboard_piloto_client,
):
    ctx = dashboard_piloto_client
    db = ctx["db"]
    antigo = Atendimento(
        empresa_id=ctx["empresa"].id,
        profissional_id=ctx["profissionais"]["joao"].id,
        servico_id=ctx["servicos"]["corte"].id,
        valor=Decimal("10.00"),
        percentual_profissional=Decimal("100.00"),
        valor_profissional=Decimal("10.00"),
        valor_casa=Decimal("0.00"),
        forma_pagamento="PIX",
        realizado_em=datetime(2026, 5, 31, 23, 59),
    )
    atual = Atendimento(
        empresa_id=ctx["empresa"].id,
        profissional_id=ctx["profissionais"]["joao"].id,
        servico_id=ctx["servicos"]["corte"].id,
        valor=Decimal("20.00"),
        percentual_profissional=Decimal("100.00"),
        valor_profissional=Decimal("20.00"),
        valor_casa=Decimal("0.00"),
        forma_pagamento="PIX",
        realizado_em=datetime(2026, 6, 10),
    )
    db.add_all([antigo, atual])
    db.flush()
    pago_agora = Repasse(
        empresa_id=ctx["empresa"].id,
        profissional_id=ctx["profissionais"]["joao"].id,
        created_by_usuario_id=ctx["usuarios"]["admin"].id,
        valor=Decimal("10.00"),
        forma_pagamento="PIX",
        pago_em=datetime(2026, 6, 5),
    )
    pago_depois = Repasse(
        empresa_id=ctx["empresa"].id,
        profissional_id=ctx["profissionais"]["joao"].id,
        created_by_usuario_id=ctx["usuarios"]["admin"].id,
        valor=Decimal("20.00"),
        forma_pagamento="PIX",
        pago_em=datetime(2026, 7, 5),
    )
    db.add_all([pago_agora, pago_depois])
    db.flush()
    db.add_all(
        [
            RepasseItem(
                empresa_id=ctx["empresa"].id,
                repasse_id=pago_agora.id,
                atendimento_id=antigo.id,
                valor=Decimal("10.00"),
            ),
            RepasseItem(
                empresa_id=ctx["empresa"].id,
                repasse_id=pago_depois.id,
                atendimento_id=atual.id,
                valor=Decimal("20.00"),
            ),
        ]
    )
    db.commit()

    dados = get_admin(ctx).json()
    assert dados["total_repassado"] == "100.00"
    assert dados["total_pendente_repasses"] == "135.00"


def test_snapshots_tenant_caixa_piloto_e_endpoint_nao_escreve(
    dashboard_piloto_client,
):
    ctx = dashboard_piloto_client
    ctx["profissionais"]["joao"].percentual_padrao = Decimal("1.00")
    ctx["servicos"]["corte"].preco_padrao = Decimal("9999.00")
    ctx["db"].commit()
    contagens_antes = (
        ctx["db"].query(Atendimento).count(),
        ctx["db"].query(Repasse).count(),
        ctx["db"].query(LancamentoFinanceiro).count(),
        ctx["db"].query(Venda).count(),
        ctx["db"].query(MovimentoEstoque).count(),
    )
    dados = get_admin(ctx).json()
    contagens_depois = (
        ctx["db"].query(Atendimento).count(),
        ctx["db"].query(Repasse).count(),
        ctx["db"].query(LancamentoFinanceiro).count(),
        ctx["db"].query(Venda).count(),
        ctx["db"].query(MovimentoEstoque).count(),
    )
    assert dados["faturamento_bruto"] == "350.00"
    assert dados["valor_profissionais"] == "225.00"
    assert dados["entradas_caixa_piloto"] == "350.00"
    assert contagens_antes == contagens_depois

    dados_b = get_admin(ctx, "admin_b").json()
    assert dados_b["faturamento_bruto"] == "9000.00"
    assert dados_b["por_profissional"][0]["nome"] == "Prof B"


def test_centavos_sao_preservados_sem_float(dashboard_piloto_client):
    ctx = dashboard_piloto_client
    ctx["db"].add(
        Atendimento(
            empresa_id=ctx["empresa"].id,
            profissional_id=ctx["profissionais"]["ana"].id,
            servico_id=ctx["servicos"]["corte"].id,
            valor=Decimal("0.01"),
            percentual_profissional=Decimal("100.00"),
            valor_profissional=Decimal("0.01"),
            valor_casa=Decimal("0.00"),
            forma_pagamento="PIX",
            realizado_em=datetime(2026, 6, 25),
        )
    )
    ctx["db"].commit()
    dados = get_me(ctx, "ana").json()
    assert dados["faturamento_bruto"] == "0.01"
    assert dados["valor_profissional"] == "0.01"
    assert dados["valor_pendente"] == "0.01"


def test_consultas_em_quantidade_fixa_sem_n_mais_um(dashboard_piloto_client):
    ctx = dashboard_piloto_client
    quantidade = 0

    def contar(*args, **kwargs):
        nonlocal quantidade
        quantidade += 1

    event.listen(ctx["engine"], "before_cursor_execute", contar)
    try:
        resposta = get_admin(ctx)
    finally:
        event.remove(ctx["engine"], "before_cursor_execute", contar)
    assert resposta.status_code == 200
    assert quantidade <= 10
