import "./StatCard.css";


export default function StatCard({

    titulo,
    valor,
    icone,
    cor

}) {


    return (

        <div className="stat-card">


            <div

                className="stat-icon"

                style={{
                    background: cor
                }}

            >

                {icone}

            </div>





            <div className="stat-content">


                <span className="stat-title">

                    {titulo}

                </span>



                <strong className="stat-value">

                    {valor}

                </strong>



            </div>



        </div>

    );

}