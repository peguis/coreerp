import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    ArrowLeft,
    Save,
    Upload,
    Trash2
} from "lucide-react";

import {

    confirmDelete

} from "../utils/dialog";


import {
    buscarProduto,
    atualizarProduto
} from "../services/produtoService";


import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import Button from "../components/forms/Button";
import Mensagem from "../components/Mensagem";
import Loading from "../components/Loading";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";

import "../styles/ProdutoForm.css";
import "./EditarProduto.css";


import api from "../services/api";


import "./EditarProduto.css";



function EditarProduto() {


    const { id } = useParams();

    const navigate = useNavigate();



    const [carregando, setCarregando] = useState(true);



    const [nome, setNome] = useState("");

    const [categoria, setCategoria] = useState("");

    const [codigoInterno, setCodigoInterno] = useState("");

    const [codigoBarras, setCodigoBarras] = useState("");

    const [marca, setMarca] = useState("");

    const [unidade, setUnidade] = useState("UN");

    const [descricao, setDescricao] = useState("");



    const [preco, setPreco] = useState("");

    const [estoque, setEstoque] = useState("");

    const [estoqueMinimo, setEstoqueMinimo] = useState("");

    const [estoqueMaximo, setEstoqueMaximo] = useState("");



    const [peso, setPeso] = useState("");

    const [altura, setAltura] = useState("");

    const [largura, setLargura] = useState("");

    const [comprimento, setComprimento] = useState("");



    const [custoMedio, setCustoMedio] = useState("");



    const [imagens, setImagens] = useState([]);



    const [arquivo, setArquivo] = useState(null);

    const [preview, setPreview] = useState(null);



    const [enviandoImagem, setEnviandoImagem] = useState(false);
    const [salvando, setSalvando] = useState(false);



    const [mensagem, setMensagem] = useState("");

    const [tipoMensagem, setTipoMensagem] = useState("");







    useEffect(() => {


        carregarProduto();

        carregarImagens();


    }, []);







    async function carregarProduto() {


        try {


            setCarregando(true);



            const produto = await buscarProduto(id);



            setNome(produto.nome || "");

            setCategoria(produto.categoria || "");

            setCodigoInterno(
                produto.codigo_interno || ""
            );

            setCodigoBarras(
                produto.codigo_barras || ""
            );


            setMarca(produto.marca || "");

            setUnidade(produto.unidade || "UN");

            setDescricao(
                produto.descricao || ""
            );



            setPreco(produto.preco || "");

            setEstoque(produto.estoque || "");

            setEstoqueMinimo(
                produto.estoque_minimo || ""
            );

            setEstoqueMaximo(
                produto.estoque_maximo || ""
            );



            setPeso(produto.peso || "");

            setAltura(produto.altura || "");

            setLargura(produto.largura || "");

            setComprimento(produto.comprimento || "");



            setCustoMedio(
                produto.custo_medio || ""
            );



        } catch {


            mostrarMensagem(
                "Erro ao carregar produto.",
                "erro"
            );


        } finally {


            setCarregando(false);


        }


    }







    async function carregarImagens() {


        try {


            const resposta = await api.get(
                `/produtos/${id}/imagens`
            );


            setImagens(
                resposta.data || []
            );


        } catch {


            setImagens([]);


        }


    }







    function mostrarMensagem(texto, tipo) {


        setMensagem(texto);

        setTipoMensagem(tipo);


    }

    function selecionarImagem(e) {


        const imagem = e.target.files[0];


        if (!imagem)
            return;



        if (!imagem.type.startsWith("image")) {


            mostrarMensagem(
                "Selecione apenas arquivos de imagem.",
                "erro"
            );


            return;


        }




        if (imagem.size > 5 * 1024 * 1024) {


            mostrarMensagem(
                "A imagem deve ter no máximo 5MB.",
                "erro"
            );


            return;


        }

        if (preview) {

            URL.revokeObjectURL(preview);

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



            mostrarMensagem(
                "Imagem enviada com sucesso.",
                "sucesso"
            );



            carregarImagens();



        } catch (erro) {


            mostrarMensagem(

                erro.response?.data?.detail
                ||
                "Erro ao enviar imagem.",

                "erro"

            );



        } finally {


            setEnviandoImagem(false);


        }


    }








    async function removerImagem(imagemId) {


        const confirmar =

            confirmDelete(

                "Deseja excluir?"

        );



        if (!confirmar)
            return;





        try {


            await api.delete(
                `/produtos/${id}/imagem/${imagemId}`
            );



            mostrarMensagem(
                "Imagem removida.",
                "sucesso"
            );



            carregarImagens();



        } catch {


            mostrarMensagem(
                "Erro ao remover imagem.",
                "erro"
            );


        }


    }








    async function salvar(e) {



        e.preventDefault();


        try {


            setSalvando(true);


            await atualizarProduto(

                id,

                {


                    nome,

                    categoria,


                    codigo_interno:
                        codigoInterno,


                    codigo_barras:
                        codigoBarras,


                    marca,


                    unidade,


                    descricao,



                    preco:
                        Number(preco),



                    estoque:
                        Number(estoque),



                    estoque_minimo:
                        Number(estoqueMinimo),



                    estoque_maximo:
                        Number(estoqueMaximo),



                    peso:
                        Number(peso || 0),



                    altura:
                        Number(altura || 0),



                    largura:
                        Number(largura || 0),



                    comprimento:
                        Number(comprimento || 0),



                    custo_medio:
                        Number(custoMedio || 0),



                    ativo: true


                }


            );




            mostrarMensagem(
                "Produto atualizado com sucesso.",
                "sucesso"
            );




            setTimeout(() => {


                navigate("/produtos");


            }, 1200);




        } catch (erro) {


            mostrarMensagem(

                erro.response?.data?.detail
                ||
                "Erro ao atualizar produto.",

                "erro"

            );


        } finally {


            setSalvando(false);


        }


    }








    if (carregando) {


        return (

            <main className="editar-produto-page">

                <Loading />

            </main>

        );


    }

    return (

        <main className="editar-produto-page">


            <PageHeader

                titulo="Editar Produto"

                subtitulo="Atualize os dados e informações do produto"

            >

                <Button

                    variant="secondary"

                    onClick={() =>
                        navigate("/produtos")
                    }

                >

                    <ArrowLeft size={18} />

                    Voltar

                </Button>


            </PageHeader>





            {
                mensagem &&


                <Mensagem

                    tipo={tipoMensagem}

                    texto={mensagem}

                />

            }







            <form onSubmit={salvar}>


                <FormCard

                    titulo="Informações principais"

                    subtitulo="Dados básicos do produto"

                >





                    <Input
                        label="Nome"
                        value={nome}
                        onChange={(e) => setNome(e.target.value)}
                        required
                    />





                    <Input
                        label="Categoria"
                        value={categoria}
                        onChange={(e) => setCategoria(e.target.value)}
                    />






                    <Input
                        label="Marca"
                        value={marca}
                        onChange={(e) => setMarca(e.target.value)}
                    />






                    <Select
                        label="Unidade"
                        value={unidade}
                        onChange={(e) => setUnidade(e.target.value)}
                        options={[
                            { value: "UN", label: "Unidade" },
                            { value: "KG", label: "Quilograma" },
                            { value: "L", label: "Litro" }
                        ]}
                    />





                    <Input
                        label="Código interno"
                        value={codigoInterno}
                        onChange={(e) => setCodigoInterno(e.target.value)}
                    />






                    <Input
                        label="Código de barras"
                        value={codigoBarras}
                        onChange={(e) => setCodigoBarras(e.target.value)}
                    />



                    





                    <Textarea
                        label="Descrição"
                        value={descricao}
                        onChange={(e) => setDescricao(e.target.value)}
                        rows={4}
                    />



                </FormCard>








                <FormCard

                    titulo="Imagens do produto"

                    subtitulo="Adicione fotos para identificação"

                >






                    <Input

                        label="Preço"

                        type="number"

                        step="0.01"

                        value={preco}

                        onChange={(e) => setPreco(e.target.value)}

                    />





                    <Input

                        label="Estoque atual"

                        type="number"

                        value={estoque}

                        onChange={(e) => setEstoque(e.target.value)}

                    />






                    <Input

                        label="Estoque mínimo"

                        type="number"

                        value={estoqueMinimo}

                        onChange={(e) => setEstoqueMinimo(e.target.value)}

                    />






                    <Input

                        label="Estoque máximo"

                        type="number"

                        value={estoqueMaximo}

                        onChange={(e) => setEstoqueMaximo(e.target.value)}

                    />





                    <Input

                        label="Custo médio"

                        type="number"

                        step="0.01"

                        value={custoMedio}

                        onChange={(e) => setCustoMedio(e.target.value)}

                    />



                    


                </FormCard>

                <FormCard
                    titulo="Dimensões do produto"
                    subtitulo="Informações físicas para logística"
                >






                    <Input
                        label="Peso"
                        type="number"
                        step="0.01"
                        value={peso}
                        onChange={(e) => setPeso(e.target.value)}
                    />






                    <Input
                        label="Altura"
                        type="number"
                        step="0.01"
                        value={altura}
                        onChange={(e) => setAltura(e.target.value)}
                    />
                    






                    <Input
                        label="Largura"
                        type="number"
                        step="0.01"
                        value={largura}
                        onChange={(e) => setLargura(e.target.value)}
                    />






                    <Input
                        label="Comprimento"
                        type="number"
                        step="0.01"
                        value={comprimento}
                        onChange={(e) => setComprimento(e.target.value)}
                    />



                    



            </FormCard>









                <FormCard
                    titulo="Imagens do produto"
                    subtitulo="Adicione fotos para identificação"
                >







                    <div className="imagem-upload">



                        <input

                            type="file"

                            accept="image/*"

                            onChange={
                                selecionarImagem
                            }

                        />



                        {
                            preview &&


                            <div className="imagem-preview">


                                <img

                                    src={preview}

                                    alt="Preview"

                                />


                            </div>


                        }






                        <Button


                            type="button"

                            disabled={
                                !arquivo ||
                                enviandoImagem
                            }

                            onClick={
                                enviarImagem
                            }


                        >


                            <Upload size={18} />



                            {
                                enviandoImagem

                                    ?

                                    "Enviando..."

                                    :

                                    "Enviar imagem"

                            }



                        </Button>



                    </div>









                    <div className="imagem-grid">



                        {
                            imagens.map(imagem => (


                                <div

                                    className="imagem-card"

                                    key={imagem.id}

                                >



                                    <img

                                        src={
                                            `${api.defaults.baseURL}/${imagem.caminho}`
                                        }

                                        alt="Produto"

                                    />





                                    <Button

                                        type="button"

                                        variant="danger"

                                        onClick={() =>
                                            removerImagem(
                                                imagem.id
                                            )
                                        }

                                    >


                                        <Trash2 size={16} />


                                        Excluir


                                    </Button>



                                </div>



                            ))
                        }



                    </div>



                </FormCard>








                <div className="produto-footer-actions">



                    <Button

                        type="button"

                        variant="secondary"

                        onClick={() =>
                            navigate("/produtos")
                        }

                    >


                        Cancelar


                    </Button>






                    <Button

                        type="submit"

                        variant="primary"

                        disabled={salvando}

                    >


                        <Save size={18} />


                        {
                            salvando

                                ?

                                "Salvando..."

                                :

                                "Salvar Produto"

                        }



                    </Button>



                </div>






            </form>



        </main>


    );


}



export default EditarProduto;