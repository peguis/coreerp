import SectionCard from "../ui/SectionCard";
import Badge from "../Badge";

import {
    formatarMoeda
} from "../../utils/formatters";


import "./AlertasDashboard.css";



export default function AlertasDashboard({

    alertas = {}

}) {


    const produtosZerados =
        alertas.produtos_zerados || [];


    const produtosCriticos =
        alertas.produtos_criticos || [];


    const contasPendentes =
        alertas.contas_pendentes || [];



    const vazio =

        produtosZerados.length === 0 &&

        produtosCriticos.length === 0 &&

        contasPendentes.length === 0;



    if (vazio) {


        return (

            <SectionCard titulo="Alertas">


                <div className="alerta-success">


                    <Badge tipo="success">

                        ✓

                    </Badge>


                    Nenhum alerta pendente.


                </div>


            </SectionCard>

        );

    }



    return (

        <SectionCard titulo="Alertas do Sistema">


            <div className="alertas-container">


                {
                    produtosZerados.length > 0 && (

                        <div className="alerta-item">


                            <Badge tipo="danger">

                                Sem estoque

                            </Badge>


                            {
                                produtosZerados.map(produto => (

                                    <p key={produto.id}>

                                        {produto.nome}

                                    </p>

                                ))
                            }


                        </div>

                    )
                }




                {
                    produtosCriticos.length > 0 && (

                        <div className="alerta-item">


                            <Badge tipo="warning">

                                Estoque crítico

                            </Badge>


                            {
                                produtosCriticos.map(produto => (

                                    <p key={produto.id}>

                                        {produto.nome}

                                        {" - Estoque: "}

                                        {produto.estoque}

                                    </p>

                                ))
                            }


                        </div>

                    )
                }





                {
                    contasPendentes.length > 0 && (

                        <div className="alerta-item">


                            <Badge tipo="default">

                                Financeiro

                            </Badge>



                            {
                                contasPendentes.map(conta => (

                                    <p key={conta.id}>


                                        {conta.descricao}


                                        {" - "}


                                        {formatarMoeda(conta.valor)}


                                    </p>

                                ))
                            }


                        </div>

                    )
                }


            </div>


        </SectionCard>

    );

}