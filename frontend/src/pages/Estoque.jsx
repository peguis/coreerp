import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    PackagePlus,
    Search
} from "lucide-react";


import {
    listarMovimentos
} from "../services/estoqueService";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import DataTable from "../components/ui/DataTable";
import EmptyState from "../components/ui/EmptyState";
import SearchInput from "../components/forms/SearchInput";

import {

    formatDate

} from "../utils/date";


import Badge from "../components/Badge";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";


import "./Estoque.css";





function Estoque() {


    const [movimentos, setMovimentos] = useState([]);


    const [carregando, setCarregando] =
        useState(true);



    const [erro, setErro] =
        useState("");



    const [busca, setBusca] =
        useState("");



    const [tipoFiltro, setTipoFiltro] =
        useState("todos");







    useEffect(() => {


        carregar();


    }, []);







    async function carregar() {


        try {


            setCarregando(true);

            setErro("");



            const dados =
                await listarMovimentos();



            setMovimentos(

                Array.isArray(dados)

                    ? dados

                    : []

            );



        } catch {


            setErro(

                "Não foi possível carregar movimentos de estoque."

            );


        } finally {


            setCarregando(false);


        }


    }









   











    const movimentosFiltrados = movimentos


        .filter(movimento => {


            const texto =

                busca.toLowerCase();



            return (

                movimento.produto?.nome

                    ?.toLowerCase()

                    .includes(texto)



                ||

                movimento.observacao

                    ?.toLowerCase()

                    .includes(texto)



                ||

                movimento.tipo

                    ?.toLowerCase()

                    .includes(texto)


            );


        })



        .filter(movimento => {



            if (tipoFiltro === "todos") {

                return true;

            }



            return (

                movimento.tipo ===

                tipoFiltro

            );


        })



        .sort((a, b) =>


            new Date(b.created_at)

            -

            new Date(a.created_at)


        );









    const columns = [



        {


            key: "produto_id",

            title: "Produto",


            render: (_, movimento) => (


                movimento.produto?.nome

                ||

                `Produto #${movimento.produto_id}`


            )


        },







        {


            key: "tipo",

            title: "Tipo",


            render: (valor) => {



                const config = {



                    ENTRADA: {

                        tipo: "success",

                        texto: "Entrada"

                    },


                    SAIDA: {

                        tipo: "danger",

                        texto: "Saída"

                    },


                    AJUSTE: {

                        tipo: "warning",

                        texto: "Ajuste"

                    }



                };



                const badge =

                    config[valor]

                    ||

                    {

                        tipo: "default",

                        texto: valor || "-"

                    };





                return (



                    <Badge

                        tipo={badge.tipo}

                    >

                        {badge.texto}


                    </Badge>



                );


            }


        },







        {


            key: "quantidade",

            title: "Quantidade"


        },






        {


            key: "observacao",

            title: "Observação",


            render: (valor) =>

                valor || "-"


        },






        {
            key: "created_at",
            title: "Data",
            render: (valor) =>
                formatDate(valor)
        }





    ];









    return (



        <main className="estoque-page">





            <PageHeader


                titulo="Estoque"


                subtitulo="Gerencie entradas, saídas e ajustes"


            >



                <Link

                    to="/estoque/novo"

                >



                    <Button

                        variant="primary"

                    >



                        <PackagePlus size={18} />



                        Nova Movimentação



                    </Button>



                </Link>



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





                <div className="estoque-filtros">



                    <SearchInput

                        value={busca}

                        onChange={(e) =>

                            setBusca(e.target.value)

                        }

                        placeholder="Buscar movimentação..."

                    />









                    <select


                        value={tipoFiltro}


                        onChange={(e) =>

                            setTipoFiltro(

                                e.target.value

                            )

                        }


                    >



                        <option value="todos">

                            Todos tipos

                        </option>



                        <option value="ENTRADA">

                            Entradas

                        </option>



                        <option value="SAIDA">

                            Saídas

                        </option>



                        <option value="AJUSTE">

                            Ajustes

                        </option>



                    </select>





                </div>









                {


                    carregando ? (



                        <Loading

                            texto="Carregando estoque..."

                        />



                    ) : movimentosFiltrados.length === 0 ? (



                        <EmptyState


                            titulo="Nenhuma movimentação encontrada"


                            descricao="Registre uma entrada ou saída de estoque."


                            icone="📦"


                        />



                    ) : (



                        <DataTable


                            columns={columns}


                            data={movimentosFiltrados}


                        />


                    )


                }






            </SectionCard>






        </main>


    );


}



export default Estoque;