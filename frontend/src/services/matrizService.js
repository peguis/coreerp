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
