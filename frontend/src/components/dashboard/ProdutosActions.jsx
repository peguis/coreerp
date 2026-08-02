import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    listarProdutos,
    excluirProduto
} from "../services/produtoService";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";

import ProdutosActions from "../components/dashboard/ProdutosActions";

import DataTable from "../ui/DataTable";
import Badge from "../Badge";
import Button from "../components/forms/Button";

import {

    confirmDelete

} from "../utils/dialog";

import Loading from "../components/Loading";
import EmptyState from "../components/EmptyState";
import Mensagem from "../components/Mensagem";
import Checkbox from "../components/forms/Checkbox";

import {
    Pencil,
    Trash2
} from "lucide-react";


import "./Produtos.css";



function Produtos() {


    const [produtos, setProdutos] = useState([]);

    const [pesquisa, setPesquisa] = useState("");

    const [ordenacao, setOrdenacao] = useState("nome");

    const [estoqueBaixo, setEstoqueBaixo] = useState(false);

    const [pagina, setPagina] = useState(1);


    const [carregando, setCarregando] = useState(true);

    const [erro, setErro] = useState("");



    const produtosPorPagina = 10;




    useEffect(() => {

        carregarProdutos();

    }, []);





    async function carregarProdutos() {


        try {


            setCarregando(true);

            setErro("");

            const dados = await listarProdutos();

            setProdutos(dados);


        } catch {


            setErro(
                "Não foi possível carregar produtos."
            );


        } finally {


            setCarregando(false);


        }


    }





    async function remover(id) {


        const confirmar =

            confirmDelete(

                "Deseja excluir?"

        );


        if (!confirmar)
            return;



        await excluirProduto(id);


        carregarProdutos();


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

            (produto.codigo_interno || "")
                .toLowerCase()
                .includes(texto)

            ||

            (produto.codigo_barras || "")
                .toLowerCase()
                .includes(texto)

            ||

            (produto.marca || "")
                .toLowerCase()
                .includes(texto);



        const estoque = estoqueBaixo

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








    const columns = [



        {


            key: "nome",

            title: "Produto"


        },



        {


            key: "categoria",

            title: "Categoria"


        },



        {


            key: "estoque",

            title: "Estoque"


        },



        {


            key: "preco",

            title: "Preço",


            render: (valor) =>

                formatarMoeda(valor)


        },




        {


            key: "ativo",

            title: "Status",


            render: (valor) => (


                <Badge

                    tipo={
                        valor
                            ?
                            "success"
                            :
                            "danger"
                    }

                >

                    {
                        valor
                            ?
                            "Ativo"
                            :
                            "Inativo"
                    }


                </Badge>


            )


        },




        {


            key: "acoes",

            title: "Ações",


            render: (_, produto) => (


                <div className="table-actions">



                    <Link

                        to={`/produtos/${produto.id}`}

                    >

                        <Button>


                            <Pencil size={16} />


                        </Button>


                    </Link>





                    <Button

                        variant="danger"

                        onClick={() => remover(produto.id)}

                    >


                        <Trash2 size={16} />


                    </Button>



                </div>


            )


        }



    ];







    return (



        <main className="produtos-page">



            <PageHeader


                titulo="Produtos"


                descricao="Gerencie os produtos cadastrados."


            />






            <ProdutosActions


                pesquisa={pesquisa}

                setPesquisa={setPesquisa}


            />







            <SectionCard>




                <div className="produtos-filtros">



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





                    <Checkbox

                        label="Estoque baixo"

                        checked={estoqueBaixo}

                        onChange={(e) =>

                            setEstoqueBaixo(e.target.checked)

                        }

                    />



                </div>








                {
                    carregando &&

                    <Loading />

                }







                {
                    erro &&

                    <Mensagem

                        tipo="erro"

                        texto={erro}

                    />

                }








                {
                    !carregando &&

                    produtosPagina.length === 0 &&


                    <EmptyState


                        titulo="Nenhum produto cadastrado"


                        descricao="Cadastre seu primeiro produto."


                        icone="📦"


                    />


                }








                {

                    !carregando &&

                    produtosPagina.length > 0 &&



                    <DataTable


                        columns={columns}


                        data={produtosPagina}


                        emptyMessage="Nenhum produto encontrado."


                    />


                }








                <div className="pagination">



                    <Button

                        disabled={pagina === 1}

                        onClick={() => setPagina(pagina - 1)}

                    >

                        Anterior

                    </Button>




                    <span>

                        Página {pagina} de {totalPaginas || 1}

                    </span>




                    <Button

                        disabled={
                            pagina >= totalPaginas
                        }

                        onClick={() => setPagina(pagina + 1)}

                    >

                        Próxima

                    </Button>



                </div>




            </SectionCard>




        </main>



    );


}


export default Produtos;