import SectionCard from "../ui/SectionCard";
import { formatarMoeda } from "../../utils/formatters";



export default function FinanceiroResumo({

    financeiro = {}

}) {



    const dados = [


        {

            titulo: "Receitas recebidas",

            valor: financeiro.receitas_recebidas || 0

        },


        {

            titulo: "Despesas pagas",

            valor: financeiro.despesas_pagas || 0

        },


        {

            titulo: "Saldo atual",

            valor: financeiro.saldo || 0

        }


    ];




    return (


        <div className="dashboard-grid">


            {

                dados.map(item => (


                    <SectionCard key={item.titulo} titulo={item.titulo}>
                        <strong>{formatarMoeda(item.valor)}</strong>
                    </SectionCard>


                ))

            }


        </div>


    );


}
