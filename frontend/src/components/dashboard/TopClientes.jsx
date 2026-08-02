import SectionCard from "../ui/SectionCard";

import EmptyState from "../ui/EmptyState";

import DataTable from "../ui/DataTable";


import {
    formatarMoeda
} from "../../utils/formatters";



export default function TopClientes({

    dados = []

}) {



    const columns = [


        {

            key: "nome",

            title: "Cliente"

        },


        {

            key: "valor",

            title: "Total comprado",


            render: (valor) =>

                formatarMoeda(valor)

        }


    ];





    return (


        <SectionCard titulo="Top Clientes">


            {

                dados.length === 0 ?


                    <EmptyState

                        titulo="Nenhum cliente encontrado"

                        descricao="Ainda não existem compras registradas."

                        icone="👥"

                    />


                    :


                    <DataTable

                        columns={columns}

                        data={dados}

                    />


            }



        </SectionCard>


    );


}