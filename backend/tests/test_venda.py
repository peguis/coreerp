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