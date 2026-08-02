import "./DataTable.css";


export default function DataTable({

    columns = [],

    data = [],

    emptyMessage = "Nenhum registro encontrado.",

    loading = false,

    className = ""

}) {


    if (loading) {


        return (

            <div className="table-container">


                <div className="table-loading">

                    Carregando dados...

                </div>


            </div>

        );


    }



    return (


        <div className={`table-container ${className}`}>


            <table className="dashboard-table">


                <thead>


                    <tr>


                        {

                            columns.map((coluna) => (


                                <th

                                    key={coluna.key}

                                    scope="col"

                                >


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

                                    colSpan={columns.length || 1}

                                    className="table-empty"

                                >


                                    {emptyMessage}


                                </td>


                            </tr>


                        ) : (


                            data.map((item, index) => (


                                <tr

                                    key={item.id || index}

                                >



                                    {


                                        columns.map((coluna) => (


                                            <td

                                                key={coluna.key}

                                            >


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