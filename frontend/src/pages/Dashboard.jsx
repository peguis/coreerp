import { useEffect, useState } from "react";


import {
    obterDashboard
} from "../services/dashboardService";


import DashboardSkeleton from "../components/dashboard/DashboardSkeleton";


import MetricCard from "../components/dashboard/MetricCard";
import FinanceiroCards from "../components/dashboard/FinanceiroCards";
import AlertasDashboard from "../components/dashboard/AlertasDashboard";
import EstoqueBaixo from "../components/dashboard/EstoqueBaixo";
import EstoqueParado from "../components/dashboard/EstoqueParado";
import TabelaVendas from "../components/dashboard/TabelaVendas";
import RevenueChart from "../components/dashboard/RevenueChart";
import SalesChart from "../components/dashboard/SalesChart";
import TopClientes from "../components/dashboard/TopClientes";
import FluxoCaixaChart from "../components/dashboard/FluxoCaixaChart";


import {
    formatarMoeda
} from "../utils/formatters";


import PageHeader from "../components/ui/PageHeader";


import "./Dashboard.css";



function Dashboard() {


    const [dados, setDados] = useState(null);



    useEffect(() => {

        carregar();

    }, []);




    async function carregar() {


        try {


            const resposta =
                await obterDashboard();


            setDados(resposta);


        } catch (erro) {


            console.error(

                "Erro dashboard:",

                erro.response?.data || erro

            );


        }


    }




    if (!dados) {


        return <DashboardSkeleton />;


    }





    const financeiro = dados.financeiro || {


        saldo: 0,

        total_receber: 0,

        total_pagar: 0,

        receitas_recebidas: 0,

        despesas_pagas: 0


    };






    const cards = [


        {
            titulo: "Produtos",
            valor: dados.total_produtos ?? 0
        },


        {
            titulo: "Clientes",
            valor: dados.total_clientes ?? 0
        },


        {
            titulo: "Vendas",
            valor: dados.total_vendas ?? 0
        },


        {
            titulo: "Estoque baixo",
            valor: dados.estoque_baixo ?? 0
        },


        {
            titulo: "Faturamento",
            valor: formatarMoeda(dados.faturamento ?? 0)
        },


        {
            titulo: "Saldo financeiro",
            valor: formatarMoeda(financeiro.saldo)
        },


        {
            titulo: "A receber",
            valor: formatarMoeda(financeiro.total_receber)
        },


        {
            titulo: "A pagar",
            valor: formatarMoeda(financeiro.total_pagar)
        }


    ];






    return (


        <main className="dashboard-page">


            <PageHeader

                titulo="Dashboard"

                subtitulo="Visão geral da empresa"

            />





            <section className="dashboard-cards">


                {

                    cards.map(card => (


                        <MetricCard

                            key={card.titulo}

                            titulo={card.titulo}

                            valor={card.valor}

                        />


                    ))

                }


            </section>





            <FinanceiroCards

                financeiro={financeiro}

            />






            <AlertasDashboard

                alertas={

                    dados.alertas || {

                        produtos_zerados: [],

                        produtos_criticos: [],

                        contas_pendentes: []

                    }

                }

            />






            <section className="dashboard-grid">


                <EstoqueBaixo

                    produtos={

                        dados.produtos_baixo_estoque || []

                    }

                />



                <TabelaVendas

                    vendas={

                        dados.ultimas_vendas || []

                    }

                />


            </section>






            <section className="dashboard-grid">


                <EstoqueParado

                    produtos={

                        dados.produtos_sem_giro || []

                    }

                />



                <FluxoCaixaChart

                    financeiro={financeiro}

                />


            </section>






            <section className="dashboard-grid">


                <RevenueChart

                    dados={

                        dados.vendas_por_mes || []

                    }

                />



                <SalesChart

                    dados={

                        dados.produtos_mais_vendidos || []

                    }

                />


            </section>






            <TopClientes

                dados={

                    dados.clientes_top || []

                }

            />



        </main>


    );


}



export default Dashboard;