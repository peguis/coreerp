import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    ArrowLeft,
    Save
} from "lucide-react";


import {
    criarProduto
} from "../services/produtoService";


import PageHeader from "../components/ui/PageHeader";
import Button from "../components/forms/Button";
import Mensagem from "../components/Mensagem";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";
import FormCard from "../components/forms/FormCard";

import "../styles/ProdutoForm.css";
import "./NovoProduto.css";





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


        custo_medio: "",

        localizacao: ""

    });




    const [mensagem, setMensagem] = useState("");

    const [tipo, setTipo] = useState("");

    const [salvando, setSalvando] = useState(false);

    const [imagens, setImagens] = useState([]); 
    
    const [preview, setPreview] = useState([]);




    function alterar(e) {


        setForm({

            ...form,

            [e.target.name]:

                e.target.value

        });


    }

    function selecionarImagens(e) {

        const arquivos = Array.from(e.target.files);

        setImagens(arquivos);

        setPreview(

            arquivos.map((arquivo) => ({

                arquivo,

                url: URL.createObjectURL(arquivo)

            }))

        );

    }






    async function salvar(e) {


        e.preventDefault();



        try {


            setSalvando(true);



            await criarProduto({


                ...form,



                preco:

                    form.preco
                        ? Number(form.preco)
                        : 0,



                estoque:

                    form.estoque
                        ? Number(form.estoque)
                        : 0,



                estoque_minimo:

                    form.estoque_minimo
                        ? Number(form.estoque_minimo)
                        : 0,


                estoque_maximo:

                    form.estoque_maximo
                        ? Number(form.estoque_maximo)
                        : 0,



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
                        0,


                localizacao:
                    form.localizacao,


                ativo: true


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



        } finally {



            setSalvando(false);



        }


    }
    return (


        <main className="novo-produto-page">


            <PageHeader

                titulo="Novo Produto"

                subtitulo="Cadastre um novo produto no sistema"


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

                    tipo={tipo}

                    texto={mensagem}

                />

            }






            <form onSubmit={salvar}>



                <FormCard

                    titulo="Informações principais"

                    subtitulo="Dados básicos do produto"

                >





                    <div className="produto-grid">





                        <Input

                            label="Nome"

                            name="nome"

                            value={form.nome}

                            onChange={alterar}

                            required

                        />

                        <Input
                            label="Localização"
                            name="localizacao"
                            value={form.localizacao}
                            onChange={alterar}
                            placeholder="Ex: Prateleira A1"
                        />






                        <Input

                            label="Categoria"

                            name="categoria"

                            value={form.categoria}

                            onChange={alterar}

                        />







                        <Input

                            label="Marca"

                            name="marca"

                            value={form.marca}

                            onChange={alterar}

                        />







                        <Select

                            label="Unidade"

                            name="unidade"

                            value={form.unidade}

                            onChange={alterar}

                            options={[

                                {

                                    value: "UN",

                                    label: "Unidade"

                                },

                                {

                                    value: "KG",

                                    label: "Quilograma"

                                },

                                {

                                    value: "L",

                                    label: "Litro"

                                }

                            ]}

                        />







                        <Input

                            label="Código interno"

                            name="codigo_interno"

                            value={form.codigo_interno}

                            onChange={alterar}

                        />
                        

                        <Input

                            label="Código de barras"

                            name="codigo_barras"

                            value={form.codigo_barras}

                            onChange={alterar}

                        />







                        

                    </div>







                    <Textarea

                        label="Descrição"

                        name="descricao"

                        value={form.descricao}

                        onChange={alterar}

                        rows={4}

                    />



                </FormCard>









                <FormCard
                    titulo="Estoque e valores"
                    subtitulo="Controle financeiro e quantidade disponível"
                >







                    <Input
                        label="Preço"
                        type="number"
                        step="0.01"
                        name="preco"
                        value={form.preco}
                        onChange={alterar}
                    />







                    <Input
                        label="Estoque atual"
                        type="number"
                        name="estoque"
                        value={form.estoque}
                        onChange={alterar}
                    />







                    <Input
                        label="Estoque mínimo"
                        type="number"
                        name="estoque_minimo"
                        value={form.estoque_minimo}
                        onChange={alterar}
                    />







                    <Input
                        label="Estoque máximo"
                        type="number"
                        name="estoque_maximo"
                        value={form.estoque_maximo}
                        onChange={alterar}
                    />







                    <Input
                        label="Custo médio"
                        type="number"
                        step="0.01"
                        name="custo_medio"
                        value={form.custo_medio}
                        onChange={alterar}
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

                        name="peso"

                        value={form.peso}

                        onChange={alterar}

                    />








                    <Input

                        label="Altura"

                        type="number"

                        step="0.01"

                        name="altura"

                        value={form.altura}

                        onChange={alterar}

                    />








                    <Input

                        label="Largura"

                        type="number"

                        step="0.01"

                        name="largura"

                        value={form.largura}

                        onChange={alterar}

                    />








                    <Input

                        label="Comprimento"

                        type="number"

                        step="0.01"

                        name="comprimento"

                        value={form.comprimento}

                        onChange={alterar}

                    />

                </FormCard> 

                <FormCard

                    titulo="Imagens do produto"

                    subtitulo="Adicione uma ou mais imagens para identificação do produto."

                >

                        <div className="imagem-upload">

                            <input
                                type="file"
                                multiple
                                accept="image/*"
                                onChange={selecionarImagens}
                            />

                            {

                                preview.length > 0 && (

                                    <div className="imagem-grid">

                                        {

                                            preview.map((imagem, index) => (

                                                <div
                                                    key={imagem.url}
                                                    className="imagem-card"
                                                >

                                                    <img
                                                        src={imagem.url}
                                                        alt={`Imagem ${index + 1}`}
                                                    />

                                                </div>

                                            ))

                                        }

                                    </div>

                                )

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
                                "Salvando produto..."
                                :
                                "Salvar Produto"
                        }


                        </Button>





                    </div>





            </form>


        </main>


    );


}


export default NovoProduto;
