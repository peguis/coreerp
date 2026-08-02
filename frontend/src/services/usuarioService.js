import api from "../services/api";



export async function buscarUsuarioLogado() {


    const resposta = await api.get(
        "/usuarios/me"
    );


    return resposta.data;


}