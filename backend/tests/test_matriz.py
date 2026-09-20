def criar_headers_pegs_admin(client, auth_headers):
    criado = client.post(
        "/usuarios/",
        headers=auth_headers,
        json={
            "nome": "Administrador da Matriz",
            "email": "matriz@pegs.coreerp.com",
            "senha": "senha-matriz-forte",
            "empresa_id": 1,
            "perfil": "pegs_admin",
        },
    )
    assert criado.status_code == 200, criado.text
    login = client.post(
        "/usuarios/login",
        data={
            "username": "matriz@pegs.coreerp.com",
            "password": "senha-matriz-forte",
        },
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_matriz_e_restrita_ao_pegs_admin(client, auth_headers):
    negado = client.get("/matriz/dashboard", headers=auth_headers)
    assert negado.status_code == 403

    pegs_headers = criar_headers_pegs_admin(client, auth_headers)
    dashboard = client.get("/matriz/dashboard", headers=pegs_headers)
    assert dashboard.status_code == 200, dashboard.text
    assert dashboard.json()["total_empresas"] == 1


def test_matriz_provisiona_lista_configura_modulo_e_audita(client, auth_headers):
    pegs_headers = criar_headers_pegs_admin(client, auth_headers)
    provisionamento = client.post(
        "/empresas/provisionar",
        headers=pegs_headers,
        json={
            "nome": "Studio Matriz Demo",
            "cnpj": "11111111000199",
            "email": "contato@studio-matriz-demo.com",
            "administrador_nome": "Admin Studio Demo",
            "administrador_email": "admin@studio-matriz-demo.com",
            "administrador_senha": "senha-studio-forte",
            "tipo_negocio": "STUDIO",
            "modulos_iniciais": ["dashboard", "agenda"],
        },
    )
    assert provisionamento.status_code == 200, provisionamento.text
    empresa_id = provisionamento.json()["id"]

    empresas = client.get("/matriz/empresas", headers=pegs_headers)
    assert empresas.status_code == 200
    criada = next(item for item in empresas.json() if item["id"] == empresa_id)
    assert criada["modulos_ativos"] == 2
    assert criada["administrador_principal"]["email"] == "admin@studio-matriz-demo.com"

    detalhe = client.get(f"/matriz/empresas/{empresa_id}", headers=pegs_headers)
    assert detalhe.status_code == 200
    assert {item["codigo"] for item in detalhe.json()["modulos"]} >= {"dashboard", "agenda"}

    identidade = client.patch(
        f"/matriz/empresas/{empresa_id}/identidade",
        headers=pegs_headers,
        json={
            "nome_exibicao": "Studio Demo",
            "tipo_negocio": "SALAO",
            "cor_primaria": "#6F8CFF",
            "ativo": False,
        },
    )
    assert identidade.status_code == 200, identidade.text
    assert identidade.json()["nome"] == "Studio Demo"
    assert identidade.json()["ativo"] is False

    modulo = client.patch(
        f"/matriz/empresas/{empresa_id}/modulos/agenda",
        headers=pegs_headers,
        json={"ativo": False},
    )
    assert modulo.status_code == 200, modulo.text
    assert modulo.json()["ativo"] is False

    auditoria = client.get("/matriz/auditoria", headers=pegs_headers)
    assert auditoria.status_code == 200
    acoes = {item["acao"] for item in auditoria.json() if item["empresa_id"] == empresa_id}
    assert {"PROVISIONAR_EMPRESA", "ATUALIZAR_IDENTIDADE", "DESATIVAR_MODULO"}.issubset(acoes)
    assert all(item["usuario_nome"] == "Administrador da Matriz" for item in auditoria.json() if item["empresa_id"] == empresa_id)
