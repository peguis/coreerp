import os

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


os.environ["DATABASE_URL"] = (
    "sqlite:///./.tmp-p9-bootstrap.db"
)

os.environ["SECRET_KEY"] = "teste_secret_key_com_mais_de_32_caracteres"


from app.main import app
from app.auth.hash import gerar_hash
from app.database import Base, get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.models.modulo import EmpresaModulo, Modulo
from app.core.modulos import MODULOS_ATUAIS


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db = factory()
    empresa = Empresa(
        nome="Empresa Teste",
        cnpj="00000000000000",
        email="empresa-teste@coreerp.com",
    )
    db.add(empresa)
    db.flush()
    modulos = [
        Modulo(
            codigo=codigo,
            nome=nome,
            ordem=indice,
        )
        for indice, (codigo, nome) in enumerate(MODULOS_ATUAIS.items(), start=1)
    ]
    db.add_all(modulos)
    db.flush()
    db.add_all(
        [
            EmpresaModulo(empresa_id=empresa.id, modulo_id=modulo.id, ativo=True)
            for modulo in modulos
        ]
    )
    db.add(
        Usuario(
            empresa_id=empresa.id,
            nome="Administrador Teste",
            email="admin@coreerp.com",
            senha=gerar_hash("123456"),
            perfil="admin",
            ativo=True,
        )
    )
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def auth_headers(client):

    response = client.post(
        "/usuarios/login",
        data={
            "username": "admin@coreerp.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
