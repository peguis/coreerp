import api from "../api/axios";


export async function listarVendas() {

    const response = await api.get("/vendas/");

    return response.data;

}


export async function criarVenda(dados) {

    const response = await api.post(
        "/vendas/",
        dados
    );

    return response.data;

}


export async function buscarVenda(id) {

    const response = await api.get(
        `/vendas/${id}`
    );

    return response.data;

}


export async function excluirVenda(id) {

    await api.delete(
        `/vendas/${id}`
    );

}