def test_login(client):

    response = client.post(
        "/usuarios/login",
        data={
            "username": "admin@coreerp.com",
            "password": "123456"
        }
    )


    assert response.status_code == 200


    dados = response.json()


    assert "access_token" in dados
    assert "token_type" in dados