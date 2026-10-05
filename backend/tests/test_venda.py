def test_listar_vendas(client, auth_headers):

    response = client.get(
        "/vendas/",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_pedido_pendente_so_baixa_estoque_ao_ser_concluido(
    client,
    auth_headers
):
    cliente = client.post(
        "/clientes/",
        json={
            "nome": "Cliente do E-commerce",
            "email": "cliente@example.com"
        },
        headers=auth_headers
    )
    assert cliente.status_code == 200

    produto = client.post(
        "/produtos/",
        json={
            "nome": "Produto do E-commerce",
            "preco": 25,
            "estoque": 5,
            "estoque_minimo": 1,
            "estoque_maximo": 10
        },
        headers=auth_headers
    )
    assert produto.status_code == 200

    pedido = client.post(
        "/vendas/",
        json={
            "cliente_id": cliente.json()["id"],
            "itens": [
                {
                    "produto_id": produto.json()["id"],
                    "quantidade": 2
                }
            ],
            "status": "PENDENTE"
        },
        headers=auth_headers
    )
    assert pedido.status_code == 200
    assert pedido.json()["status"] == "PENDENTE"
    assert pedido.json()["estoque_baixado"] is False
    assert client.get(
        f"/produtos/{produto.json()['id']}",
        headers=auth_headers
    ).json()["estoque"] == 5

    concluido = client.put(
        f"/vendas/{pedido.json()['id']}",
        json={"status": "CONCLUIDA"},
        headers=auth_headers
    )
    assert concluido.status_code == 200
    assert concluido.json()["status"] == "CONCLUIDA"
    assert concluido.json()["estoque_baixado"] is True
    assert client.get(
        f"/produtos/{produto.json()['id']}",
        headers=auth_headers
    ).json()["estoque"] == 3

    # A confirmação repetida não pode gerar uma segunda saída.
    repetido = client.put(
        f"/vendas/{pedido.json()['id']}",
        json={"status": "CONCLUIDA"},
        headers=auth_headers
    )
    assert repetido.status_code == 200
    assert client.get(
        f"/produtos/{produto.json()['id']}",
        headers=auth_headers
    ).json()["estoque"] == 3


def test_cancelar_pedido_pendente_nao_altera_estoque(
    client,
    auth_headers
):
    cliente = client.post(
        "/clientes/",
        json={"nome": "Cliente para cancelamento"},
        headers=auth_headers
    )
    produto = client.post(
        "/produtos/",
        json={
            "nome": "Produto cancelado",
            "preco": 10,
            "estoque": 4,
            "estoque_minimo": 1,
            "estoque_maximo": 10
        },
        headers=auth_headers
    )

    pedido = client.post(
        "/vendas/",
        json={
            "cliente_id": cliente.json()["id"],
            "itens": [
                {
                    "produto_id": produto.json()["id"],
                    "quantidade": 1
                }
            ],
            "status": "PENDENTE"
        },
        headers=auth_headers
    )
    assert pedido.status_code == 200

    cancelado = client.put(
        f"/vendas/{pedido.json()['id']}",
        json={"status": "CANCELADA"},
        headers=auth_headers
    )
    assert cancelado.status_code == 200
    assert cancelado.json()["estoque_baixado"] is False
    assert client.get(
        f"/produtos/{produto.json()['id']}",
        headers=auth_headers
    ).json()["estoque"] == 4


def test_integracao_ecommerce_e_idempotente(
    client,
    auth_headers
):
    cliente = client.post(
        "/clientes/",
        json={"nome": "Cliente externo"},
        headers=auth_headers
    )
    produto = client.post(
        "/produtos/",
        json={
            "nome": "Produto externo",
            "preco": 15,
            "estoque": 8,
            "estoque_minimo": 1,
            "estoque_maximo": 10
        },
        headers=auth_headers
    )
    payload = {
        "cliente_id": cliente.json()["id"],
        "itens": [
            {
                "produto_id": produto.json()["id"],
                "quantidade": 1
            }
        ],
        "pedido_externo_id": "ecommerce-order-1001",
        "chave_idempotencia": "ecommerce-key-1001"
    }

    primeira = client.post(
        "/vendas/integracao/ecommerce",
        json=payload,
        headers=auth_headers
    )
    segunda = client.post(
        "/vendas/integracao/ecommerce",
        json=payload,
        headers=auth_headers
    )

    assert primeira.status_code == 200
    assert segunda.status_code == 200
    assert primeira.json()["id"] == segunda.json()["id"]
    assert segunda.json()["status"] == "PENDENTE"
    assert segunda.json()["origem"] == "ECOMMERCE"
    assert segunda.json()["pedido_externo_id"] == "ecommerce-order-1001"
    assert segunda.json()["estoque_baixado"] is False
    assert client.get(
        f"/produtos/{produto.json()['id']}",
        headers=auth_headers
    ).json()["estoque"] == 8
