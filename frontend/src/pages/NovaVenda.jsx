import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


import { listarClientes } from "../services/clienteService";
import { listarProdutos } from "../services/produtoService";
import { criarVenda } from "../services/vendaService";
import Mensagem from "../components/Mensagem";


function NovaVenda() {


    const navigate = useNavigate();


    const [clientes, setClientes] = useState([]);
    const [produtos, setProdutos] = useState([]);


    const [clienteId, setClienteId] = useState("");
    const [produtoId, setProdutoId] = useState("");
    const [quantidade, setQuantidade] = useState(1);
    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");



    useEffect(() => {

        carregarDados();

    }, []);



    async function carregarDados() {

        const clientesDados = await listarClientes();

        const produtosDados = await listarProdutos();


        setClientes(clientesDados);

        setProdutos(produtosDados);

    }



    async function salvar(e) {

        e.preventDefault();


        try {


            await criarVenda({

                cliente_id: Number(clienteId),

                itens: [

                    {
                        produto_id: Number(produtoId),
                        quantidade: Number(quantidade)
                    }

                ]

            });



            setTipo("sucesso");

            setMensagem(
                "Venda criada com sucesso"
            );



            setTimeout(() => {

                navigate("/vendas");

            }, 1000);



        } catch (erro) {


            setTipo("erro");

            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao criar venda"
            );


        }


    }



    return (

        <div style={{ display: "flex" }}>




            <main style={{ padding: 30 }}>


                <h1>Nova Venda</h1>

                <Mensagem
                    tipo={tipo}
                    texto={mensagem}
                />


                <form onSubmit={salvar}>


                    <label>
                        Cliente:
                    </label>


                    <br />


                    <select
                        value={clienteId}
                        onChange={(e) => setClienteId(e.target.value)}
                    >

                        <option value="">
                            Selecione
                        </option>


                        {
                            clientes.map(cliente => (

                                <option
                                    key={cliente.id}
                                    value={cliente.id}
                                >

                                    {cliente.nome}

                                </option>

                            ))
                        }


                    </select>



                    <br /><br />



                    <label>
                        Produto:
                    </label>


                    <br />


                    <select
                        value={produtoId}
                        onChange={(e) => setProdutoId(e.target.value)}
                    >


                        <option value="">
                            Selecione
                        </option>


                        {
                            produtos.map(produto => (

                                <option
                                    key={produto.id}
                                    value={produto.id}
                                >

                                    {produto.nome}

                                </option>

                            ))

                        }


                    </select>



                    <br /><br />


                    <label>
                        Quantidade:
                    </label>


                    <br />


                    <input

                        type="number"

                        value={quantidade}

                        onChange={(e) => setQuantidade(e.target.value)}

                    />



                    <br /><br />



                    <button type="submit">

                        Salvar Venda

                    </button>



                </form>


            </main>


        </div>

    );


}


export default NovaVenda;