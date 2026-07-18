import { useEffect, useState } from "react";
import { Link } from "react-router-dom";


import {
    listarMovimentos
} from "../services/estoqueService";



function Estoque() {


    const [movimentos, setMovimentos] = useState([]);



    useEffect(() => {

        carregar();

    }, []);



    async function carregar() {

        const dados = await listarMovimentos();

        setMovimentos(dados);

    }



    return (

        <>


            <main style={{ padding: 30 }}>


                <h1>
                    Movimentos de Estoque
                </h1>



                <Link to="/estoque/novo">

                    <button>
                        Nova Movimentação
                    </button>

                </Link>



                <br />
                <br />



                <table border="1" cellPadding="10">


                    <thead>

                        <tr>

                            <th>
                                ID
                            </th>

                            <th>
                                Produto
                            </th>

                            <th>
                                Tipo
                            </th>

                            <th>
                                Quantidade
                            </th>

                            <th>
                                Observação
                            </th>

                        </tr>

                    </thead>



                    <tbody>


                        {
                            movimentos.map((movimento) => (


                                <tr key={movimento.id}>


                                    <td>
                                        {movimento.id}
                                    </td>


                                    <td>
                                        {movimento.produto_id}
                                    </td>


                                    <td>
                                        {movimento.tipo}
                                    </td>


                                    <td>
                                        {movimento.quantidade}
                                    </td>


                                    <td>
                                        {movimento.observacao}
                                    </td>


                                </tr>


                            ))
                        }


                    </tbody>


                </table>



            </main>


        </>

    );


}



export default Estoque;