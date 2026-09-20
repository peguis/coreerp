import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";


import {
    formatarMoeda
} from "../../utils/formatters";


import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend
} from "recharts";


import "./FluxoCaixaChart.css";



export default function FluxoCaixaChart({

    financeiro = {}

}) {



    const dados = [


        {
            name: "Recebido",
            value: Number(financeiro.receitas_recebidas || 0)
        },


        {
            name: "Pago",
            value: Number(financeiro.despesas_pagas || 0)
        },


        {
            name: "Saldo",
            value: Number(financeiro.saldo || 0)
        }


    ];



    const possuiDados = dados.some(

        item => item.value > 0

    );



    const cores = [

        "#43c58b",

        "#e26b72",

        "var(--tenant-accent)"

    ];



    return (


        <SectionCard titulo="Fluxo de Caixa">


            {


                !possuiDados ? (


                    <EmptyState

                        titulo="Sem dados financeiros"

                        descricao="Não existem movimentações financeiras para exibir."

                        icone="💰"

                    />


                ) : (


                    <div className="chart-container">


                        <ResponsiveContainer

                            width="100%"

                            height={300}

                        >


                            <PieChart>


                                <Pie

                                    data={dados}

                                    dataKey="value"

                                    nameKey="name"

                                    outerRadius={100}

                                    labelLine={false}

                                >


                                    {

                                        dados.map((item, index) => (


                                            <Cell

                                                key={item.name}

                                                fill={cores[index]}

                                            />


                                        ))

                                    }


                                </Pie>


                                <Tooltip
                                    contentStyle={{ background: "var(--tenant-surface-elevated)", border: "1px solid var(--tenant-border)", borderRadius: "10px", color: "var(--tenant-text)" }}

                                    formatter={(valor) =>

                                        formatarMoeda(valor)

                                    }

                                />


                                <Legend wrapperStyle={{ color: "var(--tenant-text-secondary)" }} />


                            </PieChart>


                        </ResponsiveContainer>


                    </div>


                )


            }


        </SectionCard>


    );


}
