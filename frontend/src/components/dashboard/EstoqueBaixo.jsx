import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";

import DataTable from "../ui/DataTable";

import Badge from "../Badge";



export default function EstoqueBaixo({

    produtos = []

}) {



    const columns = [


        {
            key: "nome",
            title: "Produto"
        },


        {
            key: "estoque",
            title: "Estoque"
        },


        {
            key: "estoque_minimo",
            title: "Mínimo"
        },


        {
            key: "status",

            title: "Status",

            render: () => (

                <Badge tipo="warning">

                    Baixo

                </Badge>

            )

        }


    ];



    return (

        <SectionCard titulo="Produtos com Estoque Baixo">


            {

                produtos.length === 0 ?


                    <EmptyState

                        titulo="Estoque normal"

                        descricao="Nenhum produto abaixo do mínimo."

                        icone="📦"

                    />


                    :


                    <DataTable

                        columns={columns}

                        data={produtos}

                    />

            }


        </SectionCard>

    );


}