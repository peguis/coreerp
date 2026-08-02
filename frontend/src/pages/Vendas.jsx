import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    ShoppingCart,
    Eye,
    Trash2
} from "lucide-react";

import {

    confirmDelete

} from "../utils/dialog";

import {

    formatDate

} from "../utils/date";


import {
    listarVendas,
    excluirVenda
} from "../services/vendaService";



import {
    formatarMoeda
} from "../utils/formatters";

import {

    badgeStatus

} from "../utils/status";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import DataTable from "../components/ui/DataTable";
import EmptyState from "../components/ui/EmptyState";
import SearchInput from "../components/forms/SearchInput";

import Badge from "../components/Badge";
import Button from "../components/forms/Button";

import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";


import "./Vendas.css";



function Vendas() {


    const [vendas, setVendas] = useState([]);

    const [carregando, setCarregando] = useState(true);

    const [erro, setErro] = useState("");

    const [pesquisa, setPesquisa] = useState("");




    useEffect(() => {

        carregarVendas();

    }, []);




    async function carregarVendas() {


        try {


            setCarregando(true);

            setErro("");



            const dados = await listarVendas();



            setVendas(

                Array.isArray(dados)

                    ? dados

                    : []

            );



        } catch {


            setErro(
                "Não foi possível carregar vendas."
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




        try {


            await excluirVenda(id);


            carregarVendas();



        } catch (error) {

            setErro(

                getErrorMessage(

                    error,

                    "Erro ao excluir."

                )

            );

        }


    }













    







    function definirBadge(status) {


        const mapa = {


            ABERTA: "warning",

            FINALIZADA: "success",

            CANCELADA: "danger"


        };


        return mapa[status] || "default";


    }







    const vendasFiltradas = vendas.filter((venda) => {


        const texto = pesquisa
            .toLowerCase()
            .trim();



        return (


            venda.cliente?.nome
                ?.toLowerCase()
                .includes(texto)



            ||



            venda.status
                ?.toLowerCase()
                .includes(texto)



            ||



            String(venda.id)
                .includes(texto)



        );


    });









    const columns = [



        {

            key: "id",

            title: "Venda"

        },





        {

            key: "cliente",

            title: "Cliente",


            render: (_, venda) => (

                venda.cliente?.nome

                ||

                `Cliente #${venda.cliente_id}`

            )

        },





        {

            key: "total",

            title: "Total",


            render: (valor) => (

                formatarMoeda(valor)

            )

        },





        {

            key: "status",

            title: "Status",


            render: (valor) => (


                <Badge

                    tipo={badgeStatus(valor)}
                >

                    {valor || "SEM STATUS"}

                </Badge>


            )


        },





        {
            key: "created_at",
            title: "Data",

            render: (valor) => (

                formatDate(valor)

            )
        },





        {

            key: "acoes",

            title: "Ações",


            render: (_, venda) => (



                <div className="venda-actions">



                    <Link

                        to={`/vendas/${venda.id}`}

                    >



                        <Button

                            variant="secondary"

                        >


                            <Eye size={16} />


                        </Button>



                    </Link>







                    <Button

                        variant="danger"

                        onClick={() => remover(venda.id)}

                    >



                        <Trash2 size={16} />



                    </Button>



                </div>


            )


        }


    ];









    return (


        <main className="vendas-page">





            <PageHeader

                titulo="Vendas"

                subtitulo="Gerencie as vendas realizadas"

            >



                <div className="vendas-header-actions">



                    <Link

                        to="/vendas/nova"

                    >



                        <Button

                            variant="primary"

                        >



                            <ShoppingCart size={18} />


                            Nova Venda



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





                <div className="vendas-filtros">


                    <SearchInput

                        value={pesquisa}

                        onChange={(e) =>

                            setPesquisa(e.target.value)

                        }

                        placeholder="Buscar venda..."

                    />



                </div>









                {


                    carregando ? (


                        <Loading

                            texto="Carregando vendas..."

                        />


                    )

                        :


                        vendasFiltradas.length === 0 ? (


                            <EmptyState


                                titulo="Nenhuma venda encontrada"


                                descricao="Registre uma nova venda para começar."


                                icone="🛒"


                            />


                        )


                            :


                            (


                                <DataTable


                                    columns={columns}


                                    data={vendasFiltradas}


                                    emptyMessage="Nenhuma venda encontrada."


                                />


                            )


                }







            </SectionCard>






        </main>


    );


}



export default Vendas;