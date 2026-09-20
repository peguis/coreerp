import io
import unittest
from contextlib import redirect_stdout

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class DemoSeedTests(unittest.TestCase):
    def setUp(self):
        from app import models
        from app.core.modulos import MODULOS_ATUAIS
        from app.database import Base
        from app.models.modulo import Modulo
        from app.seeds.create_demo import criar_demo

        self.Base = Base
        self.Empresa = models.Empresa
        self.Usuario = models.Usuario
        self.Servico = models.Servico
        self.Profissional = models.Profissional
        self.RecursoAgenda = models.RecursoAgenda
        self.Cliente = models.Cliente
        self.Agendamento = models.Agendamento
        self.Modulo = Modulo
        self.modulos_atuais = MODULOS_ATUAIS
        self.criar_demo = criar_demo
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.Base.metadata.create_all(self.engine)
        self.factory = sessionmaker(bind=self.engine)
        with self.factory() as db:
            db.add_all(
                [
                    self.Modulo(codigo=codigo, nome=nome, ordem=ordem)
                    for ordem, (codigo, nome) in enumerate(
                        self.modulos_atuais.items(), start=1
                    )
                ]
            )
            db.commit()
        self.env = {
            "COREERP_DEMO_EMPRESA_NOME": "Studio Demo",
            "COREERP_DEMO_EMPRESA_CNPJ": "22222222000199",
            "COREERP_DEMO_EMPRESA_EMAIL": "contato@studio-demo.test",
            "COREERP_DEMO_ADMIN_NOME": "Admin Demo",
            "COREERP_DEMO_ADMIN_EMAIL": "admin@studio-demo.test",
            "COREERP_DEMO_ADMIN_PASSWORD": "senha-demo-forte",
            "COREERP_DEMO_TIPO_NEGOCIO": "STUDIO",
            "COREERP_DEMO_COR_PRIMARIA": "#D9AB3F",
            "COREERP_DEMO_COR_SECUNDARIA": "#111111",
            "COREERP_DEMO_SERVICO_NOME": "Sessão Demo",
            "COREERP_DEMO_SERVICO_CATEGORIA": "STUDIO",
            "COREERP_DEMO_SERVICO_PRECO": "180.00",
            "COREERP_DEMO_SERVICO_DURACAO": "90",
            "COREERP_DEMO_PROFISSIONAL_AREA": "STUDIO_LONGO",
            "COREERP_DEMO_PROFISSIONAL_PERCENTUAL": "60",
            "COREERP_DEMO_RECURSO_NOME": "Sala Demo",
            "COREERP_DEMO_RECURSO_TIPO": "SALA",
            "COREERP_DEMO_CLIENTE_NOME": "Cliente Demo",
            "COREERP_DEMO_AGENDAMENTO_INICIO": "2026-10-01T10:00:00",
        }

    def tearDown(self):
        self.Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_cria_demo_com_dados_opcionais_e_isolamento(self):
        with self.factory() as db:
            empresa_existente = self.Empresa(
                nome="Empresa Existente",
                cnpj="77777777000199",
                email="existente@coreerp.com",
            )
            db.add(empresa_existente)
            db.flush()
            db.add(
                self.Usuario(
                    empresa_id=empresa_existente.id,
                    nome="Admin Existente",
                    email="admin-existente@coreerp.com",
                    senha="hash-existente",
                    perfil="admin",
                    ativo=True,
                )
            )
            db.commit()

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertTrue(self.criar_demo(self.factory, self.env))

        with self.factory() as db:
            empresa = db.query(self.Empresa).filter(
                self.Empresa.cnpj == self.env["COREERP_DEMO_EMPRESA_CNPJ"]
            ).one()
            usuario = db.query(self.Usuario).filter(
                self.Usuario.email == self.env["COREERP_DEMO_ADMIN_EMAIL"]
            ).one()
            servico = db.query(self.Servico).one()
            profissional = db.query(self.Profissional).one()
            recurso = db.query(self.RecursoAgenda).one()
            cliente = db.query(self.Cliente).one()
            agendamento = db.query(self.Agendamento).one()

            self.assertEqual(empresa.nome, "Studio Demo")
            self.assertEqual(usuario.empresa_id, empresa.id)
            self.assertEqual(servico.empresa_id, empresa.id)
            self.assertEqual(servico.duracao_minutos, 90)
            self.assertEqual(str(servico.preco_padrao), "180.00")
            self.assertEqual(profissional.area_atuacao, "STUDIO_LONGO")
            self.assertEqual(recurso.empresa_id, empresa.id)
            self.assertEqual(cliente.empresa_id, empresa.id)
            self.assertEqual(agendamento.empresa_id, empresa.id)
            self.assertEqual(agendamento.duracao_minutos, 90)
            self.assertEqual(str(agendamento.preco_aplicado), "180.00")
            self.assertEqual(db.query(self.Modulo).count(), len(self.modulos_atuais))
            self.assertEqual(len(empresa.modulos), len(self.modulos_atuais))

        self.assertNotIn(self.env["COREERP_DEMO_ADMIN_PASSWORD"], output.getvalue())
        self.assertFalse(self.criar_demo(self.factory, self.env))

    def test_dashboard_aceita_area_configuravel(self):
        from app.schemas.dashboard_piloto import (
            DesempenhoProfissionalResponse,
        )

        resposta = DesempenhoProfissionalResponse(
            profissional_id=1,
            nome="Profissional Demo",
            area_atuacao="STUDIO",
            quantidade_atendimentos=0,
            faturamento_bruto=0,
            valor_profissional=0,
            valor_casa=0,
            valor_repassado=0,
            valor_pendente=0,
        )

        self.assertEqual(resposta.area_atuacao, "STUDIO")


if __name__ == "__main__":
    unittest.main()
