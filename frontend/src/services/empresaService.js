import api from "./api";


export async function buscarEmpresaAtual() {
    const resposta = await api.get("/empresas/me");
    return resposta.data;
}


export async function buscarIdentidadeEmpresaAtual() {
    const resposta = await api.get("/empresas/me/identidade");
    return resposta.data;
}


export async function atualizarConfiguracaoEmpresa(dados) {
    const resposta = await api.put("/empresas/me/configuracao", dados);
    return resposta.data;
}

export async function buscarOnboardingEmpresa() {
    const resposta = await api.get("/empresas/me/onboarding");
    return resposta.data;
}
