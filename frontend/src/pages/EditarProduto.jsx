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

    const [preview, setPreview] = useState(null);

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");

    const [enviandoImagem, setEnviandoImagem] = useState(false);



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

        try {

            const resposta = await api.get(
                `/produtos/${id}/imagens`
            );

            setImagens(
                resposta.data
            );


        } catch {

            setImagens([]);

        }

    }





    function selecionarImagem(e) {


        const imagem =
            e.target.files[0];


        if (!imagem)
            return;



        if (!imagem.type.startsWith("image")) {

            setTipo("erro");

            setMensagem(
                "Selecione apenas imagens."
            );

            return;

        }



        if (imagem.size > 5 * 1024 * 1024) {

            setTipo("erro");

            setMensagem(
                "Imagem deve ter no máximo 5MB."
            );

            return;

        }



        setArquivo(imagem);


        setPreview(
            URL.createObjectURL(imagem)
        );


    }





    async function enviarImagem() {


        if (!arquivo)
            return;



        const formData = new FormData();


        formData.append(
            "arquivo",
            arquivo
        );



        try {


            setEnviandoImagem(true);



            await api.post(

                `/produtos/${id}/imagem`,

                formData,

                {

                    headers: {
                        "Content-Type":
                            "multipart/form-data"
                    }

                }

            );



            setArquivo(null);

            setPreview(null);


            setTipo("sucesso");

            setMensagem(
                "Imagem enviada."
            );



            carregarImagens();



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao enviar imagem."
            );


        } finally {


            setEnviandoImagem(false);


        }


    }






    async function excluirImagem(imagemId) {


        const confirmar =
            window.confirm(
                "Excluir imagem?"
            );


        if (!confirmar)
            return;



        await api.delete(
            `/produtos/${id}/imagem/${imagemId}`
        );



        setTipo("sucesso");

        setMensagem(
            "Imagem removida."
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

                estoque_minimo: Number(estoque_minimo),

                estoque_maximo: Number(estoque_maximo),

                ativo: true

            });



            setTipo("sucesso");

            setMensagem(
                "Produto atualizado."
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

                accept="image/*"

                onChange={selecionarImagem}

            />



            {
                preview &&

                <div>

                    <p>
                        Preview:
                    </p>


                    <img

                        src={preview}

                        width="150"

                        height="150"

                        style={{
                            objectFit: "cover"
                        }}

                    />


                </div>

            }



            <button

                type="button"

                disabled={
                    !arquivo || enviandoImagem
                }

                onClick={enviarImagem}

            >

                {
                    enviandoImagem
                        ?
                        "Enviando..."
                        :
                        "Enviar Imagem"
                }


            </button>





            <hr />




            <div style={{
                display: "flex",
                gap: 20,
                flexWrap: "wrap"
            }}>


                {
                    imagens.map(imagem => (


                        <div key={imagem.id}>


                            <img

                                src={
                                    `http://127.0.0.1:8000/${imagem.caminho}`
                                }

                                width="120"

                                height="120"

                                style={{
                                    objectFit: "cover"
                                }}

                            />


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
                    onChange={e => setNome(e.target.value)}
                />

                <br /><br />


                <input
                    placeholder="Categoria"
                    value={categoria}
                    onChange={e => setCategoria(e.target.value)}
                />


                <br /><br />


                <input
                    placeholder="Marca"
                    value={marca}
                    onChange={e => setMarca(e.target.value)}
                />

                <br /><br />


                <textarea

                    placeholder="Descrição"

                    value={descricao}

                    onChange={e => setDescricao(e.target.value)}

                />


                <br /><br />


                <input

                    type="number"

                    step="0.01"

                    value={preco}

                    onChange={e => setPreco(e.target.value)}

                />


                <br /><br />


                <input

                    type="number"

                    value={estoque}

                    onChange={e => setEstoque(e.target.value)}

                />


                <br /><br />


                <button>
                    Salvar
                </button>



            </form>


        </main>

    );

}


export default EditarProduto;