from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.hash import gerar_hash, verificar_senha
from app.auth.jwt import criar_token
from app.core.config import Settings, settings
from app.database import Base, get_db
from app.main import app
from app.models.cliente import Cliente
from app.models.empresa import Empresa
from app.models.financeiro import LancamentoFinanceiro
from app.models.movimento_estoque import MovimentoEstoque
from app.models.produto import Produto
from app.models.profissional import Profissional
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.models.venda import Venda


@pytest.fixture
def security_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db = factory()

    empresa_a = Empresa(
        nome="Empresa A P9",
        cnpj="91919191919191",
        email="empresa-a-p9@teste.local",
    )
    empresa_b = Empresa(
        nome="Empresa B P9",
        cnpj="92929292929292",
        email="empresa-b-p9@teste.local",
    )
    empresa_inativa = Empresa(
        nome="Empresa Inativa P9",
        cnpj="93939393939393",
        email="empresa-inativa-p9@teste.local",
        ativo=False,
    )
    db.add_all([empresa_a, empresa_b, empresa_inativa])
    db.flush()

    usuarios = {}
    for chave, perfil, empresa, ativo in (
        ("admin", "admin", empresa_a, True),
        ("gerente", "gerente", empresa_a, True),
        ("joao", "profissional", empresa_a, True),
        ("maria", "profissional", empresa_a, True),
        ("inativo", "profissional", empresa_a, False),
        ("admin_b", "admin", empresa_b, True),
        ("prof_b", "profissional", empresa_b, True),
        ("empresa_inativa", "admin", empresa_inativa, True),
    ):
        usuarios[chave] = Usuario(
            empresa_id=empresa.id,
            nome=chave.title(),
            email=f"{chave}-p9@teste.local",
            senha=gerar_hash("senha123"),
            perfil=perfil,
            ativo=ativo,
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
        "b": Profissional(
            empresa_id=empresa_b.id,
            usuario_id=usuarios["prof_b"].id,
            area_atuacao="BARBEARIA",
            percentual_padrao=Decimal("50.00"),
        ),
    }
    servicos = {
        "corte": Servico(
            empresa_id=empresa_a.id,
            nome="Corte P9",
            preco_padrao=Decimal("40.00"),
        ),
        "b": Servico(
            empresa_id=empresa_b.id,
            nome="Servico B P9",
            preco_padrao=Decimal("99.00"),
        ),
    }
    clientes = {
        "a": Cliente(nome="Cliente A P9", empresa_id=empresa_a.id),
        "b": Cliente(nome="Cliente B P9", empresa_id=empresa_b.id),
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
        Base.metadata.drop_all(engine)
        engine.dispose()


def login(ctx, chave, senha="senha123"):
    return ctx["client"].post(
        "/usuarios/login",
        data={
            "username": ctx["usuarios"][chave].email,
            "password": senha,
        },
    )


def test_autenticacao_tokens_e_contas_inativas(security_client):
    ctx = security_client
    assert login(ctx, "admin").status_code == 200
    assert login(ctx, "admin", "incorreta").status_code == 401
    inexistente = ctx["client"].post(
        "/usuarios/login",
        data={"username": "nao-existe@teste.local", "password": "senha123"},
    )
    assert inexistente.status_code == 401
    assert login(ctx, "inativo").status_code == 401
    assert login(ctx, "empresa_inativa").status_code == 401

    assert ctx["client"].get("/usuarios/me").status_code == 401
    assert ctx["client"].get(
        "/usuarios/me", headers={"Authorization": "Bearer token-invalido"}
    ).status_code == 401

    expirado = jwt.encode(
        {
            "sub": ctx["usuarios"]["admin"].email,
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    assert ctx["client"].get(
        "/usuarios/me", headers={"Authorization": f"Bearer {expirado}"}
    ).status_code == 401

    temporario = Usuario(
        empresa_id=ctx["empresa_a"].id,
        nome="Temporario",
        email="temporario-p9@teste.local",
        senha=gerar_hash("senha123"),
        perfil="operador",
    )
    ctx["db"].add(temporario)
    ctx["db"].commit()
    token_removido = criar_token({"sub": temporario.email})
    ctx["db"].delete(temporario)
    ctx["db"].commit()
    assert ctx["client"].get(
        "/usuarios/me",
        headers={"Authorization": f"Bearer {token_removido}"},
    ).status_code == 401

    token_joao = criar_token({"sub": ctx["usuarios"]["joao"].email})
    ctx["usuarios"]["joao"].ativo = False
    ctx["db"].commit()
    assert ctx["client"].get(
        "/usuarios/me",
        headers={"Authorization": f"Bearer {token_joao}"},
    ).status_code == 403


def test_fluxo_usuario_profissional_senha_hash_e_permissoes(security_client):
    ctx = security_client
    criado = ctx["client"].post(
        "/usuarios/",
        json={
            "nome": "Novo Profissional",
            "email": "novo-profissional-p9@example.com",
            "senha": "inicial123",
            "empresa_id": ctx["empresa_b"].id,
            "perfil": "profissional",
        },
        headers=ctx["headers"]("admin"),
    )
    assert criado.status_code == 200
    corpo = criado.json()
    assert corpo["empresa_id"] == ctx["empresa_a"].id
    assert corpo["perfil"] == "profissional"
    assert "senha" not in corpo

    usuario = ctx["db"].query(Usuario).filter(Usuario.id == corpo["id"]).one()
    hash_inicial = usuario.senha
    assert hash_inicial != "inicial123"
    assert verificar_senha("inicial123", hash_inicial)
    assert usuario.profissional is None

    sem_trocar_senha = ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"nome": "Novo Profissional Editado"},
        headers=ctx["headers"]("admin"),
    )
    ctx["db"].refresh(usuario)
    assert sem_trocar_senha.status_code == 200
    assert usuario.senha == hash_inicial

    senha_curta = ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"senha": "123"},
        headers=ctx["headers"]("admin"),
    )
    assert senha_curta.status_code == 422

    senha_nova = ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"senha": "novaSenha456"},
        headers=ctx["headers"]("admin"),
    )
    ctx["db"].refresh(usuario)
    assert senha_nova.status_code == 200
    assert "senha" not in senha_nova.json()
    assert usuario.senha != hash_inicial
    assert verificar_senha("novaSenha456", usuario.senha)

    assert ctx["client"].post(
        "/usuarios/login",
        data={"username": usuario.email, "password": "inicial123"},
    ).status_code == 401
    login_novo = ctx["client"].post(
        "/usuarios/login",
        data={"username": usuario.email, "password": "novaSenha456"},
    )
    assert login_novo.status_code == 200
    headers_prof = {
        "Authorization": f"Bearer {login_novo.json()['access_token']}"
    }
    assert ctx["client"].get("/usuarios/me", headers=headers_prof).json()[
        "perfil"
    ] == "profissional"
    assert ctx["client"].get("/usuarios/", headers=headers_prof).status_code == 403
    assert ctx["client"].get(
        f"/usuarios/{ctx['usuarios']['admin'].id}", headers=headers_prof
    ).status_code == 403
    assert ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"nome": "Ataque"},
        headers=headers_prof,
    ).status_code == 403


@pytest.mark.parametrize(
    ("metodo", "rota"),
    [
        ("get", "/dashboard/"),
        ("get", "/usuarios/"),
        ("get", "/profissionais/"),
        ("get", "/financeiro/lancamentos"),
        ("get", "/categorias-financeiras/"),
        ("get", "/produtos/"),
        ("get", "/produtos/1/imagens"),
        ("get", "/movimentos-estoque/"),
        ("get", "/vendas/"),
        ("get", "/empresas/me"),
    ],
)
def test_profissional_nao_acessa_endpoints_administrativos(
    security_client, metodo, rota
):
    ctx = security_client
    resposta = getattr(ctx["client"], metodo)(
        rota, headers=ctx["headers"]("joao")
    )
    assert resposta.status_code == 403


@pytest.mark.parametrize(
    "secret_key",
    ["change-me", "replace-with-at-least-32-random-characters"],
)
def test_configuracao_rejeita_secret_e_cors_inseguros(secret_key):
    with pytest.raises(ValueError):
        Settings(
            DATABASE_URL="sqlite://",
            SECRET_KEY=secret_key,
            _env_file=None,
        )
    with pytest.raises(ValueError):
        configuracao = Settings(
            DATABASE_URL="sqlite://",
            SECRET_KEY="x" * 32,
            CORS_ORIGINS="*",
            _env_file=None,
        )
        _ = configuracao.cors_origins


def test_e2e_piloto_valores_visoes_e_ataques(security_client):
    ctx = security_client
    client = ctx["client"]
    headers_prof = ctx["headers"]("joao")
    headers_admin = ctx["headers"]("admin")
    hoje = datetime.now(timezone.utc).date().isoformat()

    cliente_profissional = client.get(
        "/clientes/", headers=headers_prof
    ).json()[0]
    assert set(cliente_profissional) == {"id", "nome"}
    cliente_admin = client.get(
        f"/clientes/{ctx['clientes']['a'].id}", headers=headers_admin
    ).json()
    assert {"email", "telefone", "cpf_cnpj"}.issubset(cliente_admin)

    ids = []
    for _ in range(2):
        resposta = client.post(
            "/atendimentos/",
            json={
                "servico_id": ctx["servicos"]["corte"].id,
                "cliente_id": ctx["clientes"]["a"].id,
                "valor": "40.00",
                "forma_pagamento": "PIX",
            },
            headers=headers_prof,
        )
        assert resposta.status_code == 200
        assert resposta.json()["valor_profissional"] == 28.0
        assert "valor_casa" not in resposta.json()
        ids.append(resposta.json()["id"])

    repasse = client.post(
        "/repasses/",
        json={
            "profissional_id": ctx["profissionais"]["joao"].id,
            "forma_pagamento": "PIX",
            "itens": [{"atendimento_id": ids[0], "valor": "20.00"}],
        },
        headers=headers_admin,
    )
    assert repasse.status_code == 200

    periodo = {"data_inicio": hoje, "data_fim": hoje}
    painel = client.get(
        "/dashboard/piloto", params=periodo, headers=headers_admin
    )
    producao = client.get(
        "/dashboard/profissional/me", params=periodo, headers=headers_prof
    )
    assert painel.status_code == 200
    assert painel.json()["total_atendimentos"] == 2
    assert painel.json()["faturamento_bruto"] == "80.00"
    assert painel.json()["valor_profissionais"] == "56.00"
    assert painel.json()["valor_casa"] == "24.00"
    assert painel.json()["total_repassado"] == "20.00"
    assert painel.json()["total_pendente_repasses"] == "36.00"
    assert painel.json()["entradas_caixa_piloto"] == "80.00"
    assert painel.json()["saidas_caixa_piloto"] == "20.00"
    assert painel.json()["saldo_caixa_piloto"] == "60.00"

    assert producao.status_code == 200
    assert producao.json()["quantidade_atendimentos"] == 2
    assert producao.json()["faturamento_bruto"] == "80.00"
    assert producao.json()["valor_profissional"] == "56.00"
    assert producao.json()["valor_repassado"] == "20.00"
    assert producao.json()["valor_pendente"] == "36.00"
    assert "valor_casa" not in producao.json()

    lancamentos = client.get(
        "/financeiro/lancamentos", headers=headers_admin
    ).json()
    automaticos = [item for item in lancamentos if item["origem_tipo"]]
    assert len(automaticos) == 3
    assert sum(
        Decimal(item["valor"])
        for item in automaticos
        if item["origem_tipo"] == "ATENDIMENTO"
    ) == Decimal("80.00")
    assert sum(
        Decimal(item["valor"])
        for item in automaticos
        if item["origem_tipo"] == "REPASSE"
    ) == Decimal("20.00")
    assert {item["forma_pagamento"] for item in automaticos} == {"PIX"}

    assert client.get(
        "/dashboard/piloto", headers=headers_prof
    ).status_code == 403
    assert client.post(
        "/repasses/",
        json={
            "profissional_id": ctx["profissionais"]["joao"].id,
            "forma_pagamento": "PIX",
            "itens": [{"atendimento_id": ids[1], "valor": "1.00"}],
        },
        headers=headers_prof,
    ).status_code == 403
    assert client.post(
        "/atendimentos/",
        json={
            "profissional_id": ctx["profissionais"]["maria"].id,
            "servico_id": ctx["servicos"]["corte"].id,
            "valor": "40.00",
            "forma_pagamento": "PIX",
        },
        headers=headers_prof,
    ).status_code == 403
    assert client.post(
        "/atendimentos/",
        json={
            "servico_id": ctx["servicos"]["corte"].id,
            "valor": "40.00",
            "forma_pagamento": "PIX",
            "percentual_profissional_override": "99.00",
        },
        headers=headers_prof,
    ).status_code == 403

    atendimento_b = client.post(
        "/atendimentos/",
        json={
            "profissional_id": ctx["profissionais"]["b"].id,
            "servico_id": ctx["servicos"]["b"].id,
            "cliente_id": ctx["clientes"]["b"].id,
            "valor": "99.00",
            "forma_pagamento": "PIX",
        },
        headers=ctx["headers"]("admin_b"),
    )
    assert atendimento_b.status_code == 200
    assert client.get(
        f"/atendimentos/{atendimento_b.json()['id']}", headers=headers_admin
    ).status_code == 404
    assert client.get(
        f"/servicos/{ctx['servicos']['b'].id}", headers=headers_admin
    ).status_code == 404
    assert client.put(
        f"/servicos/{ctx['servicos']['b'].id}",
        json={"nome": "Ataque"},
        headers=headers_admin,
    ).status_code == 404
    assert client.delete(
        f"/servicos/{ctx['servicos']['b'].id}", headers=headers_admin
    ).status_code == 404
    assert client.get(
        f"/clientes/{ctx['clientes']['b'].id}", headers=headers_admin
    ).status_code == 404
    assert client.put(
        f"/clientes/{ctx['clientes']['b'].id}",
        json={"nome": "Ataque"},
        headers=headers_admin,
    ).status_code == 404
    assert client.delete(
        f"/clientes/{ctx['clientes']['b'].id}", headers=headers_admin
    ).status_code == 404
    assert client.get(
        f"/usuarios/{ctx['usuarios']['admin_b'].id}", headers=headers_admin
    ).status_code == 404
    assert client.put(
        f"/usuarios/{ctx['usuarios']['admin_b'].id}",
        json={"nome": "Ataque"},
        headers=headers_admin,
    ).status_code == 404
    assert client.delete(
        f"/usuarios/{ctx['usuarios']['admin_b'].id}", headers=headers_admin
    ).status_code == 404
    painel_b = client.get(
        "/dashboard/piloto", params=periodo, headers=ctx["headers"]("admin_b")
    )
    assert painel_b.json()["faturamento_bruto"] == "99.00"
    assert all(
        item.empresa_id == ctx["empresa_a"].id
        for item in ctx["db"].query(LancamentoFinanceiro).filter(
            LancamentoFinanceiro.empresa_id == ctx["empresa_a"].id
        )
    )


def test_isolamento_cross_tenant_produtos_estoque_vendas_financeiro(
    security_client,
):
    ctx = security_client
    db = ctx["db"]
    produto_b = Produto(
        empresa_id=ctx["empresa_b"].id,
        nome="Produto secreto B",
        preco=99,
        estoque=10,
        estoque_minimo=1,
        estoque_maximo=20,
        custo_medio=50,
    )
    db.add(produto_b)
    db.flush()
    movimento_b = MovimentoEstoque(
        empresa_id=ctx["empresa_b"].id,
        produto_id=produto_b.id,
        usuario_id=ctx["usuarios"]["admin_b"].id,
        tipo="ENTRADA",
        quantidade=10,
        estoque_anterior=0,
        estoque_posterior=10,
    )
    venda_b = Venda(
        empresa_id=ctx["empresa_b"].id,
        cliente_id=ctx["clientes"]["b"].id,
        usuario_id=ctx["usuarios"]["admin_b"].id,
        total=99,
        status="FINALIZADA",
    )
    financeiro_b = LancamentoFinanceiro(
        empresa_id=ctx["empresa_b"].id,
        usuario_id=ctx["usuarios"]["admin_b"].id,
        descricao="Lancamento secreto B",
        valor=Decimal("99.00"),
        tipo="RECEITA",
        data_vencimento=datetime.now(timezone.utc).date(),
        status="PENDENTE",
    )
    db.add_all([movimento_b, venda_b, financeiro_b])
    db.commit()

    client = ctx["client"]
    headers = ctx["headers"]("admin")
    assert client.get(f"/produtos/{produto_b.id}", headers=headers).status_code == 404
    assert client.put(
        f"/produtos/{produto_b.id}", json={"nome": "Ataque"}, headers=headers
    ).status_code == 404
    assert client.delete(
        f"/produtos/{produto_b.id}", headers=headers
    ).status_code == 404
    assert client.get(
        f"/movimentos-estoque/{movimento_b.id}", headers=headers
    ).status_code == 404
    assert client.post(
        "/movimentos-estoque/",
        json={"produto_id": produto_b.id, "tipo": "ENTRADA", "quantidade": 1},
        headers=headers,
    ).status_code == 404
    assert client.get(f"/vendas/{venda_b.id}", headers=headers).status_code == 404
    assert client.post(
        "/vendas/",
        json={
            "cliente_id": ctx["clientes"]["b"].id,
            "itens": [{"produto_id": produto_b.id, "quantidade": 1}],
        },
        headers=headers,
    ).status_code == 400
    assert client.get(
        f"/financeiro/lancamentos/{financeiro_b.id}", headers=headers
    ).status_code == 404
    assert client.put(
        f"/financeiro/lancamentos/{financeiro_b.id}",
        json={"descricao": "Ataque"},
        headers=headers,
    ).status_code == 404
    assert client.delete(
        f"/financeiro/lancamentos/{financeiro_b.id}", headers=headers
    ).status_code == 404

    assert all(
        item["empresa_id"] == ctx["empresa_a"].id
        for item in client.get("/produtos/", headers=headers).json()
    )
    assert all(
        item["empresa_id"] == ctx["empresa_a"].id
        for item in client.get("/movimentos-estoque/", headers=headers).json()
    )
    assert all(
        item["empresa_id"] == ctx["empresa_a"].id
        for item in client.get("/vendas/", headers=headers).json()
    )
    assert all(
        item["empresa_id"] == ctx["empresa_a"].id
        for item in client.get("/financeiro/lancamentos", headers=headers).json()
    )
