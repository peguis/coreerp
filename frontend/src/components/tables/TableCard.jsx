import "./TableCard.css";


export default function TableCard({

    titulo,
    children

}) {


    return (

        <div className="table-card">


            <div className="table-card-header">


                <h2>

                    {titulo}

                </h2>


            </div>



            <div className="table-card-body">

                {children}

            </div>



        </div>

    );

}