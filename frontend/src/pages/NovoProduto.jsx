import { useState } from "react";
import { useNavigate } from "react-router-dom";


import { criarProduto } from "../services/produtoService";
import Mensagem from "../components/Mensagem";

function NovoProduto() {

    const navigate = useNavigate();

    const [nome, setNome] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");
    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");

    async function salvar() {

        try {

            await criarProduto({

                nome,
                preco,
                estoque

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

        <div style={{ display: "flex" }}>


            <main style={{ padding: 30 }}>

                <h1>Novo Produto</h1>

                <Mensagem
                    tipo={tipo}
                    texto={mensagem}
                />

                <input
                    placeholder="Nome"
                    value={nome}
                    onChange={e => setNome(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Preço"
                    value={preco}
                    onChange={e => setPreco(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Estoque"
                    value={estoque}
                    onChange={e => setEstoque(e.target.value)}
                />

                <br /><br />

                <button onClick={salvar}>
                    Salvar
                </button>

            </main>

        </div>

    );

}

export default NovoProduto;