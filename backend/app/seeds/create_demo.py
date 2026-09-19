"""Provisiona uma empresa-demo isolada para validação local da Pegs.

Este módulo não é executado pela aplicação nem pela migração. Ele só deve ser
chamado explicitamente em um banco local/staging com as variáveis COREERP_DEMO_*.
Assim, dados de demonstração nunca são inseridos silenciosamente na HYPE.
"""

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Mapping

from sqlalchemy import func

from app.auth.hash import gerar_hash
from app.database import SessionLocal
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.empresa import Empresa
from app.models.profissional import Profissional
from app.models.recurso_agenda import RecursoAgenda
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.services.modulo import inicializar_modulos_empresa


class DemoConfigurationError(ValueError):
    """Raised when the explicit demo configuration is incomplete."""


@dataclass(frozen=True)
class DemoConfig:
    empresa_nome: str
    empresa_cnpj: str
    empresa_email: str
    admin_nome: str
    admin_email: str
    admin_password: str
    tipo_negocio: str | None
    cor_primaria: str | None
    cor_secundaria: str | None
    servico_nome: str | None
    servico_categoria: str | None
    servico_preco: Decimal
    servico_duracao: int
    profissional_area: str | None
    profissional_percentual: Decimal
    recurso_nome: str | None
    recurso_tipo: str | None
    cliente_nome: str | None
    agendamento_inicio: datetime | None


def _required(env: Mapping[str, str], name: str) -> str:
    value = env.get(name)
    if value is None or not value.strip():
        raise DemoConfigurationError(f"Variável obrigatória ausente: {name}")
    return value.strip()


def _optional(env: Mapping[str, str], name: str) -> str | None:
    value = env.get(name)
    return value.strip() if value and value.strip() else None


def _read_config(env: Mapping[str, str] | None = None) -> DemoConfig:
    source = os.environ if env is None else env
    password = _required(source, "COREERP_DEMO_ADMIN_PASSWORD")
    inicio_texto = _optional(source, "COREERP_DEMO_AGENDAMENTO_INICIO")
    try:
        inicio = datetime.fromisoformat(inicio_texto) if inicio_texto else None
    except ValueError as exc:
        raise DemoConfigurationError(
            "COREERP_DEMO_AGENDAMENTO_INICIO deve estar em formato ISO."
        ) from exc

    try:
        preco = Decimal(_optional(source, "COREERP_DEMO_SERVICO_PRECO") or "0")
        duracao = int(_optional(source, "COREERP_DEMO_SERVICO_DURACAO") or "40")
        percentual = Decimal(
            _optional(source, "COREERP_DEMO_PROFISSIONAL_PERCENTUAL") or "50"
        )
    except (ValueError, ArithmeticError) as exc:
        raise DemoConfigurationError(
            "Preço e duração do serviço-demo devem ser numéricos."
        ) from exc
    if (
        preco < 0
        or duracao <= 0
        or duracao > 1440
        or percentual < 0
        or percentual > 100
    ):
        raise DemoConfigurationError("Preço ou duração do serviço-demo inválidos.")

    return DemoConfig(
        empresa_nome=_required(source, "COREERP_DEMO_EMPRESA_NOME"),
        empresa_cnpj=_required(source, "COREERP_DEMO_EMPRESA_CNPJ"),
        empresa_email=_required(source, "COREERP_DEMO_EMPRESA_EMAIL").lower(),
        admin_nome=_required(source, "COREERP_DEMO_ADMIN_NOME"),
        admin_email=_required(source, "COREERP_DEMO_ADMIN_EMAIL").lower(),
        admin_password=password,
        tipo_negocio=_optional(source, "COREERP_DEMO_TIPO_NEGOCIO"),
        cor_primaria=_optional(source, "COREERP_DEMO_COR_PRIMARIA"),
        cor_secundaria=_optional(source, "COREERP_DEMO_COR_SECUNDARIA"),
        servico_nome=_optional(source, "COREERP_DEMO_SERVICO_NOME"),
        servico_categoria=_optional(source, "COREERP_DEMO_SERVICO_CATEGORIA"),
        servico_preco=preco,
        servico_duracao=duracao,
        profissional_area=_optional(source, "COREERP_DEMO_PROFISSIONAL_AREA"),
        profissional_percentual=percentual,
        recurso_nome=_optional(source, "COREERP_DEMO_RECURSO_NOME"),
        recurso_tipo=_optional(source, "COREERP_DEMO_RECURSO_TIPO"),
        cliente_nome=_optional(source, "COREERP_DEMO_CLIENTE_NOME"),
        agendamento_inicio=inicio,
    )


def _find_conflicts(db, config: DemoConfig) -> list[str]:
    conflicts = []
    if db.query(Empresa).filter(Empresa.cnpj == config.empresa_cnpj).first():
        conflicts.append("CNPJ da empresa")
    if db.query(Empresa).filter(
        func.lower(Empresa.email) == config.empresa_email
    ).first():
        conflicts.append("e-mail da empresa")
    if db.query(Usuario).filter(
        func.lower(Usuario.email) == config.admin_email
    ).first():
        conflicts.append("e-mail do administrador")
    return conflicts


def criar_demo(session_factory=SessionLocal, env: Mapping[str, str] | None = None) -> bool:
    """Cria uma empresa-demo e dados opcionais sem tocar em outro tenant."""
    config = _read_config(env)
    db = session_factory()
    try:
        conflicts = _find_conflicts(db, config)
        if conflicts:
            db.rollback()
            print("Demo não criada: conflito em " + ", ".join(conflicts) + ".")
            return False

        if len(config.empresa_nome.strip()) < 3:
            raise DemoConfigurationError(
                "COREERP_DEMO_EMPRESA_NOME deve possuir no mínimo 3 caracteres."
            )
        empresa = Empresa(
            nome=config.empresa_nome,
            cnpj=config.empresa_cnpj,
            email=config.empresa_email,
            tipo_negocio=config.tipo_negocio,
            cor_primaria=config.cor_primaria,
            cor_secundaria=config.cor_secundaria,
            ativo=True,
        )
        db.add(empresa)
        db.flush()
        admin = Usuario(
            empresa_id=empresa.id,
            nome=config.admin_nome,
            email=config.admin_email,
            senha=gerar_hash(config.admin_password),
            perfil="admin",
            ativo=True,
        )
        db.add(admin)
        db.flush()
        inicializar_modulos_empresa(db, empresa.id, commit=False)

        profissional = None
        servico = None
        recurso = None
        cliente = None
        if config.servico_nome:
            servico = Servico(
                empresa_id=empresa.id,
                nome=config.servico_nome,
                categoria=config.servico_categoria,
                preco_padrao=config.servico_preco,
                duracao_minutos=config.servico_duracao,
                requer_recurso=bool(config.recurso_nome),
                tipo_recurso=config.recurso_tipo,
                ativo=True,
            )
            db.add(servico)
        if config.profissional_area:
            profissional = Profissional(
                empresa_id=empresa.id,
                usuario_id=admin.id,
                area_atuacao=config.profissional_area.upper(),
                percentual_padrao=config.profissional_percentual,
                ativo=True,
            )
            db.add(profissional)
        if config.recurso_nome and config.recurso_tipo:
            recurso = RecursoAgenda(
                empresa_id=empresa.id,
                nome=config.recurso_nome,
                tipo=config.recurso_tipo,
                ativo=True,
                status="ATIVO",
            )
            db.add(recurso)
        if config.cliente_nome:
            cliente = Cliente(empresa_id=empresa.id, nome=config.cliente_nome, ativo=True)
            db.add(cliente)
        db.flush()

        if config.agendamento_inicio and profissional and servico:
            inicio = config.agendamento_inicio
            fim = inicio + timedelta(minutes=servico.duracao_minutos)
            db.add(
                Agendamento(
                    empresa_id=empresa.id,
                    profissional_id=profissional.id,
                    servico_id=servico.id,
                    cliente_id=cliente.id if cliente else None,
                    recurso_id=recurso.id if recurso else None,
                    criado_por_usuario_id=admin.id,
                    inicio_em=inicio,
                    fim_em=fim,
                    duracao_minutos=servico.duracao_minutos,
                    preco_aplicado=servico.preco_padrao,
                    status="AGENDADO",
                )
            )
        db.commit()
        print("Empresa-demo criada com isolamento próprio e módulos ativados.")
        return True
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        if not criar_demo():
            raise SystemExit(2)
    except DemoConfigurationError as exc:
        print(f"Demo abortada: {exc}")
        raise SystemExit(1) from None
    except Exception:
        print("Demo abortada: nenhuma alteração foi aplicada.")
        raise SystemExit(1) from None
