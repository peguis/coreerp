import axios from 'axios';

// Instância base do Axios apontando para a sua API FastAPI
const api = axios.create({
    baseURL: "http://localhost:8000"
});

// Request Interceptor: Injeta automaticamente o token JWT salvo no localStorage em todas as requisições
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor: Trata erros de autenticação (401) e expiração de sessão
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('usuario');

            // Se a sessão expirou e o usuário não está na tela de login, redireciona
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }

        // Extrai a mensagem de erro retornada pela FastAPI (detail) ou aplica uma mensagem padrão
        const mensagemErro =
            error.response?.data?.detail ||
            'Ocorreu um erro ao processar sua requisição. Tente novamente.';

        return Promise.reject(new Error(mensagemErro));
    }
);

export default api;