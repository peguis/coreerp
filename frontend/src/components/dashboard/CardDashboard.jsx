import "./CardDashboard.css";


export default function CardDashboard({

    titulo,

    valor,

    icone: Icon

}) {


    return (


        <div className="card-dashboard">



            <div className="card-dashboard-header">


                {

                    Icon && (

                        <Icon size={24} />

                    )

                }


                <span>

                    {titulo}

                </span>



            </div>




            <strong>

                {valor}

            </strong>



        </div>


    );


}