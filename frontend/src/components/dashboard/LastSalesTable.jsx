import "./DashboardTable.css";


export default function LastSalesTable({ vendas }) {


    return (

        <table className="dashboard-table">


            <thead>

                <tr>

                    <th>
                        ID
                    </th>


                    <th>
                        Total
                    </th>


                    <th>
                        Status
                    </th>

                </tr>


            </thead>




            <tbody>


                {vendas.map(venda => (


                    <tr key={venda.id}>


                        <td>
                            #{venda.id}
                        </td>


                        <td>
                            formatarMoeda(valor)
                        </td>


                        <td>

                            <span className="status-badge">

                                {venda.status}

                            </span>


                        </td>


                    </tr>


                ))}


            </tbody>



        </table>

    );

}