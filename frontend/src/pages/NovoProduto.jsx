import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    criarProduto
} from "../services/produtoService";

import Mensagem from "../components/Mensagem";


function NovoProduto() {


    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



    async function salvar(e) {


        e.preventDefault();


        try {


            await criarProduto({

                nome,
                preco: Number(preco),
                estoque: Number(estoque)

            });



            setTipo("sucesso");

            setMensagem(
                "Produto criado com sucesso"
            );



            setTimeout(() => {

                navigate("/produtos");

            }, 1000);



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao criar produto"
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


                <input
                    placeholder="Nome"
                    value={nome}
                    onChange={
                        e => setNome(e.target.value)
                    }
                />



                <br />
                <br />



                <input
                    placeholder="Preço"
                    type="number"
                    value={preco}
                    onChange={
                        e => setPreco(e.target.value)
                    }
                />



                <br />
                <br />



                <input
                    placeholder="Estoque"
                    type="number"
                    value={estoque}
                    onChange={
                        e => setEstoque(e.target.value)
                    }
                />



                <br />
                <br />



                <button type="submit">
                    Salvar
                </button>


            </form>


        </main>


    );


}


export default NovoProduto;