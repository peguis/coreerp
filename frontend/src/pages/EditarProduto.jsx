import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Sidebar from "../components/Sidebar";

import {
    buscarProduto,
    atualizarProduto
} from "../services/produtoService";

function EditarProduto() {

    const { id } = useParams();

    const navigate = useNavigate();

    const [nome, setNome] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");

    useEffect(() => {

        carregarProduto();

    }, []);

    async function carregarProduto() {

        const produto = await buscarProduto(id);

        setNome(produto.nome);
        setPreco(produto.preco);
        setEstoque(produto.estoque);

    }

    async function salvar() {

        await atualizarProduto(id, {

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

                <h1>Editar Produto</h1>

                <input
                    value={nome}
                    onChange={e => setNome(e.target.value)}
                />

                <br /><br />

                <input
                    value={preco}
                    onChange={e => setPreco(e.target.value)}
                />

                <br /><br />

                <input
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

export default EditarProduto;