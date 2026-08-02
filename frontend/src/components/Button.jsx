import "./Button.css";


export default function Button({

    children,

    tipo = "default",

    className = "",

    onClick,

    disabled = false,

    type = "button",

    icone

}) {


    return (


        <button


            type={type}


            disabled={disabled}


            onClick={onClick}


            className={

                `btn btn-${tipo} ${className}`

            }


        >


            {

                icone && (

                    <span className="btn-icon">

                        {icone}

                    </span>

                )

            }



            {children}



        </button>


    );


}