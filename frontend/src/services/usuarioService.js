import api from "../api/axios";


export async function buscarUsuarioLogado() {

    const resposta = await api.get(
        "/usuarios/me"
    );

    return resposta.data;

}