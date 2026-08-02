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

                                        strokeDasharray="3 3"

                                    />



                                    <XAxis

                                        dataKey="nome"

                                    />



                                    <YAxis />



                                    <Tooltip />



                                    <Bar

                                        dataKey="quantidade"

                                    />



                                </BarChart>



                            </ResponsiveContainer>



                        </div>


                    )


            }



        </SectionCard>


    );


}