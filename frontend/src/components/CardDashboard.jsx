function CardDashboard({ titulo, valor }) {

    return (

        <div
            style={{
                border: "1px solid #ddd",
                padding: 20,
                borderRadius: 10,
                width: 200,
                background: "#fff"
            }}
        >

            <h3>
                {titulo}
            </h3>


            <h1>
                {valor}
            </h1>


        </div>

    );

}


export default CardDashboard;