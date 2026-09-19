def test_empresa_lista_modulos_e_bloqueia_endpoint_desativado(client, auth_headers):
    resposta = client.get("/modulos/", headers=auth_headers)
    assert resposta.status_code == 200
    assert {item["codigo"] for item in resposta.json()} >= {"agenda", "dashboard"}

    agenda = next(item for item in resposta.json() if item["codigo"] == "agenda")
    assert agenda["ativo"] is True

    desativacao = client.patch(
        "/modulos/agenda",
        headers=auth_headers,
        json={"ativo": False},
    )
    assert desativacao.status_code == 200
    assert desativacao.json()["ativo"] is False

    bloqueado = client.get("/agendamentos/", headers=auth_headers)
    assert bloqueado.status_code == 403


def test_modulo_desativado_pode_ser_reativado(client, auth_headers):
    desativacao = client.patch(
        "/modulos/clientes",
        headers=auth_headers,
        json={"ativo": False},
    )
    assert desativacao.status_code == 200

    reativacao = client.patch(
        "/modulos/clientes",
        headers=auth_headers,
        json={"ativo": True},
    )
    assert reativacao.status_code == 200
    assert reativacao.json()["ativo"] is True


def test_empresa_atualiza_configuracao_sem_alterar_dados_operacionais(
    client,
    auth_headers,
):
    resposta = client.put(
        "/empresas/me/configuracao",
        headers=auth_headers,
        json={
            "nome_exibicao": "Empresa Demo",
            "cor_primaria": "#D9AB3F",
            "tema": "dark",
            "tipo_negocio": "servicos",
        },
    )
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Empresa Demo"
    assert resposta.json()["cor_primaria"] == "#D9AB3F"

    consulta = client.get("/empresas/me", headers=auth_headers)
    assert consulta.status_code == 200
    assert consulta.json()["tipo_negocio"] == "servicos"
