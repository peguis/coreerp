from app.database import SessionLocal

from app.models.usuario import Usuario
from app.models.empresa import Empresa

from app.auth.hash import gerar_hash


def criar_admin():

    db = SessionLocal()

    try:

        usuario_existente = (
            db.query(Usuario)
            .filter(
                Usuario.email == "admin@coreerp.com"
            )
            .first()
        )


        if usuario_existente:

            print("Admin já existe")

            return


        empresa = Empresa(
            nome="CoreERP Empresa Demo",
            cnpj="00.000.000/0001-00",
            email="admin@coreerp.com",
            telefone="000000000",
            ativo=True
        )


        db.add(empresa)

        db.flush()


        usuario = Usuario(
            empresa_id=empresa.id,
            nome="Administrador",
            email="admin@coreerp.com",
            senha=gerar_hash("admin123"),
            ativo=True
        )


        db.add(usuario)

        db.commit()


        print("Admin criado com sucesso")
        print("Email: admin@coreerp.com")
        print("Senha: admin123")


    finally:

        db.close()



if __name__ == "__main__":

    criar_admin()