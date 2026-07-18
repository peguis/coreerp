function Mensagem({ tipo, texto }) {


    if (!texto) {
        return null;
    }


    return (

        <div
            style={{
                padding: 10,
                margin: 10,
                borderRadius: 5,
                background:
                    tipo === "erro"
                        ? "#ffdddd"
                        : "#ddffdd"
            }}
        >

            {texto}

        </div>

    );

}


export default Mensagem;