from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest
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
from app.schemas.atendimento import AtendimentoCreate
from app.services.atendimento import criar_atendimento_service


@pytest.fixture
def atendimento_client():
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
        nome="Empresa Atendimento A",
        cnpj="55555555555555",
        email="atendimento-a@teste.local",
    )
    empresa_b = Empresa(
        nome="Empresa Atendimento B",
        cnpj="66666666666666",
        email="atendimento-b@teste.local",
    )
    db.add_all([empresa_a, empresa_b])
    db.flush()

    usuarios = {}
    for chave, nome, perfil, empresa in (
        ("admin", "Admin A", "admin", empresa_a),
        ("gerente", "Gerente A", "gerente", empresa_a),
        ("prof1", "Profissional A1", "profissional", empresa_a),
        ("prof2", "Profissional A2", "profissional", empresa_a),
        ("operador", "Operador A", "operador", empresa_a),
        ("admin_b", "Admin B", "admin", empresa_b),
        ("prof_b", "Profissional B", "profissional", empresa_b),
    ):
        usuarios[chave] = Usuario(
            nome=nome,
            email=f"{chave}-atendimento@example.com",
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
            percentual_padrao=40,
            ativo=True,
        ),
        "p2": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["prof2"].id,
            area_atuacao="TATTOO",
            percentual_padrao=50,
            ativo=True,
        ),
        "inativo": Profissional(
            empresa_id=empresa_a.id,
            usuario_id=usuarios["operador"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=30,
            ativo=False,
        ),
        "pb": Profissional(
            empresa_id=empresa_b.id,
            usuario_id=usuarios["prof_b"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=40,
            ativo=True,
        ),
    }
    servicos = {
        "ativo": Servico(
            empresa_id=empresa_a.id,
            nome="Corte",
            preco_padrao=35,
            ativo=True,
        ),
        "inativo": Servico(
            empresa_id=empresa_a.id,
            nome="Servico inativo",
            preco_padrao=20,
            ativo=False,
        ),
        "b": Servico(
            empresa_id=empresa_b.id,
            nome="Servico B",
            preco_padrao=50,
            ativo=True,
        ),
    }
    clientes = {
        "a": Cliente(nome="Cliente A", empresa_id=empresa_a.id),
        "b": Cliente(nome="Cliente B", empresa_id=empresa_b.id),
    }
    db.add_all([*profissionais.values(), *servicos.values(), *clientes.values()])
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
            "empresa_a": empresa_a,
            "empresa_b": empresa_b,
            "usuarios": usuarios,
            "profissionais": profissionais,
            "servicos": servicos,
            "clientes": clientes,
            "headers": headers,
        }
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(engine, tables=list(reversed(tabelas)))
        engine.dispose()


def payload(ctx, **alteracoes):
    dados = {
        "profissional_id": ctx["profissionais"]["p1"].id,
        "servico_id": ctx["servicos"]["ativo"].id,
        "cliente_id": ctx["clientes"]["a"].id,
        "valor": 40.55,
        "forma_pagamento": "PIX",
    }
    dados.update(alteracoes)
    return dados


def post(ctx, perfil="admin", **alteracoes):
    return ctx["client"].post(
        "/atendimentos/",
        json=payload(ctx, **alteracoes),
        headers=ctx["headers"](perfil),
    )


def test_profissional_cria_para_si_com_cliente_opcional_e_horario_automatico(
    atendimento_client,
):
    ctx = atendimento_client
    resposta = post(
        ctx,
        "prof1",
        profissional_id=None,
        cliente_id=None,
        valor=40.55,
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["profissional_id"] == ctx["profissionais"]["p1"].id
    assert corpo["empresa_id"] == ctx["empresa_a"].id
    assert corpo["cliente_id"] is None
    assert corpo["valor"] == 40.55
    assert corpo["realizado_em"]
    assert corpo["created_at"] and corpo["updated_at"]


def test_profissional_nao_cria_para_outro_e_payload_nao_define_campos_internos(
    atendimento_client,
):
    ctx = atendimento_client
    outro = post(
        ctx,
        "prof1",
        profissional_id=ctx["profissionais"]["p2"].id,
    )
    empresa_forjada = payload(ctx, empresa_id=ctx["empresa_b"].id)
    forjado = ctx["client"].post(
        "/atendimentos/",
        json=empresa_forjada,
        headers=ctx["headers"]("admin"),
    )

    assert outro.status_code == 403
    assert forjado.status_code == 422


def test_admin_e_gerente_criam_e_formas_de_pagamento_sao_aceitas(
    atendimento_client,
):
    ctx = atendimento_client
    respostas = []
    formas = ["PIX", "DINHEIRO", "CARTAO_DEBITO", "CARTAO_CREDITO"]
    for indice, forma in enumerate(formas):
        perfil = "admin" if indice % 2 == 0 else "gerente"
        respostas.append(post(ctx, perfil, forma_pagamento=forma))

    assert [resposta.status_code for resposta in respostas] == [200] * 4
    assert [resposta.json()["forma_pagamento"] for resposta in respostas] == formas


def test_rejeita_referencias_cross_tenant_e_entidades_inativas(
    atendimento_client,
):
    ctx = atendimento_client
    respostas = [
        post(
            ctx,
            profissional_id=ctx["profissionais"]["pb"].id,
            percentual_profissional_override="80.00",
        ),
        post(ctx, servico_id=ctx["servicos"]["b"].id),
        post(ctx, cliente_id=ctx["clientes"]["b"].id),
        post(ctx, profissional_id=ctx["profissionais"]["inativo"].id),
        post(ctx, servico_id=ctx["servicos"]["inativo"].id),
    ]

    assert [resposta.status_code for resposta in respostas] == [404, 404, 404, 400, 400]
    assert ctx["db"].query(Atendimento).count() == 0


def test_rejeita_valores_e_forma_invalidos(atendimento_client):
    ctx = atendimento_client
    zero = post(ctx, valor=0)
    negativo = post(ctx, valor=-1)
    forma = post(ctx, forma_pagamento="CHEQUE")

    assert zero.status_code == 422
    assert negativo.status_code == 422
    assert forma.status_code == 422
    assert ctx["db"].query(Atendimento).count() == 0


def test_profissional_lista_e_consulta_somente_os_proprios(atendimento_client):
    ctx = atendimento_client
    proprio = post(ctx, profissional_id=ctx["profissionais"]["p1"].id).json()
    alheio = post(ctx, profissional_id=ctx["profissionais"]["p2"].id).json()

    lista = ctx["client"].get(
        "/atendimentos/", headers=ctx["headers"]("prof1")
    )
    detalhe_alheio = ctx["client"].get(
        f"/atendimentos/{alheio['id']}", headers=ctx["headers"]("prof1")
    )
    bypass = ctx["client"].get(
        f"/atendimentos/?profissional_id={ctx['profissionais']['p2'].id}",
        headers=ctx["headers"]("prof1"),
    )

    assert [item["id"] for item in lista.json()] == [proprio["id"]]
    assert detalhe_alheio.status_code == 404
    assert bypass.status_code == 403


def test_resposta_profissional_nao_expoe_valor_casa(atendimento_client):
    ctx = atendimento_client
    criado_profissional = post(
        ctx,
        "prof1",
        profissional_id=None,
        valor="100.00",
    )
    criado_admin = post(ctx, valor="100.00")

    assert criado_profissional.status_code == 200
    assert "valor_casa" not in criado_profissional.json()
    assert criado_admin.status_code == 200
    assert criado_admin.json()["valor_casa"] == 60.0

    atendimento_id = criado_profissional.json()["id"]
    detalhe_profissional = ctx["client"].get(
        f"/atendimentos/{atendimento_id}",
        headers=ctx["headers"]("prof1"),
    )
    lista_profissional = ctx["client"].get(
        "/atendimentos/",
        headers=ctx["headers"]("prof1"),
    )
    detalhe_admin = ctx["client"].get(
        f"/atendimentos/{atendimento_id}",
        headers=ctx["headers"]("admin"),
    )

    assert "valor_casa" not in detalhe_profissional.json()
    assert all("valor_casa" not in item for item in lista_profissional.json())
    assert detalhe_admin.json()["valor_casa"] == 60.0


def test_admin_e_gerente_listam_empresa_e_cross_tenant_retorna_404(
    atendimento_client,
):
    ctx = atendimento_client
    post(ctx, profissional_id=ctx["profissionais"]["p1"].id)
    segundo = post(ctx, profissional_id=ctx["profissionais"]["p2"].id).json()

    for perfil in ("admin", "gerente"):
        lista = ctx["client"].get(
            "/atendimentos/", headers=ctx["headers"](perfil)
        )
        assert lista.status_code == 200
        assert len(lista.json()) == 2

    cross_tenant = ctx["client"].get(
        f"/atendimentos/{segundo['id']}",
        headers=ctx["headers"]("admin_b"),
    )
    operador = ctx["client"].get(
        "/atendimentos/", headers=ctx["headers"]("operador")
    )
    assert cross_tenant.status_code == 404
    assert operador.status_code == 403


def test_filtros_intervalo_paginacao_e_ordenacao(atendimento_client):
    ctx = atendimento_client
    antigo = datetime.now(timezone.utc) - timedelta(days=2)
    recente = datetime.now(timezone.utc) - timedelta(days=1)
    primeiro = post(
        ctx,
        profissional_id=ctx["profissionais"]["p1"].id,
        forma_pagamento="DINHEIRO",
        realizado_em=antigo.isoformat(),
    ).json()
    segundo = post(
        ctx,
        profissional_id=ctx["profissionais"]["p2"].id,
        forma_pagamento="PIX",
        realizado_em=recente.isoformat(),
    ).json()

    ordenada = ctx["client"].get(
        "/atendimentos/?limite=1", headers=ctx["headers"]("admin")
    )
    filtrada = ctx["client"].get(
        "/atendimentos/",
        params={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "servico_id": ctx["servicos"]["ativo"].id,
            "cliente_id": ctx["clientes"]["a"].id,
            "forma_pagamento": "DINHEIRO",
            "realizado_de": (antigo - timedelta(hours=1)).isoformat(),
            "realizado_ate": (antigo + timedelta(hours=1)).isoformat(),
        },
        headers=ctx["headers"]("admin"),
    )

    assert ordenada.json()[0]["id"] == segundo["id"]
    assert [item["id"] for item in filtrada.json()] == [primeiro["id"]]


def test_criacao_persiste_somente_atendimento_sem_outros_efeitos(
    atendimento_client,
):
    ctx = atendimento_client
    resposta = post(ctx)

    assert resposta.status_code == 200
    assert ctx["db"].query(Atendimento).count() == 1
    assert ctx["db"].query(MovimentoEstoque).count() == 0
    assert ctx["db"].query(Venda).count() == 0
    lancamentos = ctx["db"].query(LancamentoFinanceiro).all()
    assert len(lancamentos) == 1
    assert lancamentos[0].tipo == "RECEITA"
    assert lancamentos[0].valor == Decimal("40.55")
    assert "repasse" not in Atendimento.__table__.columns.keys()
    assert ctx["db"].query(Repasse).count() == 0
    assert ctx["db"].query(RepasseItem).count() == 0


def test_snapshot_100_reais_70_porcento(atendimento_client):
    ctx = atendimento_client
    profissional = ctx["profissionais"]["p1"]
    profissional.percentual_padrao = Decimal("70.00")
    ctx["db"].commit()

    resposta = post(ctx, valor=100)

    assert resposta.status_code == 200
    assert resposta.json()["percentual_profissional"] == 70
    assert resposta.json()["valor_profissional"] == 70
    assert resposta.json()["valor_casa"] == 30


def test_snapshot_500_reais_60_porcento(atendimento_client):
    ctx = atendimento_client
    profissional = ctx["profissionais"]["p1"]
    profissional.percentual_padrao = Decimal("60.00")
    ctx["db"].commit()

    resposta = post(ctx, valor=500)

    assert resposta.status_code == 200
    assert resposta.json()["valor_profissional"] == 300
    assert resposta.json()["valor_casa"] == 200


@pytest.mark.parametrize(
    ("percentual", "esperado_profissional", "esperado_casa"),
    [
        (Decimal("0.00"), 0, 80),
        (Decimal("100.00"), 80, 0),
    ],
)
def test_snapshot_aceita_percentuais_extremos(
    atendimento_client,
    percentual,
    esperado_profissional,
    esperado_casa,
):
    ctx = atendimento_client
    ctx["profissionais"]["p1"].percentual_padrao = percentual
    ctx["db"].commit()

    resposta = post(ctx, valor=80)

    assert resposta.status_code == 200
    assert resposta.json()["valor_profissional"] == esperado_profissional
    assert resposta.json()["valor_casa"] == esperado_casa


def test_arredondamento_decimal_preserva_soma_exata(atendimento_client):
    ctx = atendimento_client
    ctx["profissionais"]["p1"].percentual_padrao = Decimal("33.33")
    ctx["db"].commit()

    resposta = post(ctx, valor=10)
    atendimento = ctx["db"].get(Atendimento, resposta.json()["id"])

    assert resposta.status_code == 200
    assert isinstance(atendimento.valor, Decimal)
    assert isinstance(atendimento.percentual_profissional, Decimal)
    assert isinstance(atendimento.valor_profissional, Decimal)
    assert isinstance(atendimento.valor_casa, Decimal)
    assert atendimento.valor_profissional == Decimal("3.33")
    assert atendimento.valor_casa == Decimal("6.67")
    assert atendimento.valor_profissional + atendimento.valor_casa == Decimal("10.00")


def test_snapshot_nao_muda_e_novo_atendimento_usa_novo_percentual(
    atendimento_client,
):
    ctx = atendimento_client
    profissional = ctx["profissionais"]["p1"]
    servico = ctx["servicos"]["ativo"]
    profissional.percentual_padrao = Decimal("40.00")
    ctx["db"].commit()
    antigo = post(ctx, valor=100).json()

    profissional.percentual_padrao = Decimal("60.00")
    servico.preco_padrao = Decimal("999.00")
    ctx["db"].commit()
    novo = post(ctx, valor=100).json()
    profissional.ativo = False
    ctx["db"].commit()

    detalhe = ctx["client"].get(
        f"/atendimentos/{antigo['id']}", headers=ctx["headers"]("admin")
    )
    lista = ctx["client"].get(
        "/atendimentos/", headers=ctx["headers"]("admin")
    )
    itens = {item["id"]: item for item in lista.json()}

    assert detalhe.json()["percentual_profissional"] == 40
    assert detalhe.json()["valor_profissional"] == 40
    assert detalhe.json()["valor"] == 100
    assert itens[antigo["id"]]["valor_casa"] == 60
    assert itens[novo["id"]]["percentual_profissional"] == 60
    assert itens[novo["id"]]["valor_profissional"] == 60


@pytest.mark.parametrize(
    "campo",
    ["percentual_profissional", "valor_profissional", "valor_casa"],
)
def test_payload_nao_define_snapshot(atendimento_client, campo):
    ctx = atendimento_client
    resposta = post(ctx, **{campo: 1})

    assert resposta.status_code == 422
    assert ctx["db"].query(Atendimento).count() == 0


@pytest.mark.parametrize("percentual", [Decimal("-0.01"), Decimal("100.01")])
def test_percentual_inconsistente_e_rejeitado_defensivamente(
    atendimento_client,
    monkeypatch,
    percentual,
):
    ctx = atendimento_client
    profissional_real = ctx["profissionais"]["p1"]
    profissional_inconsistente = SimpleNamespace(
        id=profissional_real.id,
        ativo=True,
        percentual_padrao=percentual,
    )
    monkeypatch.setattr(
        "app.services.atendimento.buscar_profissional_por_id",
        lambda *args, **kwargs: profissional_inconsistente,
    )

    resposta = post(ctx, valor=100)

    assert resposta.status_code == 400
    assert ctx["db"].query(Atendimento).count() == 0


def test_falha_de_persistencia_faz_rollback(atendimento_client, monkeypatch):
    ctx = atendimento_client
    usuario = ctx["usuarios"]["admin"]
    dados = AtendimentoCreate(**payload(ctx))

    def falhar_apos_flush(db, **kwargs):
        atendimento = Atendimento(**kwargs)
        db.add(atendimento)
        db.flush()
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(
        "app.services.atendimento.criar_atendimento",
        falhar_apos_flush,
    )

    with pytest.raises(RuntimeError, match="falha simulada"):
        criar_atendimento_service(ctx["db"], dados, usuario)

    assert ctx["db"].query(Atendimento).count() == 0


def test_admin_e_gerente_podem_usar_override_sem_alterar_padrao(
    atendimento_client,
):
    ctx = atendimento_client
    ctx["profissionais"]["p1"].percentual_padrao = Decimal("70.00")
    ctx["db"].commit()

    admin = post(ctx, valor="100.00", percentual_profissional_override="80.00")
    gerente = post(
        ctx,
        perfil="gerente",
        valor="100.00",
        percentual_profissional_override="60.00",
    )

    assert admin.status_code == 200
    assert admin.json()["percentual_profissional"] == 80
    assert admin.json()["valor_profissional"] == 80
    assert admin.json()["valor_casa"] == 20
    assert gerente.status_code == 200
    assert gerente.json()["percentual_profissional"] == 60
    assert gerente.json()["valor_profissional"] == 60
    assert gerente.json()["valor_casa"] == 40
    ctx["db"].refresh(ctx["profissionais"]["p1"])
    assert ctx["profissionais"]["p1"].percentual_padrao == Decimal("70.00")


def test_profissional_nao_pode_enviar_override(atendimento_client):
    ctx = atendimento_client
    resposta = post(
        ctx,
        perfil="prof1",
        profissional_id=None,
        cliente_id=None,
        percentual_profissional_override="80.00",
    )
    assert resposta.status_code == 403
    assert "nao possui permissao" in resposta.json()["detail"]
    assert ctx["db"].query(Atendimento).count() == 0


@pytest.mark.parametrize(
    ("override", "valor", "esperado_profissional", "esperado_casa"),
    [
        ("0.00", "100.00", Decimal("0.00"), Decimal("100.00")),
        ("100.00", "100.00", Decimal("100.00"), Decimal("0.00")),
        ("33.33", "10.00", Decimal("3.33"), Decimal("6.67")),
        ("70.00", "0.01", Decimal("0.01"), Decimal("0.00")),
        ("80.00", "33.33", Decimal("26.66"), Decimal("6.67")),
    ],
)
def test_override_decimal_preserva_soma_e_arredondamento(
    atendimento_client,
    override,
    valor,
    esperado_profissional,
    esperado_casa,
):
    ctx = atendimento_client
    resposta = post(
        ctx,
        valor=valor,
        percentual_profissional_override=override,
    )
    atendimento = ctx["db"].get(Atendimento, resposta.json()["id"])

    assert resposta.status_code == 200
    assert atendimento.percentual_profissional == Decimal(override)
    assert atendimento.valor_profissional == esperado_profissional
    assert atendimento.valor_casa == esperado_casa
    assert atendimento.valor_profissional + atendimento.valor_casa == atendimento.valor


@pytest.mark.parametrize(
    "override",
    ["-0.01", "100.01", "nao-e-percentual"],
)
def test_override_fora_da_faixa_e_rejeitado(override, atendimento_client):
    ctx = atendimento_client
    resposta = post(ctx, percentual_profissional_override=override)
    assert resposta.status_code == 422
    assert ctx["db"].query(Atendimento).count() == 0


def test_sem_override_seguinte_usa_padrao_e_historico_override_e_imutavel(
    atendimento_client,
):
    ctx = atendimento_client
    profissional = ctx["profissionais"]["p1"]
    servico = ctx["servicos"]["ativo"]
    profissional.percentual_padrao = Decimal("70.00")
    ctx["db"].commit()
    excepcional = post(
        ctx,
        valor="100.00",
        percentual_profissional_override="80.00",
    ).json()
    normal = post(ctx, valor="100.00").json()

    profissional.percentual_padrao = Decimal("60.00")
    servico.preco_padrao = Decimal("999.99")
    ctx["db"].commit()
    detalhe = ctx["client"].get(
        f"/atendimentos/{excepcional['id']}", headers=ctx["headers"]("admin")
    ).json()
    normal_atual = ctx["db"].get(Atendimento, normal["id"])

    assert detalhe["percentual_profissional"] == 80
    assert detalhe["valor_profissional"] == 80
    assert detalhe["valor_casa"] == 20
    assert normal_atual.percentual_profissional == Decimal("70.00")
    assert normal_atual.valor_profissional == Decimal("70.00")
    assert profissional.percentual_padrao == Decimal("60.00")


def test_p5_usa_snapshot_override_em_repasses_parciais(atendimento_client):
    ctx = atendimento_client
    atendimento = post(
        ctx,
        valor="100.00",
        percentual_profissional_override="80.00",
    ).json()
    pendencias = ctx["client"].get(
        "/repasses/pendencias",
        params={"profissional_id": ctx["profissionais"]["p1"].id},
        headers=ctx["headers"]("admin"),
    ).json()
    pendencia = next(item for item in pendencias if item["profissional_id"] == ctx["profissionais"]["p1"].id)
    item = next(item for item in pendencia["atendimentos"] if item["atendimento_id"] == atendimento["id"])
    assert item["valor_pendente"] == "80.00"

    parcial = ctx["client"].post(
        "/repasses/",
        json={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "forma_pagamento": "PIX",
            "itens": [{"atendimento_id": atendimento["id"], "valor": "50.00"}],
        },
        headers=ctx["headers"]("admin"),
    )
    final = ctx["client"].post(
        "/repasses/",
        json={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "forma_pagamento": "PIX",
            "itens": [{"atendimento_id": atendimento["id"], "valor": "30.00"}],
        },
        headers=ctx["headers"]("admin"),
    )
    pendencias_finais = ctx["client"].get(
        "/repasses/pendencias",
        params={"profissional_id": ctx["profissionais"]["p1"].id},
        headers=ctx["headers"]("admin"),
    ).json()
    item_final = next(
        item
        for item in next(
            item for item in pendencias_finais
            if item["profissional_id"] == ctx["profissionais"]["p1"].id
        )["atendimentos"]
        if item["atendimento_id"] == atendimento["id"]
    )
    assert parcial.status_code == 200
    assert final.status_code == 200
    assert item_final["valor_pendente"] == "0.00"


def test_p6_receita_bruta_unica_e_saida_do_override(atendimento_client):
    ctx = atendimento_client
    atendimento = post(
        ctx,
        valor="100.00",
        percentual_profissional_override="80.00",
    ).json()
    receitas = [
        item for item in ctx["db"].query(LancamentoFinanceiro).all()
        if item.origem_tipo == "ATENDIMENTO"
    ]
    assert len(receitas) == 1
    assert receitas[0].valor == Decimal("100.00")
    assert receitas[0].tipo == "RECEITA"

    repasse = ctx["client"].post(
        "/repasses/",
        json={
            "profissional_id": ctx["profissionais"]["p1"].id,
            "forma_pagamento": "PIX",
            "itens": [{"atendimento_id": atendimento["id"], "valor": "80.00"}],
        },
        headers=ctx["headers"]("admin"),
    )
    saidas = [
        item for item in ctx["db"].query(LancamentoFinanceiro).all()
        if item.origem_tipo == "REPASSE"
    ]
    assert repasse.status_code == 200
    assert len(saidas) == 1
    assert saidas[0].valor == Decimal("80.00")
    assert saidas[0].tipo == "DESPESA"


def test_p7_reflete_snapshots_mistos_admin_e_profissional(atendimento_client):
    ctx = atendimento_client
    ctx["profissionais"]["p1"].percentual_padrao = Decimal("70.00")
    ctx["db"].commit()
    post(ctx, valor="100.00", percentual_profissional_override="80.00")
    post(ctx, valor="100.00")

    dashboard = ctx["client"].get(
        "/dashboard/piloto", headers=ctx["headers"]("admin")
    )
    profissional = ctx["client"].get(
        "/dashboard/profissional/me", headers=ctx["headers"]("prof1")
    )
    assert dashboard.status_code == 200
    assert dashboard.json()["faturamento_bruto"] == "200.00"
    assert dashboard.json()["valor_profissionais"] == "150.00"
    assert dashboard.json()["valor_casa"] == "50.00"
    assert profissional.status_code == 200
    assert profissional.json()["valor_profissional"] == "150.00"
