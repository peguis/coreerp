import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Sidebar from "../components/Sidebar";

import {
    listarClientes,
    excluirCliente
} from "../services/clienteService";


function Clientes() {


    const [clientes, setClientes] = useState([]);



    useEffect(() => {

        carregarClientes();

    }, []);



    async function carregarClientes() {

        const dados = await listarClientes();

        setClientes(dados);

    }



    async function remover(id) {


        const confirmar = window.confirm(
            "Deseja realmente excluir?"
        );


        if (!confirmar) return;



        await excluirCliente(id);


        carregarClientes();

    }




    return (


        <div style={{ display: "flex" }}>


            <Sidebar />


            <main style={{ padding: 30 }}>


                <h1>Clientes</h1>



                <Link to="/clientes/novo">

                    <button>
                        Novo Cliente
                    </button>

                </Link>



                <br />
                <br />



                <table border="1" cellPadding="10">


                    <thead>


                        <tr>

                            <th>ID</th>

                            <th>Nome</th>

                            <th>Email</th>

                            <th>Telefone</th>

                            <th>Ações</th>

                        </tr>


                    </thead>



                    <tbody>


                        {clientes.map((cliente) => (


                            <tr key={cliente.id}>


                                <td>
                                    {cliente.id}
                                </td>


                                <td>
                                    {cliente.nome}
                                </td>


                                <td>
                                    {cliente.email}
                                </td>


                                <td>
                                    {cliente.telefone}
                                </td>



                                <td>


                                    <Link to={`/clientes/${cliente.id}`}>

                                        <button>
                                            Editar
                                        </button>

                                    </Link>



                                    <button
                                        onClick={() => remover(cliente.id)}
                                    >

                                        Excluir

                                    </button>



                                </td>


                            </tr>


                        ))}



                    </tbody>


                </table>



            </main>


        </div>


    );

}



export default Clientes;