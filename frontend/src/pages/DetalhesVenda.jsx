import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    ArrowLeft
} from "lucide-react";


import {
    buscarVenda
} from "../services/vendaService";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";

import Button from "../components/forms/Button";

import {
    formatarDataHora
} from "../utils/formatters";

import "./DetalhesVenda.css";



function DetalhesVenda() {


    const {
        id
    } = useParams();


    const navigate = useNavigate();



    const [venda, setVenda] = useState(null);




    useEffect(() => {

        carregar();

    }, []);





    async function carregar() {


        try {


            const dados =
                await buscarVenda(id);


            setVenda(dados);



        } catch (erro) {


            console.error(
                "Erro ao carregar venda:",
                erro
            );


        }


    }







    function moeda(valor) {


        return new Intl.NumberFormat(
            "pt-PT",
            {
                style: "currency",
                currency: "EUR"
            }

        ).format(

            Number(valor || 0)

        );


    }







    if (!venda) {


        return (

            <main className="detalhes-venda-page">

                <h2>
                    Carregando venda...
                </h2>

            </main>

        );


    }








    return (


        <main className="detalhes-venda-page">





            <PageHeader

                titulo={`Venda #${venda.id}`}

                subtitulo="Detalhes da venda realizada"

            >



                <Button

                    variant="secondary"

                    onClick={() =>
                        navigate("/vendas")
                    }

                >

                    <ArrowLeft size={18} />

                    Voltar


                </Button>



            </PageHeader>









            <div className="venda-info-grid">





                <SectionCard>


                    <h2>
                        Informações da Venda
                    </h2>



                    <p>

                        <strong>Status:</strong>

                        {" "}

                        {venda.status}

                    </p>



                    <p>

                        <strong>Data:</strong>{" "}

                        {formatarDataHora(venda.created_at)}

                    </p>



                    <p>

                        <strong>Cliente ID:</strong>

                        {" "}

                        {venda.cliente_id}


                    </p>



                </SectionCard>








                <SectionCard>


                    <h2>
                        Resumo Financeiro
                    </h2>



                    <div className="total-venda">


                        {moeda(venda.total)}


                    </div>



                </SectionCard>



            </div>









            <SectionCard>


                <h2>
                    Produtos da Venda
                </h2>





                {

                    !venda.itens ||
                        venda.itens.length === 0

                        ?

                        <p>
                            Nenhum item encontrado.
                        </p>


                        :



                        <table className="venda-table">


                            <thead>


                                <tr>

                                    <th>
                                        Produto
                                    </th>


                                    <th>
                                        Quantidade
                                    </th>


                                    <th>
                                        Preço Unitário
                                    </th>


                                    <th>
                                        Subtotal
                                    </th>


                                </tr>


                            </thead>





                            <tbody>


                                {

                                    venda.itens.map(
                                        item => (


                                            <tr
                                                key={
                                                    item.id
                                                }
                                            >


                                                <td>


                                                    {

                                                        item.produto?.nome

                                                        ||

                                                        `Produto ${item.produto_id}`

                                                    }


                                                </td>




                                                <td>

                                                    {
                                                        item.quantidade
                                                    }

                                                </td>




                                                <td>

                                                    {
                                                        moeda(
                                                            item.preco_unitario
                                                        )
                                                    }


                                                </td>




                                                <td>

                                                    {
                                                        moeda(
                                                            item.subtotal
                                                        )
                                                    }


                                                </td>




                                            </tr>


                                        )

                                    )

                                }


                            </tbody>


                        </table>


                }





            </SectionCard>







        </main>


    );


}



export default DetalhesVenda;