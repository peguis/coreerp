import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    ArrowLeft,
    Save
} from "lucide-react";


import financeiroService from "../services/financeiroService";


import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";

import Button from "../components/forms/Button";

import Mensagem from "../components/Mensagem";


import "./NovoLancamento.css";



function NovoLancamento() {


    const navigate = useNavigate();



    const [tipo, setTipo] = useState("RECEITA");

    const [descricao, setDescricao] = useState("");

    const [categoriaId, setCategoriaId] = useState("");

    const [categorias, setCategorias] = useState([]);

    const [valor, setValor] = useState("");

    const [dataVencimento, setDataVencimento] = useState("");

    const [observacoes, setObservacoes] = useState("");



    const [carregando, setCarregando] = useState(false);


    const [mensagem, setMensagem] = useState("");

    const [tipoMensagem, setTipoMensagem] = useState("");





    useEffect(() => {


        document.title = "Novo Lançamento";


        carregarCategorias();


    }, []);







    async function carregarCategorias() {


        try {


            const dados =
                await financeiroService.getCategorias();



            setCategorias(

                Array.isArray(dados)

                    ? dados

                    : []

            );



        } catch (erro) {


            console.error(
                "Erro ao carregar categorias:",
                erro
            );


            setCategorias([]);


        }


    }








    async function salvar(e) {


        e.preventDefault();



        if (

            descricao.trim() === "" ||

            valor === "" ||

            dataVencimento === ""

        ) {


            setTipoMensagem("erro");


            setMensagem(

                "Preencha todos os campos obrigatórios."

            );


            return;


        }








        try {


            setCarregando(true);





            await financeiroService.criarLancamento({



                descricao,


                valor: Number(valor),


                tipo,



                data_vencimento:
                    dataVencimento,



                categoria_id:

                    categoriaId

                        ? Number(categoriaId)

                        : null,



                observacoes



            });






            setTipoMensagem("sucesso");


            setMensagem(

                "Lançamento criado com sucesso."

            );






            setTimeout(() => {


                navigate("/financeiro");


            }, 800);






        } catch (erro) {



            console.error(
                "Erro ao criar lançamento:",
                erro
            );



            setTipoMensagem("erro");



            setMensagem(


                erro.response?.data?.detail ||


                erro.message ||


                "Erro ao salvar lançamento."


            );



        } finally {


            setCarregando(false);


        }


    }









    return (


        <main className="novo-financeiro-page">





            <PageHeader


                titulo="Novo Lançamento"


                subtitulo="Cadastre uma receita ou despesa"


            >



                <Button


                    variant="secondary"


                    onClick={() =>
                        navigate("/financeiro")
                    }


                >



                    <ArrowLeft size={18} />


                    Voltar



                </Button>



            </PageHeader>









            {

                mensagem &&



                <Mensagem


                    tipo={tipoMensagem}


                    texto={mensagem}


                />


            }









            <SectionCard>





                <form onSubmit={salvar}>


                    <div className="financeiro-grid">







                        <div className="campo">


                            <label>

                                Tipo

                            </label>





                            <select


                                value={tipo}


                                onChange={(e) =>
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



                        </div>









                        <div className="campo">


                            <label>

                                Categoria

                            </label>





                            <select


                                value={categoriaId}


                                onChange={(e) =>
                                    setCategoriaId(
                                        e.target.value
                                    )
                                }


                            >



                                <option value="">


                                    Sem categoria


                                </option>






                                {

                                    categorias.map(
                                        categoria => (


                                            <option


                                                key={
                                                    categoria.id
                                                }


                                                value={
                                                    categoria.id
                                                }


                                            >


                                                {
                                                    categoria.nome
                                                }


                                            </option>


                                        )

                                    )

                                }



                            </select>



                        </div>









                        <div className="campo">


                            <label>

                                Descrição

                            </label>





                            <input


                                value={descricao}


                                onChange={(e) =>
                                    setDescricao(
                                        e.target.value
                                    )
                                }


                                placeholder="Descrição do lançamento"


                            />



                        </div>









                        <div className="campo">


                            <label>

                                Valor

                            </label>





                            <input


                                type="number"


                                step="0.01"


                                min="0"


                                value={valor}


                                onChange={(e) =>
                                    setValor(
                                        e.target.value
                                    )
                                }


                                placeholder="0,00"


                            />



                        </div>









                        <div className="campo">


                            <label>

                                Data de Vencimento

                            </label>





                            <input


                                type="date"


                                value={
                                    dataVencimento
                                }


                                onChange={(e) =>
                                    setDataVencimento(
                                        e.target.value
                                    )
                                }


                            />



                        </div>






                    </div>









                    <div className="campo campo-full">



                        <label>


                            Observações


                        </label>







                        <textarea


                            value={observacoes}


                            onChange={(e) =>
                                setObservacoes(
                                    e.target.value
                                )
                            }


                            placeholder="Detalhes adicionais..."


                        />



                    </div>









                    <div className="financeiro-footer-actions">







                        <Button


                            type="button"


                            variant="secondary"


                            onClick={() =>
                                navigate("/financeiro")
                            }


                        >



                            Cancelar



                        </Button>











                        <Button


                            type="submit"


                            variant="primary"


                            disabled={carregando}


                        >



                            <Save size={18} />





                            {

                                carregando

                                    ?

                                    "Salvando..."

                                    :

                                    "Salvar"


                            }





                        </Button>







                    </div>






                </form>





            </SectionCard>






        </main>


    );



}



export default NovoLancamento;