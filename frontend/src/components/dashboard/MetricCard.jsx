import {
    Package,
    Users,
    ShoppingCart,
    AlertTriangle,
    DollarSign,
    Wallet,
    TrendingUp,
    TrendingDown
} from "lucide-react";

import SectionCard from "../ui/SectionCard";

import "./MetricCard.css";


const icones = {

    Produtos: Package,

    Clientes: Users,

    Vendas: ShoppingCart,

    "Estoque baixo": AlertTriangle,

    Faturamento: DollarSign,

    "Saldo financeiro": Wallet,

    "A receber": TrendingUp,

    "A pagar": TrendingDown

};



export default function MetricCard({

    titulo,

    valor

}) {


    const Icon = icones[titulo] || Package;



    return (

        <SectionCard>


            <div className="metric-card">


                <div className="metric-card-icon">

                    <Icon size={28} />

                </div>



                <div className="metric-card-content">


                    <span className="metric-card-title">

                        {titulo}

                    </span>



                    <strong className="metric-card-value">

                        {valor}

                    </strong>


                </div>


            </div>


        </SectionCard>

    );

}