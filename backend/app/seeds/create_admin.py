import os
from dataclasses import dataclass
from typing import Mapping

from sqlalchemy import func

from app.auth.hash import gerar_hash
from app.core.identidade import IDENTIDADE_PEGS_DEMO, resolver_identidade_codigo
from app.core.enums import PerfilUsuario
from app.database import SessionLocal
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.services.modulo import inicializar_modulos_empresa


class BootstrapConfigurationError(ValueError):
    """Raised when the bootstrap configuration is incomplete."""


@dataclass(frozen=True)
class BootstrapConfig:
    empresa_nome: str
    empresa_cnpj: str
    empresa_email: str
    empresa_telefone: str | None
    admin_nome: str
    admin_email: str
    admin_password: str
    admin_perfil: str


def _required(env: Mapping[str, str], name: str) -> str:
    value = env.get(name)
    if value is None or not value.strip():
        raise BootstrapConfigurationError(
            f"Variável obrigatória ausente ou vazia: {name}"
        )
    return value.strip()


def _optional(env: Mapping[str, str], name: str) -> str | None:
    value = env.get(name)
    return value.strip() if value and value.strip() else None


def _read_config(env: Mapping[str, str] | None = None) -> BootstrapConfig:
    source = os.environ if env is None else env
    password = source.get("COREERP_ADMIN_PASSWORD")
    if password is None or not password.strip():
        raise BootstrapConfigurationError(
            "Variável obrigatória ausente ou vazia: COREERP_ADMIN_PASSWORD"
        )

    admin_perfil = source.get("COREERP_BOOTSTRAP_ADMIN_PERFIL", "admin").strip().lower()
    if admin_perfil not in {PerfilUsuario.ADMIN.value, PerfilUsuario.PEGS_ADMIN.value}:
        raise BootstrapConfigurationError(
            "COREERP_BOOTSTRAP_ADMIN_PERFIL deve ser admin ou pegs_admin"
        )

    return BootstrapConfig(
        empresa_nome=_required(source, "COREERP_BOOTSTRAP_EMPRESA_NOME"),
        empresa_cnpj=_required(source, "COREERP_BOOTSTRAP_EMPRESA_CNPJ"),
        empresa_email=_required(source, "COREERP_BOOTSTRAP_EMPRESA_EMAIL").lower(),
        empresa_telefone=_optional(source, "COREERP_BOOTSTRAP_EMPRESA_TELEFONE"),
        admin_nome=_required(source, "COREERP_BOOTSTRAP_ADMIN_NOME"),
        admin_email=_required(source, "COREERP_BOOTSTRAP_ADMIN_EMAIL").lower(),
        admin_password=password,
        admin_perfil=admin_perfil,
    )


def _find_conflicts(db, config: BootstrapConfig) -> list[str]:
    conflicts = []
    if db.query(Empresa).filter(Empresa.cnpj == config.empresa_cnpj).first():
        conflicts.append("CNPJ da empresa")
    if (
        db.query(Empresa)
        .filter(func.lower(Empresa.email) == config.empresa_email)
        .first()
    ):
        conflicts.append("e-mail da empresa")
    if (
        db.query(Usuario)
        .filter(func.lower(Usuario.email) == config.admin_email)
        .first()
    ):
        conflicts.append("e-mail do usuário ADMIN")
    return conflicts


def criar_admin(session_factory=SessionLocal, env: Mapping[str, str] | None = None) -> bool:
    """Create the first production tenant and its ADMIN in one transaction.

    Returns False on a pre-existing conflict and never mutates that record.
    """
    config = _read_config(env)
    db = session_factory()

    try:
        conflicts = _find_conflicts(db, config)
        if conflicts:
            db.rollback()
            print(
                "Bootstrap não executado: conflito detectado em "
                + ", ".join(conflicts)
                + ". Nenhum registro foi alterado."
            )
            return False

        empresa = Empresa(
            nome=config.empresa_nome,
            identidade_codigo=resolver_identidade_codigo(
                None,
                nome=config.empresa_nome,
                email=config.empresa_email,
                padrao=IDENTIDADE_PEGS_DEMO,
            ),
            cnpj=config.empresa_cnpj,
            email=config.empresa_email,
            telefone=config.empresa_telefone,
            ativo=True,
            eh_matriz=config.admin_perfil == PerfilUsuario.PEGS_ADMIN.value,
        )
        db.add(empresa)
        db.flush()

        usuario = Usuario(
            empresa_id=empresa.id,
            nome=config.admin_nome,
            email=config.admin_email,
            senha=gerar_hash(config.admin_password),
            perfil=config.admin_perfil,
            ativo=True,
        )
        db.add(usuario)
        inicializar_modulos_empresa(db, empresa.id, commit=False)
        db.commit()
        print("Bootstrap concluído: empresa e usuário ADMIN criados.")
        return True
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        if not criar_admin():
            raise SystemExit(2)
    except BootstrapConfigurationError as exc:
        print(f"Bootstrap abortado: {exc}")
        raise SystemExit(1) from None
    except Exception:
        print("Bootstrap abortado: nenhuma alteração foi aplicada.")
        raise SystemExit(1) from None
