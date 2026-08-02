export default function LowStockProducts({ produtos }) {


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

                Produtos com estoque baixo

            </h2>





            {

                produtos.length === 0 ? (


                    <p>

                        Nenhum produto com estoque baixo.

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

                                        padding: 12,

                                        borderBottom: "1px solid #eee"

                                    }}

                                >

                                    Produto

                                </th>



                                <th

                                    style={{

                                        textAlign: "left",

                                        padding: 12,

                                        borderBottom: "1px solid #eee"

                                    }}

                                >

                                    Estoque atual

                                </th>



                                <th

                                    style={{

                                        textAlign: "left",

                                        padding: 12,

                                        borderBottom: "1px solid #eee"

                                    }}

                                >

                                    Estoque mínimo

                                </th>


                            </tr>


                        </thead>





                        <tbody>


                            {

                                produtos.map(produto => (


                                    <tr key={produto.id}>


                                        <td

                                            style={{

                                                padding: 12,

                                                borderBottom: "1px solid #eee"

                                            }}

                                        >

                                            {produto.nome}

                                        </td>




                                        <td

                                            style={{

                                                padding: 12,

                                                borderBottom: "1px solid #eee"

                                            }}

                                        >

                                            {produto.estoque}

                                        </td>





                                        <td

                                            style={{

                                                padding: 12,

                                                borderBottom: "1px solid #eee"

                                            }}

                                        >

                                            {produto.minimo}

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