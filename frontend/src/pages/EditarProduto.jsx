import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    buscarProduto,
    atualizarProduto
} from "../services/produtoService";

import Mensagem from "../components/Mensagem";

import api from "../api/axios";


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

    const [estoque_minimo, setEstoqueMinimo] = useState("");
    const [estoque_maximo, setEstoqueMaximo] = useState("");

    const [imagens, setImagens] = useState([]);
    const [arquivo, setArquivo] = useState(null);

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



    useEffect(() => {

        carregarProduto();
        carregarImagens();

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
            setMensagem(
                "Erro ao carregar produto."
            );

        }

    }



    async function carregarImagens() {

        const resposta = await api.get(
            `/produtos/${id}/imagens`
        );


        setImagens(resposta.data);

    }




    async function enviarImagem() {


        if (!arquivo)
            return;


        const formData = new FormData();


        formData.append(
            "arquivo",
            arquivo
        );


        await api.post(
            `/produtos/${id}/imagem`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }
        );


        setArquivo(null);

        carregarImagens();

    }




    async function excluirImagem(imagemId) {


        const confirmar = window.confirm(
            "Excluir imagem?"
        );


        if (!confirmar)
            return;



        await api.delete(
            `/produtos/${id}/imagem/${imagemId}`
        );


        carregarImagens();

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

                estoque_minimo:
                    Number(estoque_minimo),

                estoque_maximo:
                    Number(estoque_maximo),

                ativo: true

            });



            setTipo("sucesso");

            setMensagem(
                "Produto atualizado com sucesso."
            );



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


            <h1>
                Editar Produto
            </h1>



            <Mensagem
                tipo={tipo}
                texto={mensagem}
            />



            <h2>
                Imagens
            </h2>



            <input
                type="file"
                onChange={
                    e => setArquivo(e.target.files[0])
                }
            />


            <button
                type="button"
                onClick={enviarImagem}
            >
                Enviar Imagem
            </button>



            <br /><br />



            <div
                style={{
                    display: "flex",
                    gap: 20
                }}
            >


                {

                    imagens.length === 0

                        ?

                        <p>
                            Sem imagens
                        </p>


                        :


                        imagens.map(imagem => (


                            <div key={imagem.id}>


                                <img

                                    src={
                                        `http://127.0.0.1:8000/${imagem.caminho}`
                                    }

                                    width="120"

                                    height="120"

                                    style={{
                                        objectFit: "cover",
                                        borderRadius: 10
                                    }}

                                />


                                <br />


                                {

                                    imagem.principal &&

                                    <strong>
                                        Principal
                                    </strong>

                                }



                                <br />


                                <button

                                    type="button"

                                    onClick={() =>
                                        excluirImagem(imagem.id)
                                    }

                                >

                                    Excluir

                                </button>



                            </div>


                        ))

                }


            </div>



            <hr />




            <form onSubmit={salvar}>


                <input
                    placeholder="Nome"
                    value={nome}
                    onChange={
                        e => setNome(e.target.value)
                    }
                />


                <br /><br />


                <input
                    placeholder="Categoria"
                    value={categoria}
                    onChange={
                        e => setCategoria(e.target.value)
                    }
                />


                <br /><br />


                <input
                    placeholder="Código Interno"
                    value={codigo_interno}
                    onChange={
                        e => setCodigoInterno(e.target.value)
                    }
                />


                <br /><br />


                <input
                    placeholder="Código Barras"
                    value={codigo_barras}
                    onChange={
                        e => setCodigoBarras(e.target.value)
                    }
                />


                <br /><br />


                <input
                    placeholder="Marca"
                    value={marca}
                    onChange={
                        e => setMarca(e.target.value)
                    }
                />


                <br /><br />


                <input
                    placeholder="Unidade"
                    value={unidade}
                    onChange={
                        e => setUnidade(e.target.value)
                    }
                />


                <br /><br />


                <textarea

                    placeholder="Descrição"

                    value={descricao}

                    onChange={
                        e => setDescricao(e.target.value)
                    }

                />


                <br /><br />


                <input

                    type="number"

                    step="0.01"

                    placeholder="Preço"

                    value={preco}

                    onChange={
                        e => setPreco(e.target.value)
                    }

                />


                <br /><br />


                <input

                    type="number"

                    placeholder="Estoque"

                    value={estoque}

                    onChange={
                        e => setEstoque(e.target.value)
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


export default EditarProduto;