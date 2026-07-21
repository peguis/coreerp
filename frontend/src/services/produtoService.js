import api from "../api/axios";



export async function listarProdutos() {

    const response = await api.get(
        "/produtos/"
    );

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

    const response = await api.get(
        `/produtos/${id}`
    );

    return response.data;

}





export async function atualizarProduto(
    id,
    produto
) {

    const response = await api.put(
        `/produtos/${id}`,
        produto
    );

    return response.data;

}





export async function excluirProduto(id) {

    const response = await api.delete(
        `/produtos/${id}`
    );

    return response.data;

}





export async function enviarImagemProduto(
    id,
    arquivo
) {


    const formData = new FormData();


    formData.append(
        "arquivo",
        arquivo
    );



    const response = await api.post(

        `/produtos/${id}/imagem`,

        formData,

        {
            headers: {
                "Content-Type":
                    "multipart/form-data"
            }
        }

    );


    return response.data;

}





export async function listarImagensProduto(id) {


    const response = await api.get(
        `/produtos/${id}/imagens`
    );


    return response.data;

}





export async function excluirImagemProduto(
    produtoId,
    imagemId
) {


    const response = await api.delete(

        `/produtos/${produtoId}/imagem/${imagemId}`

    );


    return response.data;

}