import {
    Wallet,
    ArrowDownCircle,
    ArrowUpCircle,
    TrendingUp,
    TrendingDown
} from "lucide-react";


import SectionCard from "../ui/SectionCard";

import {
    formatarMoeda
} from "../../utils/formatters";


import "./FinanceiroCards.css";



export default function FinanceiroCards({

    financeiro = {}

}) {


    const cards = [


        {
            titulo: "Saldo atual",
            valor: financeiro.saldo || 0,
            icone: Wallet
        },


        {
            titulo: "A receber",
            valor: financeiro.total_receber || 0,
            icone: ArrowDownCircle
        },


        {
            titulo: "A pagar",
            valor: financeiro.total_pagar || 0,
            icone: ArrowUpCircle
        },


        {
            titulo: "Receitas recebidas",
            valor: financeiro.receitas_recebidas || 0,
            icone: TrendingUp
        },


        {
            titulo: "Despesas pagas",
            valor: financeiro.despesas_pagas || 0,
            icone: TrendingDown
        }


    ];




    return (

        <div className="financeiro-cards-grid">


            {
                cards.map((card) => {


                    const Icon = card.icone;



                    return (

                        <SectionCard
                            key={card.titulo}
                        >


                            <div className="financeiro-card">


                                <div className="financeiro-card-icon">

                                    <Icon size={26} />

                                </div>



                                <div>


                                    <span className="financeiro-card-title">

                                        {card.titulo}

                                    </span>



                                    <strong className="financeiro-card-value">

                                        {formatarMoeda(card.valor)}

                                    </strong>


                                </div>


                            </div>


                        </SectionCard>

                    );


                })

            }


        </div>

    );

}