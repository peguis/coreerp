import api from "../services/api";



export async function buscarUsuarioLogado() {


    const resposta = await api.get(
        "/usuarios/me"
    );


    return resposta.data;


}


export async function listarUsuarios() {

    const resposta = await api.get(
        "/usuarios/"
    );

    return resposta.data;

}


export async function criarUsuario(dados) {

    const resposta = await api.post(
        "/usuarios/",
        dados
    );


    return resposta.data;

}


export async function atualizarUsuario(usuarioId, dados) {

    const resposta = await api.put(
        `/usuarios/${usuarioId}`,
        dados
    );


    return resposta.data;

}
