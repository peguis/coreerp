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


def test_empresa_consulta_checklist_de_onboarding(client, auth_headers):
    resposta = client.get("/empresas/me/onboarding", headers=auth_headers)

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["percentual_concluido"] == 60
    assert dados["concluido"] is False
    assert {item["codigo"] for item in dados["itens"]} >= {
        "identidade",
        "administrador",
        "modulos",
        "servicos",
        "profissionais",
    }


def test_provisionamento_fica_restrito_ao_pegs_admin_e_cria_tenant_isolado(
    client,
    auth_headers,
):
    dados = {
        "nome": "Empresa Nova",
        "cnpj": "11111111000199",
        "email": "contato@empresa-nova.com",
        "administrador_nome": "Admin Nova",
        "administrador_email": "admin@empresa-nova.com",
        "administrador_senha": "senha-nova-forte",
        "tipo_negocio": "STUDIO",
    }

    negado = client.post(
        "/empresas/provisionar",
        headers=auth_headers,
        json=dados,
    )
    assert negado.status_code == 403

    pegs_admin = client.post(
        "/usuarios/",
        headers=auth_headers,
        json={
            "nome": "Administrador Pegs",
            "email": "admin@pegs.coreerp.com",
            "senha": "senha-pegs-forte",
            "empresa_id": 1,
            "perfil": "pegs_admin",
        },
    )
    assert pegs_admin.status_code == 200, pegs_admin.text

    login = client.post(
        "/usuarios/login",
        data={
            "username": "admin@pegs.coreerp.com",
            "password": "senha-pegs-forte",
        },
    )
    assert login.status_code == 200
    pegs_headers = {
        "Authorization": f"Bearer {login.json()['access_token']}"
    }

    criado = client.post(
        "/empresas/provisionar",
        headers=pegs_headers,
        json=dados,
    )
    assert criado.status_code == 200
    assert criado.json()["nome"] == "Empresa Nova"
    assert criado.json()["tipo_negocio"] == "STUDIO"
    assert criado.json()["identidade_codigo"] == "pegs-demo"
