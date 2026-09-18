import api from "../services/api";


export async function listarAgendamentos(params = {}) {
    const response = await api.get("/agendamentos/", { params });
    return response.data;
}


export async function criarAgendamento(dados) {
    const response = await api.post("/agendamentos/", dados);
    return response.data;
}


export async function atualizarAgendamento(id, dados) {
    const response = await api.patch(`/agendamentos/${id}`, dados);
    return response.data;
}


export async function listarRecursosAgenda(params = {}) {
    const response = await api.get("/recursos-agenda/", { params });
    return response.data;
}


export async function criarRecursoAgenda(dados) {
    const response = await api.post("/recursos-agenda/", dados);
    return response.data;
}


export async function atualizarRecursoAgenda(id, dados) {
    const response = await api.put(`/recursos-agenda/${id}`, dados);
    return response.data;
}


export async function desativarRecursoAgenda(id) {
    const response = await api.delete(`/recursos-agenda/${id}`);
    return response.data;
}
