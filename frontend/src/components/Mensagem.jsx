import "./Mensagem.css";


export default function Mensagem({

    tipo = "sucesso",

    texto

}) {


    if (!texto) {

        return null;

    }



    return (

        <div className={`mensagem mensagem-${tipo}`}>

            {texto}

        </div>

    );

}