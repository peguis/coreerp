def normalizar_tipo_recurso(valor: str | None) -> str:
    return " ".join((valor or "").strip().upper().split())


def tipos_recurso_compativeis(tipo_recurso: str | None, tipo_servico: str | None) -> bool:
    recurso = normalizar_tipo_recurso(tipo_recurso)
    servico = normalizar_tipo_recurso(tipo_servico)
    if not recurso or not servico:
        return False
    return (
        recurso == servico
        or recurso.startswith(f"{servico} ")
        or servico.startswith(f"{recurso} ")
    )
