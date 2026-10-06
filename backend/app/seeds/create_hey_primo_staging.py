"""Provisiona a tenant Hey Primo no ambiente local/staging.

Uso explícito apenas em ambiente autorizado. O script é idempotente: não cria
duplicatas e nunca altera senhas de usuários já existentes.
"""

import json
import os
import secrets
from datetime import datetime, timezone

from app.auth.hash import gerar_hash
from app.database import SessionLocal
from app.models.empresa import Empresa
from app.models.usuario import Usuario as UsuarioModel
from app.services.modulo import inicializar_modulos_empresa


EMPRESA_NOME = "Hey Primo"
EMPRESA_EMAIL = "heyprimotabacaria@gmail.com"
EMPRESA_IDENTIFICADOR = "hey-primo-staging"
TEMP_USERS = (
    {
        "nome": "Javé",
        "email": "jave@heyprimo.com",
        "perfil": "admin",
    },
    {
        "nome": "Jeova",
        "email": "jeova@heyprimo.com",
        "perfil": "gerente",
    },
)


def _senha_temporaria():
    senha_configurada = os.getenv("HEY_PRIMO_STAGING_PASSWORD", "").strip()
    if senha_configurada:
        return senha_configurada
    return secrets.token_urlsafe(18)


def provisionar():
    db = SessionLocal()
    try:
        empresa = (
            db.query(Empresa)
            .filter(Empresa.email == EMPRESA_EMAIL)
            .first()
        )

        if empresa:
            usuarios = (
                db.query(UsuarioModel)
                .filter(UsuarioModel.empresa_id == empresa.id)
                .order_by(UsuarioModel.id)
                .all()
            )
            print(json.dumps({
                "criada": False,
                "motivo": "A tenant já existe; nada foi alterado.",
                "empresa_id": empresa.id,
                "empresa_nome": empresa.nome,
                "usuarios": [
                    {
                        "nome": usuario.nome,
                        "email": usuario.email,
                        "perfil": usuario.perfil,
                    }
                    for usuario in usuarios
                ],
            }, ensure_ascii=False))
            return

        emails_em_uso = {
            email
            for (email,) in db.query(UsuarioModel.email)
            .filter(UsuarioModel.email.in_(item["email"] for item in TEMP_USERS))
            .all()
        }
        if emails_em_uso:
            raise RuntimeError(
                "E-mail temporário já utilizado: "
                + ", ".join(sorted(emails_em_uso))
            )

        empresa = Empresa(
            nome=EMPRESA_NOME,
            identidade_codigo="hey-primo",
            cnpj=EMPRESA_IDENTIFICADOR,
            email=EMPRESA_EMAIL,
            logo_url="/tenants/hey-primo/logo.svg",
            cor_primaria="#c69b37",
            cor_secundaria="#c92b30",
            tema="dark",
            tipo_negocio="Tabacaria",
            ativo=True,
            eh_demo=False,
        )
        db.add(empresa)
        db.flush()

        credenciais = []
        for item in TEMP_USERS:
            senha = _senha_temporaria()
            db.add(
                UsuarioModel(
                    empresa_id=empresa.id,
                    nome=item["nome"],
                    email=item["email"],
                    senha=gerar_hash(senha),
                    perfil=item["perfil"],
                    ativo=True,
                )
            )
            credenciais.append({
                "nome": item["nome"],
                "email": item["email"],
                "perfil": item["perfil"],
                "senha_temporaria": senha,
            })

        inicializar_modulos_empresa(db, empresa.id, commit=False)
        db.commit()

        print(json.dumps({
            "criada": True,
            "criada_em": datetime.now(timezone.utc).isoformat(),
            "empresa_id": empresa.id,
            "empresa_nome": empresa.nome,
            "empresa_email": empresa.email,
            "identidade": empresa.identidade_codigo,
            "credenciais_temporarias": credenciais,
            "aviso": "Trocar as credenciais quando os e-mails reais forem definidos.",
        }, ensure_ascii=False))
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    provisionar()
