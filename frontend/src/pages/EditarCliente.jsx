import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    buscarCliente,
    atualizarCliente
} from "../services/clienteService";

import Mensagem from "../components/Mensagem";


function EditarCliente() {


    const { id } = useParams();

    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [telefone, setTelefone] = useState("");


    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



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


        try {


            await atualizarCliente(id, {


                nome,

                email,

                telefone


            });



            setTipo("sucesso");

            setMensagem(
                "Cliente atualizado com sucesso"
            );



            setTimeout(() => {

                navigate("/clientes");

            }, 1000);



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao atualizar cliente"
            );


        }


    }



    return (


        <main style={{ padding: 30 }}>


            <h1>
                Editar Cliente
            </h1>



            <Mensagem
                tipo={tipo}
                texto={mensagem}
            />



            <form onSubmit={salvar}>


                <div>

                    <label>
                        Nome:
                    </label>

                    <br />

                    <input

                        value={nome}

                        onChange={
                            (e) =>
                                setNome(e.target.value)
                        }

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

                        onChange={
                            (e) =>
                                setEmail(e.target.value)
                        }

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

                        onChange={
                            (e) =>
                                setTelefone(e.target.value)
                        }

                    />

                </div>



                <br />



                <button type="submit">

                    Atualizar

                </button>



            </form>



        </main>


    );


}


export default EditarCliente;