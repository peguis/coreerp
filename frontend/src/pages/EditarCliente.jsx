import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Sidebar from "../components/Sidebar";

import {
    buscarCliente,
    atualizarCliente
} from "../services/clienteService";


function EditarCliente() {

    const { id } = useParams();

    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [telefone, setTelefone] = useState("");



    useEffect(() => {

        carregarCliente();

    }, []);



    async function carregarCliente() {

        const dados = await buscarCliente(id);


        setNome(dados.nome);
        setEmail(dados.email);
        setTelefone(dados.telefone);

    }



    async function salvar(e) {

        e.preventDefault();


        await atualizarCliente(id, {

            nome,
            email,
            telefone

        });


        navigate("/clientes");

    }



    return (

        <div style={{ display: "flex" }}>

            <Sidebar />


            <main style={{ padding: 30 }}>


                <h1>Editar Cliente</h1>


                <form onSubmit={salvar}>


                    <div>

                        <label>
                            Nome:
                        </label>

                        <br />

                        <input
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                        />

                    </div>


                    <br />


                    <div>

                        <label>
                            Email:
                        </label>

                        <br />

                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />

                    </div>


                    <br />


                    <div>

                        <label>
                            Telefone:
                        </label>

                        <br />

                        <input
                            value={telefone}
                            onChange={(e) => setTelefone(e.target.value)}
                        />

                    </div>


                    <br />


                    <button type="submit">
                        Atualizar
                    </button>


                </form>


            </main>


        </div>

    );

}


export default EditarCliente;