import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { ArrowLeft } from "lucide-react";

import Mensagem from "../components/Mensagem";
import PageHeader from "../components/ui/PageHeader";

import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Button from "../components/forms/Button";

import {
    buscarCliente,
    atualizarCliente
} from "../services/clienteService";

import "./Clientes.css";


function EditarCliente() {


    const { id } = useParams();

    const navigate = useNavigate();



    const [nome, setNome] = useState("");

    const [email, setEmail] = useState("");

    const [telefone, setTelefone] = useState("");



    const [mensagem, setMensagem] = useState("");

    const [tipo, setTipo] = useState("");



    const [carregando, setCarregando] = useState(true);




    useEffect(() => {

        carregarCliente();

    }, [id]);





    async function carregarCliente() {


        try {


            setCarregando(true);


            const dados = await buscarCliente(id);



            setNome(dados.nome || "");

            setEmail(dados.email || "");

            setTelefone(dados.telefone || "");



        } catch (erro) {


            console.error(
                "Erro ao carregar cliente:",
                erro
            );


            setTipo("erro");

            setMensagem(
                "Erro ao carregar cliente"
            );


        } finally {


            setCarregando(false);


        }


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


            console.error(
                "Erro ao atualizar cliente:",
                erro
            );


            setTipo("erro");


            setMensagem(

                erro.response?.data?.detail ||

                "Erro ao atualizar cliente"

            );


        }


    }






    if (carregando) {


        return (

            <main className="clientes-page">

                <h2>
                    Carregando cliente...
                </h2>

            </main>

        );


    }







    return (



        <main className="clientes-page">



            <PageHeader

                titulo="Editar Cliente"

                subtitulo="Atualize os dados do cliente"

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

                subtitulo="Edite os dados cadastrados"

            >



                <Mensagem

                    tipo={tipo}

                    texto={mensagem}

                />





                <form onSubmit={salvar}>


                    <Input

                        label="Nome"

                        value={nome}

                        onChange={(e) =>

                            setNome(e.target.value)

                        }

                        required

                    />





                    <Input

                        label="Email"

                        type="email"

                        value={email}

                        onChange={(e) =>

                            setEmail(e.target.value)

                        }

                        required

                    />





                    <Input

                        label="Telefone"

                        value={telefone}

                        onChange={(e) =>

                            setTelefone(e.target.value)

                        }

                    />






                    <Button

                        type="submit"

                        variant="primary"

                    >

                        Atualizar Cliente

                    </Button>




                </form>



            </FormCard>




        </main>


    );


}



export default EditarCliente;