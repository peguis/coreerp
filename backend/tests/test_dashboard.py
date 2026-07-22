def test_dashboard(client, auth_headers):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    dados = response.json()

    assert "total_produtos" in dados
    assert "total_clientes" in dados
    assert "total_vendas" in dados