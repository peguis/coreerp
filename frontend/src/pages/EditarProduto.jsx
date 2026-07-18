import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    buscarProduto,
    atualizarProduto
} from "../services/produtoService";

import Mensagem from "../components/Mensagem";


function EditarProduto() {


    const { id } = useParams();

    const navigate = useNavigate();


    const [nome, setNome] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



    useEffect(() => {

        carregarProduto();

    }, []);



    async function carregarProduto() {


        const produto = await buscarProduto(id);


        setNome(produto.nome);
        setPreco(produto.preco);
        setEstoque(produto.estoque);


    }



    async function salvar(e) {


        e.preventDefault();


        try {


            await atualizarProduto(id, {


                nome,

                preco: Number(preco),

                estoque: Number(estoque),

                ativo: true


            });



            setTipo("sucesso");

            setMensagem(
                "Produto atualizado com sucesso"
            );



            setTimeout(() => {

                navigate("/produtos");

            }, 1000);



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao atualizar produto"
            );


        }


    }



    return (


        <main style={{ padding: 30 }}>


            <h1>
                Editar Produto
            </h1>



            <Mensagem
                tipo={tipo}
                texto={mensagem}
            />



            <form onSubmit={salvar}>


                <input

                    value={nome}

                    onChange={
                        e => setNome(e.target.value)
                    }

                />



                <br />
                <br />



                <input

                    type="number"

                    value={preco}

                    onChange={
                        e => setPreco(e.target.value)
                    }

                />



                <br />
                <br />



                <input

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


export default EditarProduto;