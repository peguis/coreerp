import "./EmptyState.css";


export default function EmptyState({

    titulo = "Nenhum registro encontrado",

    descricao = "Não existem dados para exibir.",

    icone = "📭",

    children

}) {


    return (

        <div className="empty-state">


            <div className="empty-state-icon">

                {icone}

            </div>



            <h3>

                {titulo}

            </h3>



            <p>

                {descricao}

            </p>



            {

                children && (

                    <div className="empty-state-action">

                        {children}

                    </div>

                )

            }



        </div>

    );

}