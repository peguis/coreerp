import "./Loading.css";


export default function Loading({

    texto = "Carregando..."

}) {


    return (

        <div className="loading-container" role="status" aria-live="polite">


            <div className="loading-spinner"></div>


            <p>

                {texto}

            </p>


        </div>

    );

}
