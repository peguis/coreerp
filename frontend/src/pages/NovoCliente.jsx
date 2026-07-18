import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

import { criarCliente } from "../services/clienteService";


function NovoCliente() {

    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [telefone, setTelefone] = useState("");



    async function salvar(e) {

        e.preventDefault();


        await criarCliente({
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


                <h1>Novo Cliente</h1>


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
                        Salvar
                    </button>


                </form>


            </main>


        </div>

    );

}


export default NovoCliente;