import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { ArrowLeft } from "lucide-react";

import Mensagem from "../components/Mensagem";

import PageHeader from "../components/ui/PageHeader";

import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Button from "../components/forms/Button";


import {
    criarCliente
} from "../services/clienteService";


import "./Clientes.css";



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


        <main className="clientes-page">


            <PageHeader

                titulo="Novo Cliente"

                subtitulo="Cadastre um novo cliente"

            />



            <div className="form-actions">


                <Button

                    variant="secondary"

                    onClick={() => navigate("/clientes")}

                >

                    <ArrowLeft size={18} />

                    Voltar

                </Button>


            </div>




            <FormCard
                titulo="Informações do cliente"
                subtitulo="Preencha os dados para cadastrar um novo cliente"
            >


                <Mensagem

                    tipo={tipo}

                    texto={mensagem}

                />



                <form onSubmit={salvar}>


                    <Input

                        label="Nome"

                        value={nome}

                        onChange={
                            e => setNome(e.target.value)
                        }

                    />



                    <Input

                        label="Email"

                        type="email"

                        value={email}

                        onChange={
                            e => setEmail(e.target.value)
                        }

                    />



                    <Input

                        label="Telefone"

                        value={telefone}

                        onChange={
                            e => setTelefone(e.target.value)
                        }

                    />



                    <Button
                        type="submit"
                        variant="primary"
                    >
                        Salvar Cliente
                    </Button>


                </form>



            </FormCard>



        </main>


    );


}


export default NovoCliente;