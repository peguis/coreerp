import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";

import DataTable from "../ui/DataTable";

import Badge from "../Badge";


import {
    formatarMoeda
} from "../../utils/formatters";


import {
    formatDate
} from "../../utils/date";




export default function TabelaVendas({

    vendas = []

}) {



    const columns = [


        {

            key: "cliente",

            title: "Cliente"

        },


        {

            key: "total",

            title: "Total",

            render: (valor) =>

                formatarMoeda(valor)

        },


        {

            key: "status",

            title: "Status",

            render: (valor) => (


                <Badge

                    tipo={

                        valor === "CANCELADA"

                            ? "danger"

                            :

                            valor === "PENDENTE"

                                ? "warning"

                                :

                                "success"

                    }

                >

                    {valor || "SEM STATUS"}

                </Badge>


            )

        },


        {

            key: "data",

            title: "Data",

            render: (valor) =>

                formatDate(valor)

        }


    ];





    return (


        <SectionCard

            titulo="Últimas Vendas"

        >



            {

                vendas.length === 0 ?



                    (

                        <EmptyState

                            titulo="Nenhuma venda encontrada"

                            descricao="As vendas aparecerão aqui."

                            icone="🛒"

                        />

                    )



                    :



                    (


                        <DataTable

                            columns={columns}

                            data={vendas}

                        />


                    )


            }



        </SectionCard>


    );


}