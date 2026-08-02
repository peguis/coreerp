import api from "../services/api";


export async function listarMovimentos() {

    const response = await api.get(
        "/movimentos-estoque/"
    );

    return response.data;

}



export async function criarMovimento(dados) {

    const response = await api.post(
        "/movimentos-estoque/",
        dados
    );

    return response.data;

}