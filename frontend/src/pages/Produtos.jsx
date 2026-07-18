import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    listarProdutos,
    excluirProduto
} from "../services/produtoService";


function Produtos() {


    const [produtos, setProdutos] = useState([]);



    useEffect(() => {

        carregarProdutos();

    }, []);



    async function carregarProdutos() {

        const dados = await listarProdutos();

        setProdutos(dados);

    }



    async function remover(id) {

        const confirmar = window.confirm(
            "Deseja realmente excluir?"
        );


        if (!confirmar)
            return;



        await excluirProduto(id);


        carregarProdutos();

    }



    return (

        <main style={{ padding: 30 }}>


            <h1>
                Produtos
            </h1>



            <Link to="/produtos/novo">

                <button>
                    Novo Produto
                </button>

            </Link>



            <br />
            <br />



            {
                produtos.length === 0 ? (

                    <p>
                        Nenhum produto cadastrado.
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

                                <th>Nome</th>

                                <th>Preço</th>

                                <th>Estoque</th>

                                <th>Ações</th>

                            </tr>

                        </thead>



                        <tbody>


                            {
                                produtos.map((produto) => (


                                    <tr key={produto.id}>


                                        <td>
                                            {produto.id}
                                        </td>



                                        <td>
                                            {produto.nome}
                                        </td>



                                        <td>
                                            R$ {
                                                Number(produto.preco)
                                                    .toFixed(2)
                                            }
                                        </td>



                                        <td>
                                            {produto.estoque}
                                        </td>



                                        <td>


                                            <Link
                                                to={`/produtos/${produto.id}`}
                                            >

                                                <button>
                                                    Editar
                                                </button>

                                            </Link>



                                            <button
                                                onClick={() => remover(produto.id)}
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


export default Produtos;