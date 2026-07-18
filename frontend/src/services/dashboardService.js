import api from "../api/axios";

export async function obterDashboard() {

    const response = await api.get("/dashboard/");

    return response.data;

}