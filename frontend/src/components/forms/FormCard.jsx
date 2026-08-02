import "./FormCard.css";


export default function FormCard({

    titulo,

    subtitulo,

    children,

    className = ""

}) {


    return (

        <section className={`form-card ${className}`}>


            {
                titulo && (

                    <div className="form-card-header">

                        <h2>

                            {titulo}

                        </h2>


                        {
                            subtitulo && (

                                <p>

                                    {subtitulo}

                                </p>

                            )
                        }

                    </div>

                )
            }



            <div className="form-card-body">

                {children}

            </div>


        </section>

    );

}