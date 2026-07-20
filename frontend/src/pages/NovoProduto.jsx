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
    const [categoria, setCategoria] = useState("");
    const [codigoInterno, setCodigoInterno] = useState("");
    const [codigoBarras, setCodigoBarras] = useState("");
    const [marca, setMarca] = useState("");
    const [unidade, setUnidade] = useState("UN");
    const [descricao, setDescricao] = useState("");
    const [estoque_minimo, setEstoqueMinimo] = useState("");
    const [estoque_maximo, setEstoqueMaximo] = useState("");



    async function salvar(e) {


        e.preventDefault();


        try {


            await criarProduto({

                nome,
                categoria,
                codigo_interno: codigoInterno,
                codigo_barras: codigoBarras,
                marca,
                unidade,
                descricao,
                
                preco: Number(preco),
                estoque: Number(estoque),
                estoque_minimo: Number(estoque_minimo),
                estoque_maximo: Number(estoque_maximo),

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
                    placeholder="Categoria"
                    value={categoria}
                    onChange={e => setCategoria(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Código Interno"
                    value={codigoInterno}
                    onChange={e => setCodigoInterno(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Código de Barras"
                    value={codigoBarras}
                    onChange={e => setCodigoBarras(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Marca"
                    value={marca}
                    onChange={e => setMarca(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Unidade"
                    value={unidade}
                    onChange={e => setUnidade(e.target.value)}
                />

                <br /><br />

                <textarea
                    placeholder="Descrição"
                    value={descricao}
                    onChange={e => setDescricao(e.target.value)}
                />

                <br /><br />

                <input
                    placeholder="Estoque Mínimo"
                    type="number"
                    value={estoque_minimo}
                    onChange={(e) => setEstoqueMinimo(e.target.value)}
                />

                <br />
                <br />

                <input
                    placeholder="Estoque Máximo"
                    type="number"
                    value={estoque_maximo}
                    onChange={(e) => setEstoqueMaximo(e.target.value)}
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