import "./Mensagem.css";


export default function Mensagem({

    tipo = "sucesso",

    texto

}) {


    if (!texto) {

        return null;

    }



    return (

        <div className={`mensagem mensagem-${tipo}`} role={tipo === "erro" ? "alert" : "status"} aria-live={tipo === "erro" ? "assertive" : "polite"}>

            {texto}

        </div>

    );

}
