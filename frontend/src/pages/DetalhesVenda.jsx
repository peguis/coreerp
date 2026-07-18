import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { buscarVenda } from "../services/vendaService";


function DetalhesVenda() {


    const { id } = useParams();

    const [venda, setVenda] = useState(null);



    useEffect(() => {

        carregar();

    }, []);



    async function carregar() {


        const dados = await buscarVenda(id);

        setVenda(dados);


    }



    if (!venda) {


        return <h1>Carregando...</h1>;


    }



    return (


        <main style={{ padding: 30 }}>


            <h1>
                Detalhes da Venda
            </h1>



            <p>

                <strong>ID:</strong> {venda.id}

            </p>



            <p>

                <strong>Cliente:</strong> {venda.cliente_id}

            </p>



            <p>

                <strong>Total:</strong> R$ {
                    Number(venda.total)
                        .toFixed(2)
                }

            </p>



            <p>

                <strong>Status:</strong> {venda.status}

            </p>



            <p>

                <strong>Data:</strong>{" "}

                {
                    new Date(
                        venda.created_at
                    ).toLocaleString()
                }

            </p>



            <h2>
                Produtos
            </h2>



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
                            Quantidade
                        </th>


                        <th>
                            Preço Unitário
                        </th>


                        <th>
                            Subtotal
                        </th>


                    </tr>


                </thead>



                <tbody>


                    {
                        venda.itens.map((item) => (


                            <tr key={item.id}>


                                <td>

                                    {
                                        item.produto?.nome ||
                                        item.produto_id
                                    }

                                </td>



                                <td>
                                    {item.quantidade}
                                </td>



                                <td>

                                    R$ {
                                        Number(
                                            item.preco_unitario
                                        ).toFixed(2)
                                    }

                                </td>



                                <td>

                                    R$ {
                                        Number(
                                            item.subtotal
                                        ).toFixed(2)
                                    }

                                </td>



                            </tr>


                        ))
                    }


                </tbody>


            </table>



        </main>


    );


}


export default DetalhesVenda;