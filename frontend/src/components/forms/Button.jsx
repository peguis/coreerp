import "./Button.css";


export default function Button({

    children,

    type = "button",

    variant = "primary",

    size = "default",

    onClick,

    className = "",

    disabled = false,

    loading = false,

    loadingLabel = "Carregando..."

}) {


    return (

        <button

            type={type}

            onClick={onClick}

            disabled={disabled || loading}
            aria-busy={loading || undefined}

            className={`
                form-button
                ${variant}
                ${size}
                ${className}
            `}

        >

            {
                loading
                    ? loadingLabel
                    : children
            }

        </button>

    );

}
