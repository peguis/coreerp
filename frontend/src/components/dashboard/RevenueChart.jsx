import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";

import {
    formatarMoeda
} from "../../utils/formatters";


import {

    BarChart,

    Bar,

    XAxis,

    YAxis,

    CartesianGrid,

    Tooltip,

    ResponsiveContainer

} from "recharts";


import "./RevenueChart.css";




export default function RevenueChart({

    dados = []

}) {



    return (


        <SectionCard

            titulo="Faturamento por mês"

        >



            {

                dados.length === 0 ?



                    (

                        <EmptyState

                            titulo="Sem faturamento"

                            descricao="Ainda não existem dados de faturamento."

                            icone="📊"

                        />

                    )



                    :



                    (


                        <div className="chart-container">


                            <ResponsiveContainer

                                width="100%"

                                height={300}

                            >



                                <BarChart

                                    data={dados}

                                >



                                    <CartesianGrid

                                        stroke="var(--hype-border)"
                                        strokeDasharray="3 3"

                                    />



                                    <XAxis

                                        dataKey="mes"
                                        tick={{ fill: "var(--hype-text-secondary)", fontSize: 12 }}
                                        axisLine={{ stroke: "var(--hype-border)" }}
                                        tickLine={false}

                                    />



                                    <YAxis tick={{ fill: "var(--hype-text-secondary)", fontSize: 12 }} axisLine={false} tickLine={false} />



                                    <Tooltip
                                        contentStyle={{ background: "var(--hype-surface-elevated)", border: "1px solid var(--hype-border)", borderRadius: "10px", color: "var(--hype-text)" }}
                                        labelStyle={{ color: "var(--hype-text-secondary)" }}

                                        formatter={(valor) =>

                                            formatarMoeda(valor)

                                        }

                                    />



                                    <Bar

                                        dataKey="valor"
                                        fill="var(--hype-gold)"
                                        radius={[4, 4, 0, 0]}

                                    />



                                </BarChart>



                            </ResponsiveContainer>



                        </div>


                    )


            }



        </SectionCard>


    );


}
