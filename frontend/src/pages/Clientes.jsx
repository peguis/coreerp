import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    Edit,
    Trash2,
    Plus
} from "lucide-react";

import {
    confirmDelete
} from "../utils/dialog";

import {
    listarClientes,
    excluirCliente
} from "../services/clienteService";

import PageHeader from "../components/ui/PageHeader";
import EmptyState from "../components/ui/EmptyState";
import DataTable from "../components/ui/DataTable";
import SearchInput from "../components/forms/SearchInput";

import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";
import Button from "../components/forms/Button";

import "./Clientes.css";


function Clientes() {


    const [clientes, setClientes] = useState([]);

    const [busca, setBusca] = useState("");

    const [carregando, setCarregando] = useState(true);

    const [erro, setErro] = useState("");




    useEffect(() => {

        carregarClientes();

    }, []);





    async function carregarClientes() {

        try {

            setCarregando(true);
            setErro("");

            const dados = await listarClientes();


            setClientes(

                Array.isArray(dados)

                    ? dados

                    : []

            );


        } catch {

            setErro(
                "Não foi possível carregar clientes."
            );


        } finally {

            setCarregando(false);

        }

    }





    async function remover(id) {


        const confirmar = confirmDelete(
            "Deseja excluir?"
        );


        if (!confirmar) return;



        try {


            await excluirCliente(id);

            carregarClientes();


        } catch {

            setErro(
                "Erro ao excluir cliente."
            );

        }


    }






    const clientesFiltrados = clientes.filter((cliente) => {


        const texto = busca
            .toLowerCase()
            .trim();



        return (

            cliente.nome
                ?.toLowerCase()
                .includes(texto)

            ||

            cliente.email
                ?.toLowerCase()
                .includes(texto)

            ||

            cliente.telefone
                ?.includes(texto)

        );


    });







    const columns = [


        {

            key: "nome",

            title: "Nome"

        },


        {

            key: "email",

            title: "Email"

        },


        {

            key: "telefone",

            title: "Telefone"

        },


        {

            key: "acoes",

            title: "Ações",


            render: (_, cliente) => (


                <div className="table-actions">


                    <Link
                        to={`/clientes/${cliente.id}/editar`}
                    >

                        <Button
                            variant="secondary"
                        >

                            <Edit size={16} />

                            Editar

                        </Button>

                    </Link>



                    <Button

                        variant="danger"

                        onClick={() =>
                            remover(cliente.id)
                        }

                    >

                        <Trash2 size={16} />

                        Excluir

                    </Button>


                </div>


            )

        }


    ];






    return (


        <main className="clientes-page">


            <PageHeader

                titulo="Clientes"

                subtitulo="Gerencie os clientes cadastrados da empresa"


            >


                <Link to="/clientes/novo">


                    <Button variant="primary">


                        <Plus size={18} />

                        Novo Cliente


                    </Button>


                </Link>


            </PageHeader>





            {

                erro && (

                    <Mensagem

                        tipo="erro"

                        texto={erro}

                    />

                )

            }





            <section className="clientes-toolbar">


                <SearchInput

                    value={busca}

                    onChange={(e) =>
                        setBusca(e.target.value)
                    }

                    placeholder="Buscar cliente..."

                />


            </section>






            <section className="clientes-card">



                {

                    carregando ? (


                        <Loading

                            texto="Carregando clientes..."

                        />


                    )


                        :


                        clientesFiltrados.length === 0 ? (


                            <EmptyState

                                titulo="Nenhum cliente encontrado"

                                descricao="Cadastre seu primeiro cliente."

                                icone="👥"

                            />


                        )


                            :


                            (


                                <DataTable

                                    columns={columns}

                                    data={clientesFiltrados}

                                    emptyMessage="Nenhum cliente encontrado."

                                />


                            )


                }



            </section>



        </main>


    );


}


export default Clientes;