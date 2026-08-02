import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    ArrowLeft
} from "lucide-react";


import {
    criarMovimento
} from "../services/estoqueService";


import {
    listarProdutos
} from "../services/produtoService";


import PageHeader from "../components/ui/PageHeader";


import FormCard from "../components/forms/FormCard";
import Button from "../components/forms/Button";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";


import Mensagem from "../components/Mensagem";


import "./NovoMovimento.css";



function NovoMovimento() {


    const navigate = useNavigate();



    const [produtos, setProdutos] = useState([]);



    const [produtoId, setProdutoId] = useState("");

    const [tipo, setTipo] = useState("ENTRADA");

    const [quantidade, setQuantidade] = useState("");

    const [observacao, setObservacao] = useState("");



    const [mensagem, setMensagem] = useState("");

    const [tipoMensagem, setTipoMensagem] = useState("");





    useEffect(() => {


        carregarProdutos();


    }, []);






    async function carregarProdutos() {


        try {


            const dados = await listarProdutos();



            setProdutos(

                Array.isArray(dados)

                    ? dados

                    : []

            );



        } catch {


            setTipoMensagem("erro");


            setMensagem(

                "Erro ao carregar produtos."

            );


        }


    }







    async function salvar(e) {


        e.preventDefault();




        if (!produtoId || !quantidade) {



            setTipoMensagem("erro");


            setMensagem(

                "Selecione produto e informe quantidade."

            );


            return;


        }








        try {




            await criarMovimento({



                produto_id: Number(produtoId),



                tipo,



                quantidade: Number(quantidade),



                observacao



            });






            setTipoMensagem("sucesso");


            setMensagem(

                "Movimentação criada com sucesso."

            );







            setTimeout(() => {



                navigate("/estoque");



            }, 1000);






        } catch (erro) {



            setTipoMensagem("erro");


            setMensagem(


                erro.response?.data?.detail ||


                "Erro ao criar movimentação."


            );



        }



    }









    return (



        <main className="novo-movimento-page">





            <PageHeader


                titulo="Nova Movimentação"


                subtitulo="Registre entradas, saídas e ajustes de estoque"



            >



                <Button


                    variant="secondary"


                    onClick={() => navigate("/estoque")}



                >



                    <ArrowLeft size={18} />



                    Voltar



                </Button>



            </PageHeader>









            <FormCard


                titulo="Nova Movimentação"


                subtitulo="Controle entradas, saídas e ajustes do estoque"



            >





                {

                    mensagem &&



                    <Mensagem


                        tipo={tipoMensagem}


                        texto={mensagem}



                    />


                }









                <form


                    className="movimento-form"


                    onSubmit={salvar}



                >








                    <Select


                        label="Produto"


                        value={produtoId}


                        onChange={(e) =>

                            setProdutoId(

                                e.target.value

                            )

                        }


                        placeholder="Selecione um produto"


                        options={



                            produtos.map(produto => ({



                                value: produto.id,



                                label:

                                    `${produto.nome} - Estoque: ${produto.estoque}`



                            }))



                        }


                    />











                    <Select


                        label="Tipo"


                        value={tipo}


                        onChange={(e) =>

                            setTipo(

                                e.target.value

                            )

                        }


                        options={[



                            {

                                value: "ENTRADA",

                                label: "Entrada"

                            },



                            {

                                value: "SAIDA",

                                label: "Saída"

                            },



                            {

                                value: "AJUSTE",

                                label: "Ajuste"

                            }



                        ]}



                    />









                    <Input


                        label="Quantidade"


                        type="number"


                        step="0.01"


                        min="0.01"


                        value={quantidade}


                        onChange={(e) =>

                            setQuantidade(

                                e.target.value

                            )

                        }



                    />









                    <Textarea


                        label="Observação"


                        value={observacao}


                        onChange={(e) =>

                            setObservacao(

                                e.target.value

                            )

                        }


                        placeholder="Ex: Compra fornecedor"


                        rows={3}



                    />









                    <div className="movimento-actions">





                        <Button


                            type="button"


                            variant="secondary"


                            onClick={() => navigate("/estoque")}



                        >



                            Cancelar



                        </Button>







                        <Button


                            type="submit"


                            variant="primary"



                        >



                            Salvar Movimentação



                        </Button>






                    </div>







                </form>






            </FormCard>






        </main>



    );


}



export default NovoMovimento;