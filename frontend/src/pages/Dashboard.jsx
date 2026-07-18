import { useEffect, useState } from "react";


import {
    obterDashboard
} from "../services/dashboardService";


function Dashboard() {


    const [dados, setDados] = useState(null);



    useEffect(() => {

        carregar();

    }, []);



    async function carregar() {

        const resposta = await obterDashboard();

        setDados(resposta);

    }



    if (!dados) {

        return <h1>Carregando...</h1>;

    }



    const cards = [

        {
            titulo: "Produtos",
            valor: dados.total_produtos
        },

        {
            titulo: "Clientes",
            valor: dados.total_clientes
        },

        {
            titulo: "Vendas",
            valor: dados.total_vendas
        },

        {
            titulo: "Estoque baixo",
            valor: dados.estoque_baixo
        },

        {
            titulo: "Faturamento",
            valor: `R$ ${dados.faturamento}`
        }

    ];



    return (


        <div>


            <h1>
                Dashboard
            </h1>



            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                    gap: "20px",
                    marginTop: "30px"
                }}
            >


                {
                    cards.map((card) => (


                        <div
                            key={card.titulo}
                            style={{
                                padding: "25px",
                                borderRadius: "10px",
                                background: "#f8fafc",
                                boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
                            }}
                        >


                            <h3>
                                {card.titulo}
                            </h3>



                            <h1>
                                {card.valor}
                            </h1>


                        </div>


                    ))
                }


            </div>


        </div>


    );


}


export default Dashboard;