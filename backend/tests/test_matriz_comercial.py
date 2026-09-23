def autenticar(client, email, senha):
    resposta = client.post(
        "/usuarios/login",
        data={"username": email, "password": senha},
    )
    assert resposta.status_code == 200, resposta.text
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


def criar_usuario_matriz(client, headers, *, nome, email, perfil):
    resposta = client.post(
        "/usuarios/",
        headers=headers,
        json={
            "nome": nome,
            "email": email,
            "senha": "senha-forte",
            "empresa_id": 1,
            "perfil": perfil,
        },
    )
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


def test_vendedor_isola_oportunidades_e_cria_demo_com_auditoria(client, auth_headers):
    criar_usuario_matriz(
        client,
        auth_headers,
        nome="Admin da Matriz",
        email="admin.matriz@coreerp.com",
        perfil="pegs_admin",
    )
    vendedor_a = criar_usuario_matriz(
        client,
        auth_headers,
        nome="Vendedor A",
        email="vendedor.a@coreerp.com",
        perfil="vendedor_pegs",
    )
    vendedor_b = criar_usuario_matriz(
        client,
        auth_headers,
        nome="Vendedor B",
        email="vendedor.b@coreerp.com",
        perfil="vendedor_pegs",
    )
    admin_headers = autenticar(client, "admin.matriz@coreerp.com", "senha-forte")
    vendedor_headers = autenticar(client, "vendedor.a@coreerp.com", "senha-forte")
    vendedor_b_headers = autenticar(client, "vendedor.b@coreerp.com", "senha-forte")

    criada = client.post(
        "/matriz/oportunidades",
        headers=vendedor_headers,
        json={
            "nome_negocio_contato": "Studio Aurora",
            "pessoa_responsavel": "Marina",
            "telefone": "85999999999",
            "tipo_negocio": "STUDIO",
            "proxima_acao": "Apresentar a prévia",
            "status": "NOVO",
        },
    )
    assert criada.status_code == 200, criada.text
    oportunidade_id = criada.json()["id"]
    assert criada.json()["vendedor_id"] == vendedor_a["id"]

    criada_b = client.post(
        "/matriz/oportunidades",
        headers=vendedor_b_headers,
        json={"nome_negocio_contato": "Studio Beta", "status": "NOVO"},
    )
    assert criada_b.status_code == 200, criada_b.text
    oportunidade_b_id = criada_b.json()["id"]
    assert criada_b.json()["vendedor_id"] == vendedor_b["id"]

    somente_proprias = client.get("/matriz/oportunidades", headers=vendedor_headers)
    assert somente_proprias.status_code == 200
    assert [item["id"] for item in somente_proprias.json()] == [oportunidade_id]
    somente_b = client.get("/matriz/oportunidades", headers=vendedor_b_headers)
    assert somente_b.status_code == 200
    assert [item["id"] for item in somente_b.json()] == [oportunidade_b_id]
    assert client.get("/matriz/empresas", headers=vendedor_headers).status_code == 403

    demo = client.post(
        "/matriz/demonstracoes",
        headers=vendedor_headers,
        json={
            "nome": "Studio Aurora Demo",
            "cnpj": "22222222000199",
            "email": "contato@aurora-demo.com",
            "administrador_nome": "Marina Aurora",
            "administrador_email": "admin@aurora-demo.com",
            "administrador_senha": "senha-demo-forte",
            "tipo_negocio": "STUDIO",
            "modulos_iniciais": ["dashboard", "agenda"],
            "oportunidade_id": oportunidade_id,
            "template": "tatuagem",
            "dados_apresentacao": True,
            "chave_idempotencia": "demo-idempotency-key-0001",
        },
    )
    assert demo.status_code == 200, demo.text
    empresa_demo_id = demo.json()["id"]
    assert demo.json()["eh_demo"] is True
    repetida_demo = client.post(
        "/matriz/demonstracoes",
        headers=vendedor_headers,
        json={
            "nome": "Studio Aurora Demo",
            "cnpj": "22222222000199",
            "email": "contato@aurora-demo.com",
            "administrador_nome": "Marina Aurora",
            "administrador_email": "admin@aurora-demo.com",
            "administrador_senha": "senha-demo-forte",
            "tipo_negocio": "STUDIO",
            "modulos_iniciais": ["dashboard", "agenda"],
            "oportunidade_id": oportunidade_id,
            "template": "tatuagem",
            "dados_apresentacao": True,
            "chave_idempotencia": "demo-idempotency-key-0001",
        },
    )
    assert repetida_demo.status_code == 200
    assert repetida_demo.json()["id"] == empresa_demo_id
    assert repetida_demo.json()["dados_apresentacao"] is True

    previa = client.get(f"/matriz/demonstracoes/{empresa_demo_id}/previa", headers=vendedor_headers)
    assert previa.status_code == 200
    assert previa.json()["modulos_ativos"] == ["dashboard", "agenda"]

    solicitar = client.post(
        f"/matriz/oportunidades/{oportunidade_id}/solicitar-conversao",
        headers=vendedor_headers,
    )
    assert solicitar.status_code == 200, solicitar.text
    assert solicitar.json()["status"] == "PROPOSTA_ENVIADA"

    aprovado = client.post(
        f"/matriz/oportunidades/{oportunidade_id}/aprovar-conversao",
        headers=admin_headers,
        json={
            "confirmar": True,
            "cnpj": "33333333000199",
            "email": "contato@aurora-real.com",
            "administrador_nome": "Marina Aurora",
            "administrador_email": "admin@aurora-real.com",
            "administrador_senha": "senha-real-forte",
        },
    )
    assert aprovado.status_code == 200, aprovado.text
    assert aprovado.json()["status"] == "CONVERTIDO"
    empresa_real_id = aprovado.json()["tenant_real_id"]
    assert empresa_real_id != empresa_demo_id
    assert aprovado.json()["tenant_demo_eh_demo"] is True

    repetida = client.post(
        f"/matriz/oportunidades/{oportunidade_id}/aprovar-conversao",
        headers=admin_headers,
        json={
            "confirmar": True,
            "cnpj": "33333333000199",
            "email": "contato@aurora-real.com",
            "administrador_nome": "Marina Aurora",
            "administrador_email": "admin@aurora-real.com",
            "administrador_senha": "senha-real-forte",
        },
    )
    assert repetida.status_code == 200
    assert repetida.json()["tenant_real_id"] == empresa_real_id

    arquivada = client.post(f"/matriz/demonstracoes/{empresa_demo_id}/arquivar", headers=admin_headers)
    assert arquivada.status_code == 200
    assert arquivada.json()["arquivada"] is True

    auditoria = client.get("/matriz/auditoria", headers=admin_headers)
    assert auditoria.status_code == 200
    acoes = {item["acao"] for item in auditoria.json()}
    assert {
        "CRIAR_OPORTUNIDADE",
        "CRIAR_DEMONSTRACAO",
        "VINCULAR_DEMONSTRACAO_OPORTUNIDADE",
        "SOLICITAR_CONVERSAO_EMPRESA",
        "CONVERTER_EMPRESA_REAL",
        "APROVAR_CONVERSAO_EMPRESA",
    }.issubset(acoes)


def test_demo_arquivada_bloqueia_solicitacao_e_aprovacao_de_conversao(client, auth_headers):
    criar_usuario_matriz(
        client,
        auth_headers,
        nome="Admin Matriz Arquivamento",
        email="admin.arquivamento@coreerp.com",
        perfil="pegs_admin",
    )
    criar_usuario_matriz(
        client,
        auth_headers,
        nome="Vendedor Arquivamento",
        email="vendedor.arquivamento@coreerp.com",
        perfil="vendedor_pegs",
    )
    admin_headers = autenticar(client, "admin.arquivamento@coreerp.com", "senha-forte")
    vendedor_headers = autenticar(client, "vendedor.arquivamento@coreerp.com", "senha-forte")

    def criar_oportunidade_demo(sufixo):
        oportunidade = client.post(
            "/matriz/oportunidades",
            headers=vendedor_headers,
            json={"nome_negocio_contato": f"Studio Arquivado {sufixo}", "status": "NOVO"},
        )
        assert oportunidade.status_code == 200, oportunidade.text
        oportunidade_id = oportunidade.json()["id"]
        demo = client.post(
            "/matriz/demonstracoes",
            headers=vendedor_headers,
            json={
                "nome": f"Studio Arquivado Demo {sufixo}",
                "cnpj": f"555555550001{str(sufixo).zfill(2)}",
                "email": f"contato.arquivado.{sufixo}@example.com",
                "administrador_nome": "Admin Demo",
                "administrador_email": f"admin.demo.arquivado.{sufixo}@example.com",
                "administrador_senha": "senha-demo-forte",
                "tipo_negocio": "STUDIO",
                "modulos_iniciais": ["dashboard"],
                "oportunidade_id": oportunidade_id,
                "template": "tatuagem",
                "dados_apresentacao": False,
                "chave_idempotencia": f"demo-arquivada-key-{str(sufixo).zfill(8)}",
            },
        )
        assert demo.status_code == 200, demo.text
        return oportunidade_id, demo.json()["id"]

    # Uma solicitação feita antes do arquivamento não pode ser aprovada depois.
    oportunidade_id, demo_id = criar_oportunidade_demo(1)
    solicitada = client.post(
        f"/matriz/oportunidades/{oportunidade_id}/solicitar-conversao",
        headers=vendedor_headers,
    )
    assert solicitada.status_code == 200, solicitada.text
    arquivada = client.post(f"/matriz/demonstracoes/{demo_id}/arquivar", headers=admin_headers)
    assert arquivada.status_code == 200, arquivada.text
    aprovada = client.post(
        f"/matriz/oportunidades/{oportunidade_id}/aprovar-conversao",
        headers=admin_headers,
        json={
            "confirmar": True,
            "cnpj": "66666666000199",
            "email": "contato.real.arquivado@example.com",
            "administrador_nome": "Admin Real",
            "administrador_email": "admin.real.arquivado@example.com",
            "administrador_senha": "senha-real-forte",
        },
    )
    assert aprovada.status_code == 409
    assert "demonstração ativa" in aprovada.json()["detail"]

    # Uma demonstração arquivada antes do pedido também não aceita solicitação.
    oportunidade_nova_id, demo_nova_id = criar_oportunidade_demo(2)
    arquivada_antes = client.post(
        f"/matriz/demonstracoes/{demo_nova_id}/arquivar",
        headers=admin_headers,
    )
    assert arquivada_antes.status_code == 200, arquivada_antes.text
    solicitada_apos_arquivo = client.post(
        f"/matriz/oportunidades/{oportunidade_nova_id}/solicitar-conversao",
        headers=vendedor_headers,
    )
    assert solicitada_apos_arquivo.status_code == 409
    assert "arquivada ou inativa" in solicitada_apos_arquivo.json()["detail"]
