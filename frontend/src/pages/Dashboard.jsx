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

        try {

            const resposta = await obterDashboard();

            setDados(resposta);

        } catch (erro) {

            console.log(
                "Erro dashboard:",
                erro.response?.data
            );

        }

    }



    if (!dados) {

        return (
            <h1>
                Carregando...
            </h1>
        );

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
            valor:
                `R$ ${Number(dados.faturamento).toFixed(2)}`
        }

    ];




    return (


        <main>


            <h1>
                Dashboard
            </h1>




            <div

                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(200px,1fr))",
                    gap: 20,
                    marginTop: 30
                }}

            >


                {
                    cards.map(card => (


                        <div

                            key={card.titulo}

                            style={{
                                padding: 25,
                                borderRadius: 10,
                                background: "#f8fafc",
                                boxShadow:
                                    "0 2px 8px rgba(0,0,0,0.1)"
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





            <br />


            <hr />





            <h2>
                Produtos com estoque baixo
            </h2>



            {
                dados.produtos_baixo_estoque.length === 0


                    ?


                    <p>
                        Nenhum produto com estoque baixo.
                    </p>


                    :


                    <table

                        border="1"

                        cellPadding="10"

                        style={{
                            width: "100%",
                            borderCollapse: "collapse"
                        }}

                    >


                        <thead>

                            <tr>

                                <th>
                                    Produto
                                </th>

                                <th>
                                    Estoque atual
                                </th>

                                <th>
                                    Estoque mínimo
                                </th>

                            </tr>


                        </thead>



                        <tbody>


                            {
                                dados.produtos_baixo_estoque.map(produto => (


                                    <tr key={produto.id}>


                                        <td>
                                            {produto.nome}
                                        </td>


                                        <td>
                                            {produto.estoque}
                                        </td>


                                        <td>
                                            {produto.minimo}
                                        </td>


                                    </tr>


                                ))
                            }


                        </tbody>


                    </table>

            }





            <br />


            <hr />





            <h2>
                Últimas vendas
            </h2>




            {
                dados.ultimas_vendas.length === 0


                    ?


                    <p>
                        Nenhuma venda registrada.
                    </p>


                    :



                    <table

                        border="1"

                        cellPadding="10"

                        style={{
                            width: "100%",
                            borderCollapse: "collapse"
                        }}

                    >


                        <thead>

                            <tr>

                                <th>
                                    ID
                                </th>


                                <th>
                                    Total
                                </th>


                                <th>
                                    Status
                                </th>


                            </tr>


                        </thead>



                        <tbody>


                            {
                                dados.ultimas_vendas.map(venda => (


                                    <tr key={venda.id}>


                                        <td>
                                            #{venda.id}
                                        </td>


                                        <td>
                                            R$ {Number(venda.total).toFixed(2)}
                                        </td>


                                        <td>
                                            {venda.status}
                                        </td>


                                    </tr>


                                ))
                            }


                        </tbody>


                    </table>


            }



        </main>


    );


}


export default Dashboard;