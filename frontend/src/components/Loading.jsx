import "./Loading.css";


export default function Loading({

    texto = "Carregando..."

}) {


    return (

        <div className="loading-container">


            <div className="loading-spinner"></div>


            <p>

                {texto}

            </p>


        </div>

    );

}