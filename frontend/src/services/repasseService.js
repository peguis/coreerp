import api from "../services/api";


export async function listarPendencias(profissionalId) {

    const response = await api.get("/repasses/pendencias", {
        params: profissionalId
            ? { profissional_id: profissionalId }
            : {}
    });

    return response.data;

}


export async function listarRepasses(params = {}) {

    const response = await api.get("/repasses/", { params });
    return response.data;

}


export async function criarRepasse(dados) {

    const response = await api.post("/repasses/", dados);
    return response.data;

}
