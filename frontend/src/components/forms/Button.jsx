import "./Button.css";


export default function Button({

    children,

    type = "button",

    variant = "primary",

    size = "default",

    onClick,

    className = "",

    disabled = false,

    loading = false

}) {


    return (

        <button

            type={type}

            onClick={onClick}

            disabled={disabled || loading}

            className={`
                form-button
                ${variant}
                ${size}
                ${className}
            `}

        >

            {
                loading
                    ? "Carregando..."
                    : children
            }

        </button>

    );

}