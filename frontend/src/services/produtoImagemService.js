import api from "./api";


export async function listarImagens(produto_id) {

    const response = await api.get(
        `/produtos/${produto_id}/imagens`
    );

    return response.data;

}


export async function enviarImagem(produto_id, arquivo) {

    const formData = new FormData();

    formData.append(
        "arquivo",
        arquivo
    );


    const response = await api.post(
        `/produtos/${produto_id}/imagem`,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );


    return response.data;

}



export async function excluirImagem(
    produto_id,
    imagem_id
) {

    const response = await api.delete(
        `/produtos/${produto_id}/imagem/${imagem_id}`
    );


    return response.data;

}