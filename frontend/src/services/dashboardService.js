import api from "../services/api";

export async function obterDashboard() {

    const response = await api.get("/dashboard/");

    return response.data;

}


export async function obterDashboardPiloto(params = {}) {

    const response = await api.get("/dashboard/piloto", { params });
    return response.data;

}


export async function obterDashboardProfissional(params = {}) {

    const response = await api.get("/dashboard/profissional/me", { params });
    return response.data;

}
