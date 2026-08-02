import PageHeader from "../components/ui/PageHeader";

import "./Configuracoes.css";


function Configuracoes() {


    return (


        <main className="configuracoes-page">


            <PageHeader

                titulo="Configurações"

                subtitulo="Gerencie as preferências do sistema"

            />



            <div className="configuracoes-card">


                <h2>

                    Configurações do sistema

                </h2>


                <p>

                    Área reservada para ajustes da empresa,
                    usuários e preferências.

                </p>


            </div>



        </main>


    );

}


export default Configuracoes;