import "./SectionCard.css";


export default function SectionCard({

    titulo,

    subtitulo,

    children

}) {


    return (


        <section className="section-card">



            {

                titulo && (

                    <div className="section-header">


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



            <div className="section-content">

                {children}

            </div>



        </section>


    );

}