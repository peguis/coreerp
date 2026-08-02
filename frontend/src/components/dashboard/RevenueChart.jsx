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

                                        strokeDasharray="3 3"

                                    />



                                    <XAxis

                                        dataKey="mes"

                                    />



                                    <YAxis />



                                    <Tooltip

                                        formatter={(valor) =>

                                            formatarMoeda(valor)

                                        }

                                    />



                                    <Bar

                                        dataKey="valor"

                                    />



                                </BarChart>



                            </ResponsiveContainer>



                        </div>


                    )


            }



        </SectionCard>


    );


}