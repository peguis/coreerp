import api from "../api/axios";

export async function listarProdutos() {

    const response = await api.get("/produtos/");

    return response.data;

}

export async function criarProduto(produto) {

    const response = await api.post(
        "/produtos/",
        produto
    );

    return response.data;

}

export async function buscarProduto(id) {

    const response = await api.get(`/produtos/${id}`);

    return response.data;

}

export async function atualizarProduto(id, produto) {

    const response = await api.put(
        `/produtos/${id}`,
        produto
    );

    return response.data;

}

export async function excluirProduto(id) {

    await api.delete(`/produtos/${id}`);

}