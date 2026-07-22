def test_listar_produtos(client, auth_headers):

    response = client.get(
        "/produtos/",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )