import "../ui/DashboardTable.css";


export default function DataTable({

    columns = [],

    data = [],

    emptyMessage = "Nenhum registro encontrado."

}) {


    return (

        <div className="table-container">


            <table className="dashboard-table">


                <thead>

                    <tr>

                        {
                            columns.map((coluna, index) => (

                                <th key={coluna.key || index}>

                                    {coluna.title}

                                </th>

                            ))
                        }

                    </tr>

                </thead>



                <tbody>


                    {
                        data.length === 0 ? (

                            <tr>

                                <td

                                    colSpan={columns.length}

                                    className="table-empty"

                                >

                                    {emptyMessage}

                                </td>

                            </tr>


                        ) : (


                            data.map((item, index) => (


                                <tr key={item.id || index}>


                                    {

                                        columns.map((coluna, i) => (


                                            <td key={coluna.key || i}>


                                                {

                                                    coluna.render

                                                        ?

                                                        coluna.render(

                                                            item[coluna.key],

                                                            item

                                                        )

                                                        :

                                                        item[coluna.key]

                                                }


                                            </td>


                                        ))

                                    }


                                </tr>


                            ))

                        )

                    }


                </tbody>


            </table>


        </div>

    );

}