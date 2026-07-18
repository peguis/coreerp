import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Mensagem from "../components/Mensagem";

import { criarCliente } from "../services/clienteService";


function NovoCliente() {

    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [telefone, setTelefone] = useState("");


    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



    async function salvar(e) {

        e.preventDefault();


        try {


            await criarCliente({

                nome,
                email,
                telefone

            });


            setTipo("sucesso");
            setMensagem(
                "Cliente criado com sucesso"
            );


            setTimeout(() => {

                navigate("/clientes");

            }, 1000);



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao criar cliente"
            );



        }


    }



    return (

        <div style={{ display: "flex" }}>




            <main style={{ padding: 30 }}>


                <h1>
                    Novo Cliente
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

                        Salvar

                    </button>



                </form>



            </main>



        </div>

    );

}


export default NovoCliente;