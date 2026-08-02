import "./PageHeader.css";


export default function PageHeader({

    titulo,

    subtitulo,

    children

}) {


    return (

        <header className="page-header">


            <div className="page-header-info">


                <h1>

                    {titulo}

                </h1>



                {

                    subtitulo && (

                        <p>

                            {subtitulo}

                        </p>

                    )

                }


            </div>



            {

                children && (

                    <div className="page-header-actions">

                        {children}

                    </div>

                )

            }



        </header>

    );

}