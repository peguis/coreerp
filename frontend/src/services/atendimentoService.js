import api from "../services/api";


export async function criarAtendimento(dados) {

    const response = await api.post(
        "/atendimentos/",
        dados
    );

    return response.data;

}


export async function listarAtendimentos(params = {}) {

    const response = await api.get(
        "/atendimentos/",
        { params }
    );

    return response.data;

}
