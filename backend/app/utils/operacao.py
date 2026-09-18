def normalizar_texto(valor: str | None) -> str:
    return " ".join((valor or "").strip().upper().split())


def servico_e_tattoo(categoria: str | None, nome: str | None = None) -> bool:
    texto = f"{normalizar_texto(categoria)} {normalizar_texto(nome)}"
    return any(marca in texto for marca in ("TATTOO", "TATOO", "TATUAGEM"))


def servico_compativel_com_area(
    area_atuacao: str | None,
    categoria: str | None,
    nome: str | None = None,
) -> bool:
    area = normalizar_texto(area_atuacao)
    if area == "TATTOO":
        return servico_e_tattoo(categoria, nome)
    if area == "BARBEARIA":
        return not servico_e_tattoo(categoria, nome)
    return True
