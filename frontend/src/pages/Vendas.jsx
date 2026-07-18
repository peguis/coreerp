import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

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


        <main style={{ padding: 30 }}>


            <h1>
                Vendas
            </h1>



            <Link to="/vendas/nova">

                <button>
                    Nova Venda
                </button>

            </Link>



            <br />
            <br />



            {
                vendas.length === 0 ? (

                    <p>
                        Nenhuma venda registrada.
                    </p>

                ) : (


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
                                            R$ {
                                                Number(venda.total)
                                                    .toFixed(2)
                                            }
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


                                            <Link
                                                to={`/vendas/${venda.id}`}
                                            >

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


                )
            }


        </main>


    );


}


export default Vendas;