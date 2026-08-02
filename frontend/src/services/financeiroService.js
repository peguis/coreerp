import api from "./api";


const financeiroService = {


    async getLancamentos() {

        const response = await api.get(
            "/financeiro/lancamentos"
        );

        return response.data;
    },





    async getLancamentoPorId(id) {

        const response = await api.get(
            `/financeiro/lancamentos/${id}`
        );

        return response.data;
    },





    async criarLancamento(dadosLancamento) {

        const response = await api.post(
            "/financeiro/lancamentos",
            dadosLancamento
        );

        return response.data;
    },





    async atualizarLancamento(
        id,
        dadosLancamento
    ) {

        const response = await api.put(
            `/financeiro/lancamentos/${id}`,
            dadosLancamento
        );

        return response.data;
    },





    async excluirLancamento(id) {

        const response = await api.delete(
            `/financeiro/lancamentos/${id}`
        );

        return response.data;
    },





    async baixarLancamento(id) {

        const response = await api.put(
            `/financeiro/lancamentos/${id}`,
            {
                status: "PAGO"
            }
        );

        return response.data;
    },





    async getResumoFinanceiro() {

        const response = await api.get(
            "/financeiro/resumo"
        );

        return response.data;
    },





    async getDRE() {

        const response = await api.get(
            "/financeiro/dre"
        );

        return response.data;
    },

    async criarCategoria(dados) {

        const response = await api.post(
            "/categorias-financeiras/",
            dados
        );

        return response.data;

    },

    



    async getCategorias() {


        const response = await api.get(

            "/categorias-financeiras/"

        );


        return response.data;


    },




    async criarCategoria(dadosCategoria) {


        const response = await api.post(

            "/categorias-financeiras/",

            dadosCategoria

        );


        return response.data;


    },




    async atualizarCategoria(
        id,
        dadosCategoria
    ) {


        const response = await api.put(

            `/categorias-financeiras/${id}`,

            dadosCategoria

        );


        return response.data;


    },




    async excluirCategoria(id) {


        const response = await api.delete(

            `/categorias-financeiras/${id}`

        );


        return response.data;


    },


};


export default financeiroService;