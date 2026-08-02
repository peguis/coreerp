import api from "../services/api";

export async function obterDashboard() {

    const response = await api.get("/dashboard/");

    return response.data;

}