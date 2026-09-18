import api from "../services/api";


export async function listarServicos(params = {}) {

    const response = await api.get(
        "/servicos/",
        { params }
    );

    return response.data;

}


export async function criarServico(dados) {

    const response = await api.post("/servicos/", dados);
    return response.data;

}


export async function atualizarServico(id, dados) {

    const response = await api.put(`/servicos/${id}`, dados);
    return response.data;

}


export async function desativarServico(id) {

    const response = await api.delete(`/servicos/${id}`);
    return response.data;

}


export async function excluirServico(id) {

    const response = await api.delete(`/servicos/${id}/permanente`);
    return response.data;

}
