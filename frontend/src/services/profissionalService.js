import api from "../services/api";


export async function listarProfissionais(params = {}) {

    const response = await api.get(
        "/profissionais/",
        { params }
    );

    return response.data;

}


export async function criarProfissional(dados) {

    const response = await api.post("/profissionais/", dados);
    return response.data;

}


export async function atualizarProfissional(id, dados) {

    const response = await api.put(`/profissionais/${id}`, dados);
    return response.data;

}


export async function desativarProfissional(id) {

    const response = await api.delete(`/profissionais/${id}`);
    return response.data;

}
