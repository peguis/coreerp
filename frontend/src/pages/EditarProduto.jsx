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
    const [categoria, setCategoria] = useState("");
    const [codigo_interno, setCodigoInterno] = useState("");
    const [codigo_barras, setCodigoBarras] = useState("");
    const [marca, setMarca] = useState("");
    const [unidade, setUnidade] = useState("");
    const [descricao, setDescricao] = useState("");
    const [preco, setPreco] = useState("");
    const [estoque, setEstoque] = useState("");

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");
    const [estoque_minimo, setEstoqueMinimo] = useState("");
    const [estoque_maximo, setEstoqueMaximo] = useState("");

    useEffect(() => {
        carregarProduto();
    }, []);

    async function carregarProduto() {

        try {

            const produto = await buscarProduto(id);

            setNome(produto.nome || "");
            setCategoria(produto.categoria || "");
            setCodigoInterno(produto.codigo_interno || "");
            setCodigoBarras(produto.codigo_barras || "");
            setMarca(produto.marca || "");
            setUnidade(produto.unidade || "UN");
            setDescricao(produto.descricao || "");
            setPreco(produto.preco || 0);
            setEstoque(produto.estoque || 0);
            setEstoqueMinimo(produto.estoque_minimo || 0);
            setEstoqueMaximo(produto.estoque_maximo || 0);

        } catch {

            setTipo("erro");
            setMensagem("Erro ao carregar produto.");

        }

    }

    async function salvar(e) {

        e.preventDefault();

        try {

            await atualizarProduto(id, {
                nome,
                categoria,
                codigo_interno,
                codigo_barras,
                marca,
                unidade,
                descricao,
                preco: Number(preco),
                estoque: Number(estoque),
                ativo: true,
                estoque_minimo: Number(estoque_minimo),
                estoque_maximo: Number(estoque_maximo),
            });

            setTipo("sucesso");
            setMensagem("Produto atualizado com sucesso.");

            setTimeout(() => {
                navigate("/produtos");
            }, 1000);

        } catch (erro) {

            setTipo("erro");
            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao atualizar produto."
            );

        }

    }

    return (

        <main style={{ padding: 30 }}>

            <h1>Editar Produto</h1>

            <Mensagem
                tipo={tipo}
                texto={mensagem}
            />

            <form onSubmit={salvar}>

                <input
                    placeholder="Nome"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Categoria"
                    value={categoria}
                    onChange={(e) => setCategoria(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Código Interno"
                    value={codigo_interno}
                    onChange={(e) => setCodigoInterno(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Código de Barras"
                    value={codigo_barras}
                    onChange={(e) => setCodigoBarras(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Marca"
                    value={marca}
                    onChange={(e) => setMarca(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Unidade"
                    value={unidade}
                    onChange={(e) => setUnidade(e.target.value)}
                />

                <br /><br />

                <textarea
                    placeholder="Descrição"
                    value={descricao}
                    onChange={(e) => setDescricao(e.target.value)}
                    rows={4}
                />

                <br /><br />

                <input
                    type="number"
                    step="0.01"
                    placeholder="Preço"
                    value={preco}
                    onChange={(e) => setPreco(e.target.value)}
                />

                <br /><br />

                <input
                    type="number"
                    placeholder="Estoque"
                    value={estoque}
                    onChange={(e) => setEstoque(e.target.value)}
                />

                <br /><br />

                <button type="submit">
                    Salvar
                </button>

            </form>

        </main>

    );

}

export default EditarProduto;