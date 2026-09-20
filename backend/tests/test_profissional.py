import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.jwt import criar_token
from app.database import Base, get_db
from app.main import app
from app.models.empresa import Empresa
from app.models.profissional import Profissional
from app.models.usuario import Usuario


@pytest.fixture
def profissional_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(
        engine,
        tables=[
            Empresa.__table__,
            Usuario.__table__,
            Profissional.__table__,
        ],
    )
    session_factory = sessionmaker(bind=engine)
    db = session_factory()

    empresa_a = Empresa(
        nome="Empresa A",
        cnpj="33333333333333",
        email="prof-empresa-a@teste.local",
    )
    empresa_b = Empresa(
        nome="Empresa B",
        cnpj="44444444444444",
        email="prof-empresa-b@teste.local",
    )
    db.add_all([empresa_a, empresa_b])
    db.flush()

    usuarios = {
        "admin_a": Usuario(
            nome="Admin A",
            email="prof-admin-a@example.com",
            senha="nao usada",
            perfil="admin",
            empresa_id=empresa_a.id,
        ),
        "admin_b": Usuario(
            nome="Admin B",
            email="prof-admin-b@example.com",
            senha="nao usada",
            perfil="admin",
            empresa_id=empresa_b.id,
        ),
        "gerente_a": Usuario(
            nome="Gerente A",
            email="prof-gerente-a@example.com",
            senha="nao usada",
            perfil="gerente",
            empresa_id=empresa_a.id,
        ),
        "a1": Usuario(
            nome="Ana Barbeira",
            email="ana@example.com",
            senha="nao usada",
            perfil="profissional",
            empresa_id=empresa_a.id,
        ),
        "a2": Usuario(
            nome="Bruno Tattoo",
            email="bruno@example.com",
            senha="nao usada",
            perfil="profissional",
            empresa_id=empresa_a.id,
        ),
        "a3": Usuario(
            nome="Carla Profissional",
            email="carla@example.com",
            senha="nao usada",
            perfil="operador",
            empresa_id=empresa_a.id,
        ),
        "b1": Usuario(
            nome="Diego Barbeiro",
            email="diego@example.com",
            senha="nao usada",
            perfil="profissional",
            empresa_id=empresa_b.id,
        ),
    }
    db.add_all(usuarios.values())
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    def headers(usuario):
        token = criar_token({"sub": usuario.email})
        return {"Authorization": f"Bearer {token}"}

    contexto = {
        "client": client,
        "db": db,
        "empresa_a": empresa_a,
        "empresa_b": empresa_b,
        "usuarios": usuarios,
        "headers_a": headers(usuarios["admin_a"]),
        "headers_b": headers(usuarios["admin_b"]),
        "headers_gerente_a": headers(usuarios["gerente_a"]),
    }

    try:
        yield contexto
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(
            engine,
            tables=[
                Profissional.__table__,
                Usuario.__table__,
                Empresa.__table__,
            ],
        )
        engine.dispose()


def criar_profissional(client, headers, usuario_id, area="BARBEARIA", percentual=40):
    return client.post(
        "/profissionais/",
        json={
            "usuario_id": usuario_id,
            "area_atuacao": area,
            "percentual_padrao": percentual,
        },
        headers=headers,
    )


def test_cria_profissional_mesma_empresa_e_impede_duplicidade(
    profissional_client,
):
    ctx = profissional_client
    usuario_a = ctx["usuarios"]["a1"]

    criado = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        usuario_a.id,
    )
    duplicado = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        usuario_a.id,
    )
    usuario_b = ctx["usuarios"]["b1"]
    cross_tenant = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        usuario_b.id,
    )

    assert criado.status_code == 200
    assert criado.json()["empresa_id"] == ctx["empresa_a"].id
    assert criado.json()["ativo"] is True
    assert duplicado.status_code == 409
    assert cross_tenant.status_code == 400


def test_percentuais_limites_e_areas_configuraveis(profissional_client):
    ctx = profissional_client

    zero = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a1"].id,
        area="BARBEARIA",
        percentual=0,
    )
    cem = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a2"].id,
        area="TATTOO",
        percentual=100,
    )
    negativo = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a3"].id,
        percentual=-1,
    )
    acima_cem = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a3"].id,
        percentual=100.01,
    )
    area_configuravel = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a3"].id,
        area="ESTETICA",
    )

    assert zero.status_code == 200
    assert zero.json()["percentual_padrao"] == 0
    assert zero.json()["area_atuacao"] == "BARBEARIA"
    assert cem.status_code == 200
    assert cem.json()["percentual_padrao"] == 100
    assert cem.json()["area_atuacao"] == "TATTOO"
    assert negativo.status_code == 422
    assert acima_cem.status_code == 422
    assert area_configuravel.status_code == 200
    assert area_configuravel.json()["area_atuacao"] == "ESTETICA"


def test_cross_tenant_nao_consulta_edita_ou_desativa(profissional_client):
    ctx = profissional_client
    profissional = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a1"].id,
    ).json()

    consulta = ctx["client"].get(
        f"/profissionais/{profissional['id']}",
        headers=ctx["headers_b"],
    )
    edicao = ctx["client"].put(
        f"/profissionais/{profissional['id']}",
        json={"percentual_padrao": 99},
        headers=ctx["headers_b"],
    )
    exclusao = ctx["client"].delete(
        f"/profissionais/{profissional['id']}",
        headers=ctx["headers_b"],
    )

    assert consulta.status_code == 404
    assert edicao.status_code == 404
    assert exclusao.status_code == 404
    assert ctx["client"].get(
        f"/profissionais/{profissional['id']}",
        headers=ctx["headers_a"],
    ).json()["ativo"] is True

    desativado = ctx["client"].delete(
        f"/profissionais/{profissional['id']}",
        headers=ctx["headers_a"],
    )
    assert desativado.status_code == 200
    assert ctx["client"].get(
        f"/profissionais/{profissional['id']}",
        headers=ctx["headers_a"],
    ).json()["ativo"] is False


def test_usuario_id_e_empresa_id_sao_imutaveis(profissional_client):
    ctx = profissional_client
    profissional = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a1"].id,
    ).json()

    troca_usuario = ctx["client"].put(
        f"/profissionais/{profissional['id']}",
        json={"usuario_id": ctx["usuarios"]["a2"].id},
        headers=ctx["headers_a"],
    )
    troca_empresa = ctx["client"].put(
        f"/profissionais/{profissional['id']}",
        json={"empresa_id": ctx["empresa_b"].id},
        headers=ctx["headers_a"],
    )

    assert troca_usuario.status_code == 422
    assert troca_empresa.status_code == 422


def test_perfil_profissional_faz_login_sem_acesso_administrativo(
    profissional_client,
):
    ctx = profissional_client
    novo_usuario = ctx["client"].post(
        "/usuarios/",
        json={
            "nome": "Profissional Login",
            "email": "login-profissional@example.com",
            "senha": "senha123",
            "empresa_id": ctx["empresa_b"].id,
            "perfil": "profissional",
        },
        headers=ctx["headers_a"],
    )

    assert novo_usuario.status_code == 200
    assert novo_usuario.json()["perfil"] == "profissional"
    assert novo_usuario.json()["empresa_id"] == ctx["empresa_a"].id

    login = ctx["client"].post(
        "/usuarios/login",
        data={
            "username": "login-profissional@example.com",
            "password": "senha123",
        },
    )
    assert login.status_code == 200

    headers_profissional = {
        "Authorization": f"Bearer {login.json()['access_token']}"
    }
    acesso_profissionais = ctx["client"].get(
        "/profissionais/",
        headers=headers_profissional,
    )
    acesso_usuarios = ctx["client"].get(
        "/usuarios/",
        headers=headers_profissional,
    )
    assert acesso_profissionais.status_code == 403
    assert acesso_usuarios.status_code == 403


def test_admin_pode_editar_usuario_para_perfil_profissional(
    profissional_client,
):
    ctx = profissional_client
    usuario = ctx["usuarios"]["a3"]

    atualizado = ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"perfil": "profissional"},
        headers=ctx["headers_a"],
    )
    invalido = ctx["client"].put(
        f"/usuarios/{usuario.id}",
        json={"perfil": "superadmin"},
        headers=ctx["headers_a"],
    )

    assert atualizado.status_code == 200
    assert atualizado.json()["perfil"] == "profissional"
    assert invalido.status_code == 422


def test_gerente_pode_alterar_area_do_profissional_sem_alterar_percentual(
    profissional_client,
):
    ctx = profissional_client
    profissional = criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a1"].id,
        area="BARBEARIA",
        percentual=40,
    ).json()

    alterado = ctx["client"].put(
        f"/profissionais/{profissional['id']}",
        json={"area_atuacao": "TATTOO"},
        headers=ctx["headers_gerente_a"],
    )
    percentual_bloqueado = ctx["client"].put(
        f"/profissionais/{profissional['id']}",
        json={"percentual_padrao": 80},
        headers=ctx["headers_gerente_a"],
    )

    assert alterado.status_code == 200
    assert alterado.json()["area_atuacao"] == "TATTOO"
    assert alterado.json()["percentual_padrao"] == 40
    assert percentual_bloqueado.status_code == 403


def test_listagem_filtros_e_isolamento(profissional_client):
    ctx = profissional_client
    criar_profissional(
        ctx["client"],
        ctx["headers_a"],
        ctx["usuarios"]["a1"].id,
        area="BARBEARIA",
    )
    criar_profissional(
        ctx["client"],
        ctx["headers_b"],
        ctx["usuarios"]["b1"].id,
        area="TATTOO",
    )

    lista_a = ctx["client"].get(
        "/profissionais/?area_atuacao=BARBEARIA&busca=Ana",
        headers=ctx["headers_a"],
    )
    lista_b = ctx["client"].get(
        "/profissionais/",
        headers=ctx["headers_b"],
    )

    assert lista_a.status_code == 200
    assert len(lista_a.json()) == 1
    assert lista_a.json()[0]["empresa_id"] == ctx["empresa_a"].id
    assert lista_b.status_code == 200
    assert len(lista_b.json()) == 1
    assert lista_b.json()[0]["empresa_id"] == ctx["empresa_b"].id
