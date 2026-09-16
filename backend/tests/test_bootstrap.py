import io
import os
import unittest
from contextlib import redirect_stdout

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


class FailingCommitSession(Session):
    def commit(self):
        self.flush()
        raise RuntimeError("falha de commit simulada")


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        os.environ["DATABASE_URL"] = "sqlite://"
        os.environ["SECRET_KEY"] = "bootstrap_test_secret_key_with_more_than_32_chars"

        from app import models
        from app.auth.hash import verificar_senha
        from app.core.enums import PerfilUsuario
        from app.database import Base
        from app.seeds.create_admin import BootstrapConfigurationError, criar_admin

        self.Base = Base
        self.Empresa = models.Empresa
        self.Usuario = models.Usuario
        self.PerfilUsuario = PerfilUsuario
        self.verificar_senha = verificar_senha
        self.BootstrapConfigurationError = BootstrapConfigurationError
        self.criar_admin = criar_admin
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.Base.metadata.create_all(self.engine)
        self.factory = sessionmaker(bind=self.engine)
        self.env = {
            "COREERP_BOOTSTRAP_EMPRESA_NOME": "Hype Studio",
            "COREERP_BOOTSTRAP_EMPRESA_CNPJ": "12345678000199",
            "COREERP_BOOTSTRAP_EMPRESA_EMAIL": "contato@hype.test",
            "COREERP_BOOTSTRAP_EMPRESA_TELEFONE": "85999999999",
            "COREERP_BOOTSTRAP_ADMIN_NOME": "Admin Hype",
            "COREERP_BOOTSTRAP_ADMIN_EMAIL": "admin@hype.test",
            "COREERP_ADMIN_PASSWORD": "senha-bootstrap-forte",
        }

    def tearDown(self):
        self.Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def _count(self, model):
        with self.factory() as db:
            return db.query(model).count()

    def _add_empresa(self, **kwargs):
        with self.factory() as db:
            empresa = self.Empresa(
                nome=kwargs.get("nome", "Empresa existente"),
                cnpj=kwargs.get("cnpj", "99999999000199"),
                email=kwargs.get("email", "existente@hype.test"),
                ativo=True,
            )
            db.add(empresa)
            db.flush()
            if kwargs.get("admin_email"):
                db.add(
                    self.Usuario(
                        empresa_id=empresa.id,
                        nome="Admin existente",
                        email=kwargs["admin_email"],
                        senha="$2b$12$hash-existente",
                        perfil=self.PerfilUsuario.ADMIN.value,
                        ativo=True,
                    )
                )
            db.commit()

    def test_cria_empresa_admin_admin_hash_e_nao_imprime_segredos(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertTrue(self.criar_admin(self.factory, self.env))

        with self.factory() as db:
            empresa = db.query(self.Empresa).one()
            usuario = db.query(self.Usuario).one()
            self.assertEqual(usuario.empresa_id, empresa.id)
            self.assertEqual(usuario.perfil, self.PerfilUsuario.ADMIN.value)
            self.assertTrue(
                self.verificar_senha(self.env["COREERP_ADMIN_PASSWORD"], usuario.senha)
            )
            self.assertNotEqual(usuario.senha, self.env["COREERP_ADMIN_PASSWORD"])
            self.assertTrue(usuario.senha.startswith("$2"))

        self.assertNotIn(self.env["COREERP_ADMIN_PASSWORD"], output.getvalue())
        self.assertNotIn(usuario.senha, output.getvalue())

    def test_variavel_obrigatoria_falha_antes_da_sessao(self):
        env = dict(self.env)
        del env["COREERP_BOOTSTRAP_ADMIN_EMAIL"]

        def session_factory_should_not_run():
            raise AssertionError("a sessão não deveria ser criada")

        with self.assertRaises(self.BootstrapConfigurationError):
            self.criar_admin(session_factory_should_not_run, env)
        self.assertEqual(self._count(self.Empresa), 0)
        self.assertEqual(self._count(self.Usuario), 0)

    def test_conflito_de_usuario_nao_altera_registros(self):
        self._add_empresa(admin_email=self.env["COREERP_BOOTSTRAP_ADMIN_EMAIL"])

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertFalse(self.criar_admin(self.factory, self.env))

        self.assertEqual(self._count(self.Empresa), 1)
        self.assertEqual(self._count(self.Usuario), 1)
        self.assertIn("conflito", output.getvalue())
        self.assertNotIn(self.env["COREERP_ADMIN_PASSWORD"], output.getvalue())

    def test_conflito_de_cnpj_e_email_da_empresa_nao_insere(self):
        self._add_empresa(
            cnpj=self.env["COREERP_BOOTSTRAP_EMPRESA_CNPJ"],
            email=self.env["COREERP_BOOTSTRAP_EMPRESA_EMAIL"],
        )

        self.assertFalse(self.criar_admin(self.factory, self.env))
        self.assertEqual(self._count(self.Empresa), 1)
        self.assertEqual(self._count(self.Usuario), 0)

    def test_segunda_execucao_nao_duplica(self):
        self.assertTrue(self.criar_admin(self.factory, self.env))
        self.assertFalse(self.criar_admin(self.factory, self.env))

        self.assertEqual(self._count(self.Empresa), 1)
        self.assertEqual(self._count(self.Usuario), 1)

    def test_falha_no_commit_faz_rollback_completo(self):
        failing_factory = sessionmaker(
            bind=self.engine,
            class_=FailingCommitSession,
        )

        with self.assertRaises(RuntimeError):
            self.criar_admin(failing_factory, self.env)

        self.assertEqual(self._count(self.Empresa), 0)
        self.assertEqual(self._count(self.Usuario), 0)


if __name__ == "__main__":
    unittest.main()
