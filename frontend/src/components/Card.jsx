function Card({ titulo, valor }) {

    return (

        <div
            style={{
                border: "1px solid #ddd",
                borderRadius: 10,
                padding: 20,
                width: 220,
                boxShadow: "0 2px 8px rgba(0,0,0,.1)"
            }}
        >

            <h3>{titulo}</h3>

            <h1>{valor}</h1>

        </div>

    );

}

export default Card;