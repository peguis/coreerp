import "./Badge.css";


export default function Badge({

    children,

    tipo = "default",

    className = ""

}) {


    return (

        <span

            className={
                `badge badge-${tipo} ${className}`
            }

        >

            {children}

        </span>

    );

}