import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";

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



    return (

        <div style={{ display: "flex" }}>


            <Sidebar />


            <main style={{ padding: 30 }}>


                <h1>
                    Dashboard
                </h1>



                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(3, 200px)",
                    gap: 20
                }}>


                    <div>
                        <h3>
                            Produtos
                        </h3>

                        <h2>
                            {dados.total_produtos}
                        </h2>

                    </div>



                    <div>

                        <h3>
                            Clientes
                        </h3>

                        <h2>
                            {dados.total_clientes}
                        </h2>

                    </div>



                    <div>

                        <h3>
                            Vendas
                        </h3>

                        <h2>
                            {dados.total_vendas}
                        </h2>

                    </div>



                    <div>

                        <h3>
                            Estoque baixo
                        </h3>

                        <h2>
                            {dados.estoque_baixo}
                        </h2>

                    </div>



                    <div>

                        <h3>
                            Faturamento
                        </h3>

                        <h2>
                            R$ {dados.faturamento}
                        </h2>

                    </div>


                </div>


            </main>


        </div>

    );

}


export default Dashboard;