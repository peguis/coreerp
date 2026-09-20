from __future__ import annotations

import re


IDENTIDADE_HYPE = "hype"
IDENTIDADE_PEGS_DEMO = "pegs-demo"
IDENTIDADES_VALIDAS = frozenset({IDENTIDADE_HYPE, IDENTIDADE_PEGS_DEMO})


def normalizar_identidade_codigo(codigo: str | None) -> str | None:
    valor = (codigo or "").strip().lower().replace("_", "-")
    aliases = {
        "pegs": IDENTIDADE_PEGS_DEMO,
        "coreerp": IDENTIDADE_PEGS_DEMO,
        "demo": IDENTIDADE_PEGS_DEMO,
        "hype-studio": IDENTIDADE_HYPE,
    }
    valor = aliases.get(valor, valor)
    return valor if valor in IDENTIDADES_VALIDAS else None


def inferir_identidade_codigo(nome: str | None, email: str | None) -> str | None:
    texto = f"{nome or ''} {email or ''}".strip().lower()
    if re.search(r"\bhype\b", texto):
        return IDENTIDADE_HYPE
    if re.search(r"\b(pegs|coreerp|demo)\b", texto):
        return IDENTIDADE_PEGS_DEMO
    return None


def resolver_identidade_codigo(
    codigo: str | None,
    *,
    nome: str | None = None,
    email: str | None = None,
    padrao: str | None = None,
) -> str | None:
    explicita = normalizar_identidade_codigo(codigo)
    if codigo and not explicita:
        return None
    return explicita or inferir_identidade_codigo(nome, email) or normalizar_identidade_codigo(padrao)
