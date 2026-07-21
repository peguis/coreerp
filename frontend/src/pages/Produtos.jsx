import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    listarProdutos,
    excluirProduto
} from "../services/produtoService";

import ProdutoModal from "../components/ProdutoModal";


function Produtos() {


    const [produtos, setProdutos] = useState([]);

    const [pesquisa, setPesquisa] = useState("");

    const [ordenacao, setOrdenacao] = useState("nome");

    const [estoqueBaixo, setEstoqueBaixo] = useState(false);

    const [pagina, setPagina] = useState(1);

    const [visualizacao, setVisualizacao] = useState("tabela");

    const [produtoSelecionado, setProdutoSelecionado] = useState(null);


    const produtosPorPagina = 10;



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





    function imagemProduto(produto) {


        if (
            produto.imagens &&
            produto.imagens.length > 0
        ) {


            const principal =
                produto.imagens.find(
                    imagem => imagem.principal
                )
                ||
                produto.imagens[0];


            return `http://127.0.0.1:8000/${principal.caminho}`;

        }


        return null;

    }





    let produtosFiltrados = produtos.filter(produto => {


        const texto =
            pesquisa.toLowerCase();



        const busca =

            produto.nome
                .toLowerCase()
                .includes(texto)

            ||

            (produto.categoria || "")
                .toLowerCase()
                .includes(texto)

            ||

            (produto.marca || "")
                .toLowerCase()
                .includes(texto);



        const estoque =

            estoqueBaixo

                ?

                produto.estoque <= produto.estoque_minimo

                :

                true;



        return busca && estoque;


    });





    produtosFiltrados.sort((a, b) => {


        if (ordenacao === "nome")
            return a.nome.localeCompare(b.nome);


        if (ordenacao === "preco")
            return a.preco - b.preco;


        if (ordenacao === "estoque")
            return a.estoque - b.estoque;


        return 0;

    });





    const totalPaginas = Math.ceil(
        produtosFiltrados.length /
        produtosPorPagina
    );



    const produtosPagina =
        produtosFiltrados.slice(
            (pagina - 1) * produtosPorPagina,
            pagina * produtosPorPagina
        );







    function CardProduto({ produto }) {


        return (

            <div

                onClick={() =>
                    setProdutoSelecionado(produto)
                }

                style={{
                    border: "1px solid #ccc",
                    borderRadius: 10,
                    padding: 20,
                    width: 250,
                    cursor: "pointer"
                }}

            >


                {
                    imagemProduto(produto)

                        ?

                        <img

                            src={imagemProduto(produto)}

                            width="180"

                            height="180"

                            style={{
                                objectFit: "cover",
                                borderRadius: 10
                            }}

                        />

                        :

                        <div>
                            Sem imagem
                        </div>

                }



                <h3>
                    {produto.nome}
                </h3>


                <p>
                    R$ {Number(produto.preco).toFixed(2)}
                </p>


                <p>
                    Estoque: {produto.estoque}
                </p>



                {
                    produto.estoque <= produto.estoque_minimo

                    &&

                    <strong>
                        ⚠ Estoque baixo
                    </strong>

                }



                <br /><br />


                <button
                    onClick={(e) => {

                        e.stopPropagation();

                        remover(produto.id);

                    }}
                >

                    Excluir

                </button>


            </div>

        );

    }






    return (

        <main style={{ padding: 30 }}>


            <h1>
                Produtos
            </h1>



            <input

                placeholder="Pesquisar produto..."

                value={pesquisa}

                onChange={e => {

                    setPesquisa(e.target.value);

                    setPagina(1);

                }}

            />



            <br /><br />




            <select

                value={ordenacao}

                onChange={
                    e => setOrdenacao(e.target.value)
                }

            >

                <option value="nome">
                    Nome
                </option>

                <option value="preco">
                    Preço
                </option>

                <option value="estoque">
                    Estoque
                </option>


            </select>




            <label style={{ marginLeft: 20 }}>


                <input

                    type="checkbox"

                    checked={estoqueBaixo}

                    onChange={
                        e => setEstoqueBaixo(e.target.checked)
                    }

                />


                Estoque baixo


            </label>





            <br /><br />




            <button
                onClick={() => setVisualizacao("tabela")}
            >
                📋 Tabela
            </button>



            <button
                onClick={() => setVisualizacao("cards")}
            >
                🟦 Cards
            </button>



            <br /><br />



            <Link to="/produtos/novo">

                <button>
                    Novo Produto
                </button>

            </Link>




            <br /><br />





            {
                visualizacao === "cards"

                    ?

                    <div

                        style={{
                            display: "flex",
                            gap: 20,
                            flexWrap: "wrap"
                        }}

                    >

                        {
                            produtosPagina.map(produto =>

                                <CardProduto

                                    key={produto.id}

                                    produto={produto}

                                />

                            )
                        }

                    </div>


                    :


                    <table border="1" cellPadding="10">


                        <thead>

                            <tr>

                                <th>
                                    Nome
                                </th>

                                <th>
                                    Preço
                                </th>

                                <th>
                                    Estoque
                                </th>

                                <th>
                                    Ações
                                </th>


                            </tr>


                        </thead>


                        <tbody>


                            {
                                produtosPagina.map(produto => (


                                    <tr key={produto.id}>


                                        <td>
                                            {produto.nome}
                                        </td>


                                        <td>
                                            R$ {Number(produto.preco).toFixed(2)}
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

            }





            <br />


            <button

                disabled={pagina === 1}

                onClick={() => setPagina(pagina - 1)}

            >

                Anterior

            </button>



            Página {pagina} de {totalPaginas || 1}



            <button

                disabled={pagina >= totalPaginas}

                onClick={() => setPagina(pagina + 1)}

            >

                Próxima

            </button>





            <ProdutoModal

                produto={produtoSelecionado}

                fechar={() =>
                    setProdutoSelecionado(null)
                }

            />


        </main>

    );

}


export default Produtos;