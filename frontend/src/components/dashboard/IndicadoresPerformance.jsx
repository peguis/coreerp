export default function IndicadoresPerformance({ dados }) {


    if (!dados) {

        return null;

    }



    return (

        <div className="indicadores-performance">


            <div className="indicador-card">

                <h3>

                    Ticket médio

                </h3>


                <strong>

                    formatarMoeda(valor)

                </strong>


            </div>





            <div className="indicador-card">

                <h3>

                    Média de vendas

                </h3>


                <strong>

                    formatarMoeda(valor)

                </strong>


            </div>






            <div className="indicador-card">

                <h3>

                    Conversão clientes

                </h3>


                <strong>

                    formatarMoeda(valor)%

                </strong>


            </div>






            <div className="indicador-card">

                <h3>

                    Crescimento

                </h3>


                <strong>

                    formatarMoeda(valor)%

                </strong>


            </div>


        </div>

    );

}