import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    ArrowLeft,
    Save
} from "lucide-react";

import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import Button from "../components/forms/Button";
import Mensagem from "../components/Mensagem";
import Loading from "../components/Loading";

import financeiroService from "../services/financeiroService";

import "./NovoLancamento.css";


function EditarLancamento() {


    const {
        id
    } = useParams();


    const navigate = useNavigate();



    const [formData, setFormData] = useState({

        descricao: "",

        valor: "",

        tipo: "RECEITA",

        categoria_id: "",

        data_vencimento: "",

        status: "PENDENTE",

        observacoes: ""

    });



    const [categorias, setCategorias] = useState([]);



    const [loading, setLoading] = useState(true);


    const [salvando, setSalvando] = useState(false);



    const [mensagem, setMensagem] = useState(null);





    useEffect(() => {


        carregarDados();


    }, []);





    async function carregarDados() {


        try {


            const [

                lancamento,

                listaCategorias

            ] = await Promise.all([


                financeiroService.getLancamentoPorId(id),


                financeiroService.getCategorias()


            ]);




            setFormData({


                descricao:
                    lancamento.descricao || "",



                valor:
                    lancamento.valor || "",



                tipo:
                    lancamento.tipo || "RECEITA",



                categoria_id:
                    lancamento.categoria_id || "",



                data_vencimento:
                    lancamento.data_vencimento || "",



                status:
                    lancamento.status || "PENDENTE",



                observacoes:
                    lancamento.observacoes || ""

            });



            setCategorias(

                listaCategorias || []

            );



        } catch (erro) {


            console.log(
                "ERRO ATUALIZAR:",
                erro
            );


            setMensagem({

                tipo: "erro",

                texto:
                    erro.message ||
                    "Erro ao atualizar lançamento."

            });



        } finally {


            setLoading(false);


        }


    }





    function handleChange(e) {


        const {

            name,

            value

        } = e.target;



        setFormData((prev) => ({


            ...prev,


            [name]: value


        }));


    }





    async function salvar(e) {


        e.preventDefault();



        try {


            setSalvando(true);



            await financeiroService.atualizarLancamento(

                id,

                {

                    ...formData,

                    valor:
                        Number(formData.valor),

                    categoria_id:
                        formData.categoria_id
                            ? Number(formData.categoria_id)
                            : null

                }

            );



            setMensagem({

                tipo: "sucesso",

                texto:
                    "Lançamento atualizado com sucesso."

            });



            setTimeout(() => {


                navigate("/financeiro");


            }, 800);



        } catch (erro) {


            console.log(
                "ERRO ATUALIZAR:",
                erro
            );


            setMensagem({

                tipo: "erro",

                texto:
                    erro.message ||
                    "Erro ao atualizar lançamento."

            });



        } finally {


            setSalvando(false);


        }


    }





    if (loading) {


        return <Loading />;


    }

    return (

        <main className="novo-financeiro-page">


            <PageHeader

                titulo="Editar Lançamento"

                subtitulo="Atualize os dados financeiros."

            >

                <Button

                    variant="secondary"

                    onClick={() => navigate("/financeiro")}

                >

                    <ArrowLeft size={18} />

                    Voltar

                </Button>


            </PageHeader>




            {

                mensagem &&

                <Mensagem

                    tipo={mensagem.tipo}

                    texto={mensagem.texto}

                    onClose={() => setMensagem(null)}

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

                                name="tipo"

                                value={formData.tipo}

                                onChange={handleChange}

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

                                name="categoria_id"

                                value={formData.categoria_id}

                                onChange={handleChange}

                            >


                                <option value="">

                                    Selecione

                                </option>


                                {

                                    categorias.map((categoria) => (


                                        <option

                                            key={categoria.id}

                                            value={categoria.id}

                                        >

                                            {categoria.nome}

                                        </option>


                                    ))

                                }


                            </select>


                        </div>





                        <div className="campo">


                            <label>

                                Descrição

                            </label>


                            <input


                                name="descricao"


                                value={formData.descricao}


                                onChange={handleChange}


                            />


                        </div>





                        <div className="campo">


                            <label>

                                Valor

                            </label>


                            <input


                                type="number"


                                step="0.01"


                                name="valor"


                                value={formData.valor}


                                onChange={handleChange}


                            />


                        </div>





                        <div className="campo">


                            <label>

                                Data de Vencimento

                            </label>


                            <input


                                type="date"


                                name="data_vencimento"


                                value={formData.data_vencimento}


                                onChange={handleChange}


                            />


                        </div>





                        <div className="campo">


                            <label>

                                Status

                            </label>


                            <select


                                name="status"


                                value={formData.status}


                                onChange={handleChange}


                            >


                                <option value="PENDENTE">

                                    Pendente

                                </option>


                                <option value="PAGO">

                                    Pago

                                </option>


                            </select>


                        </div>


                    </div>






                    <div className="campo campo-full">


                        <label>

                            Observações

                        </label>


                        <textarea


                            name="observacoes"


                            value={formData.observacoes}


                            onChange={handleChange}


                            rows="4"


                        />


                    </div>







                    <div className="financeiro-footer-actions">


                        <Button


                            type="button"


                            variant="secondary"


                            onClick={() => navigate("/financeiro")}


                        >

                            Cancelar

                        </Button>





                        <Button


                            type="submit"


                            variant="primary"


                            disabled={salvando}


                        >


                            <Save size={18} />


                            {


                                salvando

                                    ?

                                    "Salvando..."

                                    :

                                    "Salvar Alterações"


                            }


                        </Button>



                    </div>



                </form>



            </SectionCard>



        </main>


    );


}


export default EditarLancamento;