export default function SectionCard({
    titulo,
    children
}) {


    return (

        <section

            style={{

                background: "#ffffff",

                borderRadius: 16,

                padding: 24,

                marginBottom: 24,

                boxShadow:
                    "0 4px 15px rgba(0,0,0,0.06)"

            }}

        >


            <h2

                style={{

                    marginTop: 0,

                    marginBottom: 20,

                    fontSize: 20,

                    fontWeight: 700,

                    color: "#0f172a"

                }}

            >

                {titulo}

            </h2>



            {children}



        </section>

    );

}