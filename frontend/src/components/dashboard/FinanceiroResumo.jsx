import Card from "../Card";



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


                    <SectionCard>


                        key={item.titulo}


                        titulo={item.titulo}


                        valor={

                            formatarMoeda(valor)

                        }


                    </SectionCard>


                ))

            }


        </div>


    );


}