import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    criarMovimento
} from "../services/estoqueService";


import {
    listarProdutos
} from "../services/produtoService";


import Mensagem from "../components/Mensagem";



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

        const dados = await listarProdutos();

        setProdutos(dados);

    }







    async function salvar(e) {


        e.preventDefault();



        if (!produtoId || !quantidade) {


            setTipoMensagem("erro");

            setMensagem(
                "Selecione produto e informe quantidade"
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
                "Movimentação criada com sucesso"
            );



            setTimeout(() => {


                navigate("/estoque");


            }, 1000);




        } catch (erro) {


            setTipoMensagem("erro");


            setMensagem(

                erro.response?.data?.detail ||

                "Erro ao criar movimentação"

            );


        }


    }







    return (


        <main style={{ padding: 30 }}>


            <h1>
                Nova Movimentação
            </h1>



            <Mensagem

                tipo={tipoMensagem}

                texto={mensagem}

            />





            <form onSubmit={salvar}>



                <label>
                    Produto
                </label>



                <br />



                <select


                    value={produtoId}


                    onChange={
                        e =>
                            setProdutoId(e.target.value)
                    }


                >


                    <option value="">
                        Selecione um produto
                    </option>



                    {
                        produtos.map(produto => (


                            <option

                                key={produto.id}

                                value={produto.id}

                            >

                                {produto.nome}

                                {" - Estoque: "}

                                {produto.estoque}


                            </option>


                        ))
                    }



                </select>





                <br /><br />





                <label>
                    Tipo
                </label>



                <br />



                <select


                    value={tipo}


                    onChange={
                        e =>
                            setTipo(e.target.value)
                    }


                >


                    <option value="ENTRADA">
                        Entrada
                    </option>


                    <option value="SAIDA">
                        Saída
                    </option>


                    <option value="AJUSTE">
                        Ajuste
                    </option>



                </select>





                <br /><br />





                <label>
                    Quantidade
                </label>



                <br />



                <input


                    type="number"

                    step="0.01"

                    min="0.01"


                    value={quantidade}


                    onChange={
                        e =>
                            setQuantidade(e.target.value)
                    }


                />





                <br /><br />





                <label>
                    Observação
                </label>



                <br />



                <input


                    value={observacao}


                    onChange={
                        e =>
                            setObservacao(e.target.value)
                    }


                />





                <br /><br />





                <button type="submit">

                    Salvar

                </button>




            </form>




        </main>


    );


}



export default NovoMovimento;