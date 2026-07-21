import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    criarProduto
} from "../services/produtoService";

import Mensagem from "../components/Mensagem";


function NovoProduto() {


    const navigate = useNavigate();


    const [form, setForm] = useState({

        nome: "",
        categoria: "",
        codigo_interno: "",
        codigo_barras: "",
        marca: "",
        unidade: "UN",
        descricao: "",
        preco: "",
        estoque: "",
        estoque_minimo: "",
        estoque_maximo: "",
        peso: "",
        altura: "",
        largura: "",
        comprimento: "",
        localizacao: "",
        custo_medio: ""

    });



    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");





    function alterar(e) {


        setForm({

            ...form,

            [e.target.name]:
                e.target.value

        });


    }






    async function salvar(e) {


        e.preventDefault();



        try {


            await criarProduto({

                ...form,

                preco: Number(form.preco),

                estoque: Number(form.estoque),

                estoque_minimo: Number(form.estoque_minimo),

                estoque_maximo: Number(form.estoque_maximo),

                peso:
                    form.peso
                        ?
                        Number(form.peso)
                        :
                        null,

                altura:
                    form.altura
                        ?
                        Number(form.altura)
                        :
                        null,

                largura:
                    form.largura
                        ?
                        Number(form.largura)
                        :
                        null,

                comprimento:
                    form.comprimento
                        ?
                        Number(form.comprimento)
                        :
                        null,

                custo_medio:
                    form.custo_medio
                        ?
                        Number(form.custo_medio)
                        :
                        0

            });



            setTipo("sucesso");

            setMensagem(
                "Produto criado com sucesso."
            );



            setTimeout(() => {

                navigate("/produtos");

            }, 1000);




        } catch (erro) {


            setTipo("erro");

            setMensagem(

                erro.response?.data?.detail ||

                "Erro ao criar produto."

            );


        }


    }






    return (


        <main style={{ padding: 30 }}>


            <h1>
                Novo Produto
            </h1>



            <Mensagem

                tipo={tipo}

                texto={mensagem}

            />





            <form onSubmit={salvar}>


                {
                    [

                        ["nome", "Nome"],

                        ["categoria", "Categoria"],

                        ["codigo_interno", "Código Interno"],

                        ["codigo_barras", "Código Barras"],

                        ["marca", "Marca"],

                        ["unidade", "Unidade"],

                        ["localizacao", "Localização"],

                        ["preco", "Preço"],

                        ["estoque", "Estoque"],

                        ["estoque_minimo", "Estoque Mínimo"],

                        ["estoque_maximo", "Estoque Máximo"],

                        ["peso", "Peso"],

                        ["altura", "Altura"],

                        ["largura", "Largura"],

                        ["comprimento", "Comprimento"],

                        ["custo_medio", "Custo Médio"]

                    ]

                        .map(campo => (


                            <div key={campo[0]}>


                                <input

                                    name={campo[0]}

                                    placeholder={campo[1]}

                                    value={form[campo[0]]}

                                    type={
                                        [
                                            "preco",
                                            "estoque",
                                            "estoque_minimo",
                                            "estoque_maximo",
                                            "peso",
                                            "altura",
                                            "largura",
                                            "comprimento",
                                            "custo_medio"

                                        ].includes(campo[0])

                                            ?

                                            "number"

                                            :

                                            "text"

                                    }

                                    step="0.01"

                                    onChange={alterar}

                                />


                                <br /><br />


                            </div>


                        ))

                }





                <textarea

                    name="descricao"

                    placeholder="Descrição"

                    value={form.descricao}

                    onChange={alterar}

                />



                <br /><br />




                <button type="submit">

                    Salvar

                </button>



            </form>


        </main>


    );


}


export default NovoProduto;