import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";


import {

    BarChart,

    Bar,

    XAxis,

    YAxis,

    CartesianGrid,

    Tooltip,

    ResponsiveContainer

} from "recharts";


import "./SalesChart.css";




export default function SalesChart({

    dados = []

}) {



    return (


        <SectionCard

            titulo="Produtos mais vendidos"

        >



            {

                dados.length === 0 ?



                    (

                        <EmptyState

                            titulo="Sem vendas"

                            descricao="Ainda não existem produtos vendidos."

                            icone="🛒"

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

                                        stroke="var(--tenant-border)"
                                        strokeDasharray="3 3"

                                    />



                                    <XAxis

                                        dataKey="nome"
                                        tick={{ fill: "var(--tenant-text-secondary)", fontSize: 12 }}
                                        axisLine={{ stroke: "var(--tenant-border)" }}
                                        tickLine={false}

                                    />



                                    <YAxis tick={{ fill: "var(--tenant-text-secondary)", fontSize: 12 }} axisLine={false} tickLine={false} />



                                    <Tooltip contentStyle={{ background: "var(--tenant-surface-elevated)", border: "1px solid var(--tenant-border)", borderRadius: "10px", color: "var(--tenant-text)" }} labelStyle={{ color: "var(--tenant-text-secondary)" }} />



                                    <Bar

                                        dataKey="quantidade"
                                        fill="#aa8dff"
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
