export default function RecentSales({ vendas }) {


    return (

        <div
            style={{
                background: "#fff",
                borderRadius: 14,
                padding: 24,
                marginTop: 24,
                boxShadow: "0 2px 12px rgba(0,0,0,.08)"
            }}
        >

            <h2
                style={{
                    marginBottom: 20,
                    fontSize: 22
                }}
            >
                Últimas vendas
            </h2>


            {
                vendas.length === 0 ? (

                    <p>
                        Nenhuma venda registrada.
                    </p>

                ) : (


                    <table

                        style={{

                            width: "100%",
                            borderCollapse: "collapse"

                        }}

                    >

                        <thead>

                            <tr>

                                <th
                                    style={{
                                        textAlign: "left",
                                        padding: "12px",
                                        borderBottom: "1px solid #eee"
                                    }}
                                >
                                    ID
                                </th>


                                <th
                                    style={{
                                        textAlign: "left",
                                        padding: "12px",
                                        borderBottom: "1px solid #eee"
                                    }}
                                >
                                    Total
                                </th>


                                <th
                                    style={{
                                        textAlign: "left",
                                        padding: "12px",
                                        borderBottom: "1px solid #eee"
                                    }}
                                >
                                    Status
                                </th>


                            </tr>

                        </thead>



                        <tbody>


                            {
                                vendas.map(venda => (

                                    <tr key={venda.id}>


                                        <td
                                            style={{
                                                padding: "12px",
                                                borderBottom: "1px solid #eee"
                                            }}
                                        >
                                            #{venda.id}
                                        </td>



                                        <td
                                            style={{
                                                padding: "12px",
                                                borderBottom: "1px solid #eee"
                                            }}
                                        >

                                            formatarMoeda(valor)

                                        </td>



                                        <td
                                            style={{
                                                padding: "12px",
                                                borderBottom: "1px solid #eee"
                                            }}
                                        >

                                            <span
                                                style={{

                                                    padding: "5px 12px",
                                                    borderRadius: 20,
                                                    background: "#dcfce7",
                                                    color: "#166534",
                                                    fontSize: 14

                                                }}
                                            >

                                                {venda.status}

                                            </span>

                                        </td>


                                    </tr>

                                ))
                            }


                        </tbody>


                    </table>


                )

            }


        </div>

    );

}