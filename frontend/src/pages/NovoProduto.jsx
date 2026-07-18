import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import { criarProduto } from "../services/produtoService";

function NovoProduto() {

    const navigate = useNavigate();

    const [nome, setNome] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");

    async function salvar() {

        await criarProduto({
            nome,
            preco: Number(preco),
            estoque: Number(estoque),
            ativo: true
        });

        navigate("/produtos");

    }

    return (

        <div style={{ display: "flex" }}>

            <Sidebar />

            <main style={{ padding: 30 }}>

                <h1>Novo Produto</h1>

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