import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.jwt import criar_token
from app.database import Base, get_db
from app.main import app
from app.models.empresa import Empresa
from app.models.servico import Servico
from app.models.usuario import Usuario


@pytest.fixture
def servico_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(
        engine,
        tables=[Empresa.__table__, Usuario.__table__, Servico.__table__],
    )
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    empresa_a = Empresa(
        nome="Empresa A",
        cnpj="11111111111111",
        email="empresa-a@teste.local",
    )
    empresa_b = Empresa(
        nome="Empresa B",
        cnpj="22222222222222",
        email="empresa-b@teste.local",
    )
    db.add_all([empresa_a, empresa_b])
    db.flush()

    usuario_a = Usuario(
        nome="Admin A",
        email="admin-a@teste.local",
        senha="nao usada",
        perfil="admin",
        empresa_id=empresa_a.id,
    )
    usuario_b = Usuario(
        nome="Admin B",
        email="admin-b@teste.local",
        senha="nao usada",
        perfil="admin",
        empresa_id=empresa_b.id,
    )
    db.add_all([usuario_a, usuario_b])
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    def headers(usuario):
        token = criar_token({"sub": usuario.email})
        return {"Authorization": f"Bearer {token}"}

    try:
        yield client, headers(usuario_a), headers(usuario_b)
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(
            engine,
            tables=[Servico.__table__, Usuario.__table__, Empresa.__table__],
        )
        engine.dispose()


def test_cria_lista_e_isola_por_empresa(servico_client):
    client, headers_a, headers_b = servico_client

    criado = client.post(
        "/servicos/",
        json={"nome": "Corte", "preco_padrao": 0},
        headers=headers_a,
    )

    assert criado.status_code == 200
    servico = criado.json()
    assert servico["ativo"] is True
    assert servico["preco_padrao"] == 0

    lista_a = client.get("/servicos/", headers=headers_a)
    lista_b = client.get("/servicos/", headers=headers_b)

    assert lista_a.status_code == 200
    assert len(lista_a.json()) == 1
    assert lista_a.json()[0]["empresa_id"] == servico["empresa_id"]
    assert lista_b.status_code == 200
    assert lista_b.json() == []

    acesso_cross_tenant = client.get(
        f"/servicos/{servico['id']}",
        headers=headers_b,
    )
    assert acesso_cross_tenant.status_code == 404


def test_cross_tenant_nao_edita_nem_desativa(servico_client):
    client, headers_a, headers_b = servico_client
    criado = client.post(
        "/servicos/",
        json={"nome": "Barba", "preco_padrao": 25},
        headers=headers_a,
    ).json()

    edicao = client.put(
        f"/servicos/{criado['id']}",
        json={"nome": "Tentativa", "preco_padrao": 1},
        headers=headers_b,
    )
    exclusao = client.delete(
        f"/servicos/{criado['id']}",
        headers=headers_b,
    )

    assert edicao.status_code == 404
    assert exclusao.status_code == 404
    assert client.get(
        f"/servicos/{criado['id']}",
        headers=headers_a,
    ).json()["ativo"] is True


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco_padrao": 10},
        {"nome": "   ", "preco_padrao": 10},
        {"nome": "Invalido", "preco_padrao": -1},
    ],
)
def test_rejeita_nome_vazio_e_preco_negativo(servico_client, payload):
    client, headers_a, _ = servico_client

    response = client.post("/servicos/", json=payload, headers=headers_a)

    assert response.status_code == 422


def test_zero_update_filtros_e_paginacao(servico_client):
    client, headers_a, _ = servico_client
    primeiro = client.post(
        "/servicos/",
        json={"nome": "Corte", "preco_padrao": 0},
        headers=headers_a,
    ).json()
    client.post(
        "/servicos/",
        json={"nome": "Barba", "preco_padrao": 30},
        headers=headers_a,
    )

    atualizado = client.put(
        f"/servicos/{primeiro['id']}",
        json={"nome": "Corte premium", "descricao": "Atualizado"},
        headers=headers_a,
    )
    assert atualizado.status_code == 200
    assert atualizado.json()["empresa_id"] == primeiro["empresa_id"]

    desativado = client.delete(
        f"/servicos/{primeiro['id']}",
        headers=headers_a,
    )
    assert desativado.status_code == 200

    ativos = client.get(
        "/servicos/?ativo=true&busca=Bar&pagina=1&limite=1",
        headers=headers_a,
    )
    inativos = client.get(
        "/servicos/?ativo=false&pagina=1&limite=10",
        headers=headers_a,
    )

    assert [item["nome"] for item in ativos.json()] == ["Barba"]
    assert [item["nome"] for item in inativos.json()] == ["Corte premium"]
