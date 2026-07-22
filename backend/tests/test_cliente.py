def test_listar_clientes(client, auth_headers):

    response = client.get(
        "/clientes/",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )