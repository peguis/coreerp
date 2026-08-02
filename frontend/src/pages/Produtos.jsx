import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import {
    Pencil,
    Trash2,
    PackagePlus,
    LayoutGrid,
    List
} from "lucide-react";

import {

    confirmDelete

} from "../utils/dialog";


import {
    listarProdutos,
    excluirProduto
} from "../services/produtoService";

import {
    formatarMoeda
} from "../utils/formatters";


import Checkbox from "../components/forms/Checkbox";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import DataTable from "../components/ui/DataTable";
import EmptyState from "../components/ui/EmptyState";


import Badge from "../components/Badge";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";


import "./Produtos.css";



const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000";





function Produtos() {


    const location = useLocation();



    const [produtos, setProdutos] = useState([]);


    const [carregando, setCarregando] = useState(true);


    const [erro, setErro] = useState("");



    const [pesquisa, setPesquisa] = useState("");



    const [categoriaFiltro, setCategoriaFiltro] =
        useState("");



    const [marcaFiltro, setMarcaFiltro] =
        useState("");



    const [statusFiltro, setStatusFiltro] =
        useState("todos");



    const [estoqueBaixo, setEstoqueBaixo] =
        useState(false);



    const [ordenacao, setOrdenacao] =
        useState("nome");



    const [modoVisualizacao, setModoVisualizacao] =
        useState("lista");









    useEffect(() => {


        carregarProdutos();


    }, [location.pathname]);









    async function carregarProdutos() {


        try {


            setCarregando(true);

            setErro("");



            const dados = await listarProdutos();

            console.log(dados);

            setProdutos(
                Array.isArray(dados)
                    ? dados
                    : []
            );



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



        if (!confirmar) {

            return;

        }






        try {



            await excluirProduto(id);



            carregarProdutos();




        } catch (error) {

            setErro(

                getErrorMessage(

                    error,

                    "Erro ao excluir."

                )

            );

        }


    }









    const categorias = [

        ...new Set(

            produtos

                .map(produto => produto.categoria)

                .filter(Boolean)

        )

    ];







    const marcas = [

        ...new Set(

            produtos

                .map(produto => produto.marca)

                .filter(Boolean)

        )

    ];











    const columns = [



        {

            key: "nome",

            title: "Produto",



            render: (_, produto) => (


                <div className="produto-info">


                    {

                        produto.imagens?.length > 0 ? (



                            <img
                                className="produto-miniatura"
                                src={
                                    produto.imagens[0].caminho.startsWith("http")
                                        ? produto.imagens[0].caminho
                                        : `${API_URL}${produto.imagens[0].caminho.startsWith("/") ? "" : "/"}${produto.imagens[0].caminho}`
                                }
                                alt={produto.nome}
                                onError={(e) => {
                                    e.currentTarget.src = "/placeholder.png";
                                }}
                            />



                        ) : (



                            <div className="produto-miniatura-vazia">

                                📦

                            </div>



                        )


                    }



                    <span>

                        {produto.nome}

                    </span>



                </div>


            )


        },




        {

            key: "codigo_interno",

            title: "Código",


            render: (valor) =>

                valor || "-"


        },




        {

            key: "categoria",

            title: "Categoria",


            render: (valor) =>

                valor || "-"


        },




        {

            key: "localizacao",

            title: "Localização",


            render: (valor) =>

                valor || "-"


        },




        {

            key: "estoque",

            title: "Estoque",


            render: (valor, produto) => (



                <span>


                    {valor ?? 0}



                    {


                        Number(valor) <=

                        Number(produto.estoque_minimo)

                        &&

                        " ⚠️"


                    }


                </span>


            )


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

                        to={`/produtos/${produto.id}/editar`}

                    >



                        <Button

                            variant="secondary"

                        >

                            <Pencil size={16} />

                        </Button>



                    </Link>





                    <Button

                        variant="danger"

                        onClick={() =>

                            remover(produto.id)

                        }

                    >


                        <Trash2 size={16} />


                    </Button>



                </div>


            )


        }


    ];









    const produtosFiltrados = produtos


        .filter(produto => {



            const texto =

                pesquisa.toLowerCase();




            const busca =



                produto.nome

                    ?.toLowerCase()

                    .includes(texto)



                ||



                produto.categoria

                    ?.toLowerCase()

                    .includes(texto)



                ||



                produto.marca

                    ?.toLowerCase()

                    .includes(texto)



                ||



                produto.codigo_interno

                    ?.toLowerCase()

                    .includes(texto);



            return busca;



        })



        .filter(produto => {



            if (!categoriaFiltro)

                return true;



            return (

                produto.categoria ===

                categoriaFiltro

            );


        })



        .filter(produto => {



            if (!marcaFiltro)

                return true;



            return (

                produto.marca ===

                marcaFiltro

            );


        })



        .filter(produto => {



            if (statusFiltro === "todos")

                return true;



            if (statusFiltro === "ativo")

                return produto.ativo;



            return !produto.ativo;



        })



        .filter(produto => {



            if (!estoqueBaixo)

                return true;



            return (

                produto.estoque <=

                produto.estoque_minimo

            );


        })



        .sort((a, b) => {



            if (ordenacao === "nome") {


                return (

                    a.nome || ""

                ).localeCompare(

                    b.nome || ""

                );


            }




            if (ordenacao === "preco") {


                return (

                    Number(a.preco || 0)

                    -

                    Number(b.preco || 0)

                );


            }




            if (ordenacao === "estoque") {


                return (

                    Number(a.estoque || 0)

                    -

                    Number(b.estoque || 0)

                );


            }



            return 0;



        });









    return (



        <main className="produtos-page">



            <PageHeader

                titulo="Produtos"

                subtitulo="Gerencie os produtos cadastrados"

            >



                <div className="produtos-header-actions">



                    <Button

                        variant={

                            modoVisualizacao === "lista"

                                ?

                                "primary"

                                :

                                "secondary"

                        }


                        onClick={() =>

                            setModoVisualizacao("lista")

                        }

                    >

                        <List size={18} />

                    </Button>





                    <Button

                        variant={

                            modoVisualizacao === "cards"

                                ?

                                "primary"

                                :

                                "secondary"

                        }


                        onClick={() =>

                            setModoVisualizacao("cards")

                        }

                    >

                        <LayoutGrid size={18} />

                    </Button>





                    <Link

                        to="/produtos/novo"

                    >


                        <Button

                            variant="primary"

                        >

                            <PackagePlus size={18} />


                            Novo Produto


                        </Button>


                    </Link>



                </div>



            </PageHeader>









            {

                erro && (


                    <Mensagem

                        tipo="erro"

                        texto={erro}

                    />


                )


            }








            <SectionCard>





                <div className="produtos-filtros">



                    <input


                        placeholder="Buscar produto..."


                        value={pesquisa}


                        onChange={(e) =>

                            setPesquisa(

                                e.target.value

                            )

                        }


                    />





                    <select

                        value={categoriaFiltro}

                        onChange={(e) =>

                            setCategoriaFiltro(

                                e.target.value

                            )

                        }

                    >


                        <option value="">

                            Todas categorias

                        </option>


                        {

                            categorias.map(categoria => (


                                <option

                                    key={categoria}

                                    value={categoria}

                                >

                                    {categoria}


                                </option>


                            ))

                        }


                    </select>








                    <select

                        value={marcaFiltro}

                        onChange={(e) =>

                            setMarcaFiltro(

                                e.target.value

                            )

                        }

                    >


                        <option value="">


                            Todas marcas


                        </option>


                        {


                            marcas.map(marca => (


                                <option

                                    key={marca}

                                    value={marca}

                                >


                                    {marca}


                                </option>


                            ))

                        }


                    </select>








                    <select

                        value={statusFiltro}

                        onChange={(e) =>

                            setStatusFiltro(

                                e.target.value

                            )

                        }

                    >


                        <option value="todos">

                            Todos

                        </option>


                        <option value="ativo">

                            Ativos

                        </option>


                        <option value="inativo">

                            Inativos

                        </option>


                    </select>








                    <select

                        value={ordenacao}

                        onChange={(e) =>

                            setOrdenacao(

                                e.target.value

                            )

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





                    <Button

                        variant="secondary"

                        onClick={() => {


                            setPesquisa("");

                            setCategoriaFiltro("");

                            setMarcaFiltro("");

                            setStatusFiltro("todos");

                            setEstoqueBaixo(false);


                        }}

                    >


                        Limpar filtros


                    </Button>



                </div>









                {

                    carregando ? (

                        <Loading
                            texto="Carregando produtos..."
                        />

                    ) : produtosFiltrados.length === 0 ? (

                        <EmptyState
                            titulo="Nenhum produto encontrado"
                            descricao="Cadastre um produto ou altere os filtros."
                            icone="📦"
                        />

                    ) : (

                        modoVisualizacao === "lista" ? (

                            <DataTable
                                columns={columns}
                                data={produtosFiltrados}
                            />

                        ) : (

                            <div className="produtos-grid">

                                {produtosFiltrados.map(produto => (

                                    <div
                                        key={produto.id}
                                        className="produto-card"
                                    >

                                        {
                                            produto.imagens?.length > 0 ? (

                                                <img
                                                    className="produto-card-imagem"
                                                    src={
                                                        produto.imagens[0].caminho.startsWith("http")
                                                            ? produto.imagens[0].caminho
                                                            :
                                                            `${API_URL}${produto.imagens[0].caminho.startsWith("/") ? "" : "/"}${produto.imagens[0].caminho}`
                                                    }
                                                    alt={produto.nome}
                                                />

                                            ) : (

                                                <div className="produto-card-imagem-vazia">
                                                    📦
                                                </div>

                                            )
                                        }


                                        <h3>
                                            {produto.nome}
                                        </h3>


                                        <p>
                                            Estoque: {produto.estoque}
                                        </p>


                                        <p>
                                            Preço: {formatarMoeda(produto.preco)}
                                        </p>


                                        <Link
                                            to={`/produtos/${produto.id}/editar`}
                                        >

                                            <Button
                                                variant="secondary"
                                            >
                                                <Pencil size={16} />

                                                Editar

                                            </Button>

                                        </Link>


                                    </div>

                                ))}

                            </div>

                        )

                    )

                }


            </SectionCard>


        </main>


    );


}


export default Produtos;