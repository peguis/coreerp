import "./DashboardTable.css";


export default function LowStockTable({ produtos }) {


    return (

        <table className="dashboard-table">


            <thead>

                <tr>

                    <th>
                        Produto
                    </th>

                    <th>
                        Estoque atual
                    </th>

                    <th>
                        Estoque mínimo
                    </th>

                </tr>

            </thead>



            <tbody>


                {produtos.map(produto => (


                    <tr key={produto.id}>


                        <td>
                            {produto.nome}
                        </td>


                        <td>
                            {produto.estoque}
                        </td>


                        <td>
                            {produto.minimo}
                        </td>



                    </tr>


                ))}


            </tbody>



        </table>

    );

}