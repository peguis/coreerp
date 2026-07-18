function Tabela({ colunas, children }) {

    return (

        <table
            style={{
                width: "100%",
                borderCollapse: "collapse",
                marginTop: 20
            }}
        >

            <thead>

                <tr>

                    {
                        colunas.map((coluna) => (

                            <th
                                key={coluna}
                                style={{
                                    border: "1px solid #ddd",
                                    padding: 10,
                                    textAlign: "left"
                                }}
                            >
                                {coluna}
                            </th>

                        ))
                    }

                </tr>

            </thead>


            <tbody>

                {children}

            </tbody>


        </table>

    );

}


export default Tabela;