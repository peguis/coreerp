import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
    Plus,
    ArrowUpCircle,
    ArrowDownCircle,
    DollarSign,
    Pencil,
    Trash2,
    CheckCircle
} from "lucide-react";

import {
    formatarMoeda
} from "../utils/formatters";

import {

    confirmDelete

} from "../utils/dialog";


import financeiroService from "../services/financeiroService";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import DataTable from "../components/ui/DataTable";
import EmptyState from "../components/ui/EmptyState";
import CategoriasFinanceiras from "../components/financeiro/CategoriasFinanceiras";

import Badge from "../components/Badge";
import Button from "../components/forms/Button";

import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";


import "./Financeiro.css";



function Financeiro() {


    const navigate = useNavigate();



    const [lancamentos, setLancamentos] = useState([]);


    const [loading, setLoading] = useState(true);


    const [erro, setErro] = useState("");



    const [mensagem, setMensagem] = useState("");



    const [pesquisa, setPesquisa] = useState("");


    const [tipoFiltro, setTipoFiltro] = useState("");


    const [statusFiltro, setStatusFiltro] = useState("");




    const [resumo, setResumo] = useState({

        totalReceber: 0,

        totalPagar: 0,

        saldo: 0

    });






    useEffect(() => {


        carregarDados();


    }, []);






    async function carregarDados() {


        try {


            setLoading(true);


            setErro("");



            const dados = await financeiroService.getLancamentos();




            const lista = Array.isArray(dados)

                ? dados

                : [];




            setLancamentos(lista);




            calcularResumo(lista);




        } catch {


            setErro(
                "Erro ao carregar financeiro."
            );



        } finally {


            setLoading(false);


        }


    }








    function calcularResumo(lista) {



        const receitas = lista

            .filter(item => item.tipo === "RECEITA")

            .reduce(

                (total, item) =>

                    total + Number(item.valor || 0),

                0

            );





        const despesas = lista

            .filter(item => item.tipo === "DESPESA")

            .reduce(

                (total, item) =>

                    total + Number(item.valor || 0),

                0

            );





        setResumo({

            totalReceber: receitas,

            totalPagar: despesas,

            saldo: receitas - despesas

        });



    }









    async function excluir(id) {


        const confirmar =
            confirmDelete(
                "Confirmar pagamento?"
            );



        if (!confirmar)

            return;





        try {



            await financeiroService.excluirLancamento(id);




            setMensagem(
                "Lançamento excluído com sucesso."
            );



            carregarDados();




        } catch (error) {

            setErro(
                "Erro ao excluir lançamento."
            );

        }



    }








    async function baixarLancamento(id) {


        const confirmar =

            confirmDelete(

                "Deseja excluir?"

        );



        if (!confirmar)

            return;






        try {



            await financeiroService.baixarLancamento(id);




            setMensagem(

                "Pagamento confirmado."

            );



            carregarDados();





        } catch {



            setErro(

                "Erro ao baixar lançamento."

            );


        }


    }









    function moeda(valor) {


        return formatarMoeda(valor)


    }









    function dataFormatada(valor) {


        if (!valor)

            return "-";



        return new Date(valor)

            .toLocaleDateString(

                "pt-BR"

            );


    }









    const lancamentosFiltrados = lancamentos.filter(item => {



        const texto = pesquisa

            .toLowerCase()

            .trim();





        const busca =



            item.descricao

                ?.toLowerCase()

                .includes(texto)



            ||



            item.categoria?.nome

                ?.toLowerCase()

                .includes(texto)



            ||



            item.tipo

                ?.toLowerCase()

                .includes(texto)



            ||



            item.status

                ?.toLowerCase()

                .includes(texto);







        const filtroTipo =

            tipoFiltro

                ? item.tipo === tipoFiltro

                : true;





        const filtroStatus =

            statusFiltro

                ? item.status === statusFiltro

                : true;







        return (

            busca

            &&

            filtroTipo

            &&

            filtroStatus

        );



    });









    const colunas = [



        {

            key: "descricao",

            title: "Descrição"

        },



        {

            key: "categoria",

            title: "Categoria",

            render: (_, item) =>

                item.categoria?.nome || "-"

        },



        {

            key: "tipo",

            title: "Tipo",

            render: valor => (



                <Badge

                    tipo={

                        valor === "RECEITA"

                            ?

                            "success"

                            :

                            "danger"

                    }

                >

                    {valor === "RECEITA"

                        ?

                        "Receita"

                        :

                        "Despesa"

                    }

                </Badge>



            )

        },



        {

            key: "valor",

            title: "Valor",

            render: valor => moeda(valor)

        },



        {

            key: "data_vencimento",

            title: "Vencimento",

            render: valor => dataFormatada(valor)

        },



        {

            key: "status",

            title: "Status",

            render: valor => (


                <Badge

                    tipo={

                        valor === "PAGO"

                            ?

                            "success"

                            :

                            "warning"

                    }

                >

                    {

                        valor === "PAGO"

                            ?

                            "Pago"

                            :

                            "Pendente"

                    }

                </Badge>


            )

        },



        {

            key: "acoes",

            title: "Ações",



            render: (_, item) => (


                <div className="financeiro-actions">





                    {

                        item.status !== "PAGO"

                        &&

                        (

                            <Button

                                variant="success"

                                onClick={() =>
                                    baixarLancamento(item.id)
                                }

                            >

                                <CheckCircle size={16} />

                            </Button>

                        )

                    }







                    <Button

                        variant="secondary"

                        onClick={() =>
                            navigate(
                                `/financeiro/${item.id}/editar`
                            )
                        }

                    >

                        <Pencil size={16} />

                    </Button>







                    <Button

                        variant="danger"

                        onClick={() =>
                            excluir(item.id)
                        }

                    >

                        <Trash2 size={16} />

                    </Button>





                </div>


            )


        }


    ];











    return (



        <main className="financeiro-page">





            <PageHeader

                titulo="Financeiro"

                subtitulo="Controle de receitas, despesas e fluxo de caixa"

            >



                <Link to="/financeiro/novo">


                    <Button variant="primary">


                        <Plus size={18} />


                        Novo Lançamento


                    </Button>



                </Link>



            </PageHeader>








            {

                erro &&

                (

                    <Mensagem

                        tipo="erro"

                        texto={erro}

                    />

                )

            }






            {

                mensagem &&

                (

                    <Mensagem

                        tipo="sucesso"

                        texto={mensagem}

                    />

                )

            }









            <div className="financeiro-resumo">



                <SectionCard>


                    <div className="financeiro-card">


                        <ArrowUpCircle size={28} />


                        <div>


                            <span>

                                Receitas

                            </span>


                            <strong>

                                {moeda(resumo.totalReceber)}

                            </strong>


                        </div>


                    </div>


                </SectionCard>







                <SectionCard>


                    <div className="financeiro-card">


                        <ArrowDownCircle size={28} />


                        <div>


                            <span>

                                Despesas

                            </span>


                            <strong>

                                {moeda(resumo.totalPagar)}

                            </strong>


                        </div>


                    </div>


                </SectionCard>







                <SectionCard>


                    <div className="financeiro-card">


                        <DollarSign size={28} />


                        <div>


                            <span>

                                Saldo

                            </span>


                            <strong>

                                {moeda(resumo.saldo)}

                            </strong>


                        </div>


                    </div>


                </SectionCard>



            </div>









            <SectionCard>





                <div className="financeiro-filtros">



                    <input

                        placeholder="Buscar lançamento..."

                        value={pesquisa}

                        onChange={(e) =>
                            setPesquisa(e.target.value)
                        }

                    />




                    <select

                        value={tipoFiltro}

                        onChange={(e) =>
                            setTipoFiltro(e.target.value)
                        }

                    >

                        <option value="">

                            Todos tipos

                        </option>


                        <option value="RECEITA">

                            Receitas

                        </option>


                        <option value="DESPESA">

                            Despesas

                        </option>


                    </select>







                    <select

                        value={statusFiltro}

                        onChange={(e) =>
                            setStatusFiltro(e.target.value)
                        }

                    >

                        <option value="">

                            Todos status

                        </option>


                        <option value="PENDENTE">

                            Pendentes

                        </option>


                        <option value="PAGO">

                            Pagos

                        </option>


                    </select>






                    <Button

                        variant="secondary"

                        onClick={() => {

                            setPesquisa("");

                            setTipoFiltro("");

                            setStatusFiltro("");

                        }}

                    >

                        Limpar

                    </Button>



                </div>









                {

                    loading

                        ?

                        <Loading texto="Carregando financeiro..." />


                        :


                        lancamentosFiltrados.length === 0

                            ?


                            <EmptyState

                                titulo="Nenhum lançamento encontrado"

                                descricao="Cadastre um lançamento financeiro."

                                icone="💰"

                            />


                            :


                            <DataTable

                                columns={colunas}

                                data={lancamentosFiltrados}

                            />


                }





            </SectionCard>

            <SectionCard>

                <div className="financeiro-categorias">

                    <CategoriasFinanceiras />

                </div>

            </SectionCard>





        </main>



    );


}



export default Financeiro;