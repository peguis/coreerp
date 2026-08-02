import { useEffect, useState } from "react";

import {
    Plus,
    Trash2,
    X
} from "lucide-react";


import financeiroService from "../../services/financeiroService";


import Button from "../forms/Button";
import Mensagem from "../Mensagem";
import DataTable from "../ui/DataTable";
import Badge from "../Badge";



function CategoriasFinanceiras() {


    const [categorias, setCategorias] = useState([]);


    const [mostrarForm, setMostrarForm] = useState(false);


    const [nome, setNome] = useState("");

    const [tipo, setTipo] = useState("DESPESA");


    const [erro, setErro] = useState("");

    const [mensagem, setMensagem] = useState("");



    useEffect(() => {

        carregarCategorias();

    }, []);






    async function carregarCategorias() {


        try {


            setErro("");


            const dados =

                await financeiroService.getCategorias();



            setCategorias(

                Array.isArray(dados)

                    ? dados

                    : []

            );



        } catch {


            setErro(
                "Erro ao carregar categorias."
            );


        }


    }









    async function salvarCategoria() {



        if (!nome.trim()) {


            setErro(
                "Informe o nome da categoria."
            );


            return;


        }





        try {


            await financeiroService.criarCategoria({

                nome: nome.trim(),

                tipo

            });





            setNome("");

            setTipo("DESPESA");


            setMostrarForm(false);



            setMensagem(
                "Categoria criada com sucesso."
            );



            carregarCategorias();




        } catch {


            setErro(
                "Erro ao criar categoria."
            );


        }


    }









    async function excluirCategoria(id) {



        const confirmar = window.confirm(

            "Deseja desativar esta categoria?"

        );



        if (!confirmar)

            return;






        try {



            await financeiroService.excluirCategoria(id);





            setMensagem(

                "Categoria desativada com sucesso."

            );



            carregarCategorias();




        } catch {



            setErro(

                "Erro ao desativar categoria."

            );


        }


    }









    const colunas = [



        {

            key: "nome",

            title: "Nome"

        },



        {

            key: "tipo",

            title: "Tipo",

            render: valor => (


                <Badge

                    tipo={

                        valor === "RECEITA"

                            ? "success"

                            : "danger"

                    }

                >

                    {

                        valor === "RECEITA"

                            ? "Receita"

                            : "Despesa"

                    }


                </Badge>


            )

        },





        {

            key: "ativo",

            title: "Status",

            render: valor => (


                <Badge

                    tipo={

                        valor

                            ? "success"

                            : "warning"

                    }

                >

                    {

                        valor

                            ? "Ativa"

                            : "Inativa"

                    }


                </Badge>


            )

        },





        {

            key: "acoes",

            title: "Ações",

            render: (_, item) => (


                <Button

                    variant="danger"

                    onClick={() =>

                        excluirCategoria(item.id)

                    }

                >

                    <Trash2 size={16} />

                </Button>


            )

        }



    ];









    return (


        <div className="categorias-financeiras">





            <div

                style={{

                    display: "flex",

                    justifyContent: "space-between",

                    alignItems: "center",

                    marginBottom: "20px"

                }}

            >



                <div>


                    <h2>

                        Categorias Financeiras

                    </h2>


                    <p>

                        Organize receitas e despesas da empresa.

                    </p>


                </div>






                <Button

                    variant="primary"

                    onClick={() =>

                        setMostrarForm(!mostrarForm)

                    }

                >


                    {

                        mostrarForm

                            ?

                            <X size={18} />

                            :

                            <Plus size={18} />

                    }


                    {

                        mostrarForm

                            ?

                            "Cancelar"

                            :

                            "Nova Categoria"

                    }



                </Button>



            </div>







            {

                erro &&

                <Mensagem

                    tipo="erro"

                    texto={erro}

                />

            }






            {

                mensagem &&

                <Mensagem

                    tipo="sucesso"

                    texto={mensagem}

                />

            }









            {

                mostrarForm &&

                (

                    <div

                        style={{

                            display: "flex",

                            gap: "10px",

                            marginBottom: "20px"

                        }}

                    >



                        <input

                            placeholder="Nome da categoria"

                            value={nome}

                            onChange={e =>

                                setNome(

                                    e.target.value

                                )

                            }

                        />





                        <select

                            value={tipo}

                            onChange={e =>

                                setTipo(

                                    e.target.value

                                )

                            }

                        >

                            <option value="RECEITA">

                                Receita

                            </option>


                            <option value="DESPESA">

                                Despesa

                            </option>


                        </select>






                        <Button

                            variant="success"

                            onClick={salvarCategoria}

                        >

                            Salvar

                        </Button>



                    </div>

                )

            }









            <DataTable

                columns={colunas}

                data={categorias}

            />





        </div>


    );


}


export default CategoriasFinanceiras;