import api from "./api";

export async function buscarDashboardMatriz() {
    const resposta = await api.get("/matriz/dashboard");
    return resposta.data;
}

export async function listarEmpresasMatriz(filtros = {}) {
    const resposta = await api.get("/matriz/empresas", { params: filtros });
    return resposta.data;
}

export async function buscarDetalheEmpresaMatriz(empresaId) {
    const resposta = await api.get(`/matriz/empresas/${empresaId}`);
    return resposta.data;
}

export async function atualizarIdentidadeEmpresaMatriz(empresaId, dados) {
    const resposta = await api.patch(`/matriz/empresas/${empresaId}/identidade`, dados);
    return resposta.data;
}

export async function atualizarModuloEmpresaMatriz(empresaId, codigo, ativo) {
    const resposta = await api.patch(`/matriz/empresas/${empresaId}/modulos/${codigo}`, { ativo });
    return resposta.data;
}

export async function atualizarUsuarioEmpresaMatriz(empresaId, usuarioId, dados) {
    const resposta = await api.patch(`/matriz/empresas/${empresaId}/usuarios/${usuarioId}`, dados);
    return resposta.data;
}

export async function listarAuditoriaMatriz(filtros = {}) {
    const resposta = await api.get("/matriz/auditoria", { params: filtros });
    return resposta.data;
}

export async function listarCatalogoModulosMatriz() {
    const resposta = await api.get("/matriz/modulos/catalogo");
    return resposta.data;
}

export async function provisionarEmpresaMatriz(dados) {
    const resposta = await api.post("/empresas/provisionar", dados);
    return resposta.data;
}

export async function listarVendedoresMatriz() {
    const resposta = await api.get("/matriz/vendedores");
    return resposta.data;
}

export async function listarUsuariosMatriz() {
    const resposta = await api.get("/matriz/usuarios");
    return resposta.data;
}

export async function atualizarUsuarioMatriz(usuarioId, dados) {
    const resposta = await api.patch(`/matriz/usuarios/${usuarioId}`, dados);
    return resposta.data;
}

export async function listarOportunidadesMatriz(filtros = {}) {
    const resposta = await api.get("/matriz/oportunidades", { params: filtros });
    return resposta.data;
}

export async function criarOportunidadeMatriz(dados) {
    const resposta = await api.post("/matriz/oportunidades", dados);
    return resposta.data;
}

export async function atualizarOportunidadeMatriz(oportunidadeId, dados) {
    const resposta = await api.patch(`/matriz/oportunidades/${oportunidadeId}`, dados);
    return resposta.data;
}

export async function registrarInteracaoMatriz(oportunidadeId, dados) {
    const resposta = await api.post(`/matriz/oportunidades/${oportunidadeId}/interacoes`, dados);
    return resposta.data;
}

export async function criarDemonstracaoMatriz(dados) {
    const resposta = await api.post("/matriz/demonstracoes", dados);
    return resposta.data;
}

export async function obterPreviaDemonstracaoMatriz(empresaId) {
    const resposta = await api.get(`/matriz/demonstracoes/${empresaId}/previa`);
    return resposta.data;
}

export async function solicitarConversaoMatriz(oportunidadeId) {
    const resposta = await api.post(`/matriz/oportunidades/${oportunidadeId}/solicitar-conversao`);
    return resposta.data;
}

export async function aprovarConversaoMatriz(oportunidadeId) {
    const resposta = await api.post(`/matriz/oportunidades/${oportunidadeId}/aprovar-conversao`, { confirmar: true });
    return resposta.data;
}
