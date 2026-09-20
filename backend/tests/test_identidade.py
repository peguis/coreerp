from app.core.identidade import (
    IDENTIDADE_HYPE,
    IDENTIDADE_PEGS_DEMO,
    inferir_identidade_codigo,
    normalizar_identidade_codigo,
    resolver_identidade_codigo,
)


def test_normaliza_aliases_de_identidade_sem_confundir_tenants():
    assert normalizar_identidade_codigo("hype-studio") == IDENTIDADE_HYPE
    assert normalizar_identidade_codigo("coreerp") == IDENTIDADE_PEGS_DEMO
    assert normalizar_identidade_codigo("tenant-desconhecido") is None


def test_inferencia_prioriza_a_marca_explicita_do_tenant():
    assert inferir_identidade_codigo("HYPE STUDIO", "contato@hype.com") == IDENTIDADE_HYPE
    assert inferir_identidade_codigo("Pegs Demo", "demo@pegs.com") == IDENTIDADE_PEGS_DEMO
    assert inferir_identidade_codigo("Empresa Nova", "contato@empresa.com") is None


def test_codigo_invalido_nao_aplica_fallback_de_outra_marca():
    assert resolver_identidade_codigo("marca-inexistente", padrao=IDENTIDADE_PEGS_DEMO) is None
    assert resolver_identidade_codigo(None, nome="Empresa Nova", email="contato@empresa.com") is None
