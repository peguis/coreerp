import os

from app.database import SessionLocal

from app.models.empresa import Empresa
from app.models.usuario import Usuario

from app.auth.hash import gerar_hash


senha_demo = os.getenv("COREERP_DEMO_PASSWORD")
if not senha_demo:
    raise RuntimeError(
        "COREERP_DEMO_PASSWORD deve ser definida para executar o seed manual."
    )


db = SessionLocal()


empresa = db.query(Empresa).filter(
    Empresa.email == "demo@coreerp.com"
).first()


if not empresa:

    empresa = Empresa(
        nome="CoreERP Demo LTDA",
        cnpj="00.000.000/0001-00",
        email="demo@coreerp.com",
        telefone="84999999999",
        ativo=True
    )

    db.add(empresa)
    db.commit()
    db.refresh(empresa)



usuario = db.query(Usuario).filter(
    Usuario.email == "admin@demo.com"
).first()


if not usuario:

    usuario = Usuario(
        empresa_id=empresa.id,
        nome="Administrador Demo",
        email="admin@demo.com",
        senha=gerar_hash(senha_demo),
        ativo=True
    )

    db.add(usuario)
    db.commit()


print("Seed concluído")
print("Login: admin@demo.com")


db.close()
