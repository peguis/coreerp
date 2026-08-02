import "./Card.css";


export default function Card({

    titulo,

    valor,

    icone,

    children,

    className = ""

}) {


    return (

        <div className={`card ${className}`}>


            {
                icone && (

                    <div className="card-icon">

                        {icone}

                    </div>

                )
            }



            <div className="card-content">


                {
                    titulo && (

                        <p className="card-title">

                            {titulo}

                        </p>

                    )
                }



                {
                    valor && (

                        <strong className="card-value">

                            {valor}

                        </strong>

                    )
                }



                {children}


            </div>



        </div>

    );

}