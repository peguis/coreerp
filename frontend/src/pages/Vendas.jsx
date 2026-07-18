import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Sidebar from "../components/Sidebar";

import {
    listarVendas,
    excluirVenda
} from "../services/vendaService";


function Vendas() {


    const [vendas, setVendas] = useState([]);



    useEffect(() => {

        carregarVendas();

    }, []);



    async function carregarVendas() {

        const dados = await listarVendas();

        setVendas(dados);

    }



    async function remover(id) {


        const confirmar = window.confirm(
            "Deseja realmente excluir esta venda?"
        );


        if (!confirmar)
            return;


        await excluirVenda(id);


        carregarVendas();

    }



    return (

        <div style={{ display: "flex" }}>


            <Sidebar />


            <main style={{ padding: 30 }}>


                <h1>Vendas</h1>


                <Link to="/vendas/nova">

                    <button>
                        Nova Venda
                    </button>

                </Link>


                <br /><br />



                <table border="1" cellPadding="10">


                    <thead>

                        <tr>

                            <th>ID</th>

                            <th>Cliente</th>

                            <th>Total</th>

                            <th>Status</th>

                            <th>Data</th>

                            <th>Ações</th>

                        </tr>

                    </thead>



                    <tbody>


                        {
                            vendas.map((venda) => (


                                <tr key={venda.id}>


                                    <td>
                                        {venda.id}
                                    </td>


                                    <td>
                                        {venda.cliente_id}
                                    </td>


                                    <td>
                                        R$ {venda.total}
                                    </td>


                                    <td>
                                        {venda.status}
                                    </td>


                                    <td>
                                        {
                                            new Date(
                                                venda.created_at
                                            ).toLocaleDateString()
                                        }
                                    </td>


                                    <td>

                                        <Link to={`/vendas/${venda.id}`}>
                                            <button>
                                                Detalhes
                                            </button>
                                        </Link>


                                        <button
                                            onClick={() => remover(venda.id)}
                                        >

                                            Excluir

                                        </button>


                                    </td>


                                </tr>


                            ))
                        }


                    </tbody>


                </table>


            </main>


        </div>

    );


}


export default Vendas;