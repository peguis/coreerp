import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";

import DataTable from "../ui/DataTable";

import Badge from "../Badge";



export default function EstoqueParado({

    produtos = []

}) {



    const columns = [


        {

            key: "nome",

            title: "Produto"

        },


        {

            key: "estoque",

            title: "Estoque atual"

        },


        {

            key: "situacao",

            title: "Situação",

            render: () => (


                <Badge tipo="danger">

                    Estoque parado

                </Badge>


            )

        }


    ];





    return (


        <SectionCard titulo="Estoque Parado">


            {

                produtos.length === 0 ?


                    <EmptyState

                        titulo="Nenhum estoque parado"

                        descricao="Todos os produtos possuem movimentação."

                        icone="📈"

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