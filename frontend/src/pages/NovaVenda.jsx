import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    ArrowLeft,
    Save
} from "lucide-react";

import {
    listarClientes
} from "../services/clienteService";

import {
    listarProdutos
} from "../services/produtoService";

import {
    criarVenda
} from "../services/vendaService";

import PageHeader from "../components/ui/PageHeader";

import FormCard from "../components/forms/FormCard";
import Button from "../components/forms/Button";
import Select from "../components/forms/Select";
import Input from "../components/forms/Input";

import Mensagem from "../components/Mensagem";

import "./NovaVenda.css";

function NovaVenda() {

    const navigate = useNavigate();

    const [clientes, setClientes] = useState([]);
    const [produtos, setProdutos] = useState([]);

    const [clienteId, setClienteId] = useState("");
    const [produtoId, setProdutoId] = useState("");
    const [quantidade, setQuantidade] = useState("");

    const [mensagem, setMensagem] = useState("");
    const [tipo, setTipo] = useState("");

    useEffect(() => {

        carregarDados();

    }, []);

    async function carregarDados() {

        const clientesDados = await listarClientes();
        const produtosDados = await listarProdutos();

        setClientes(
            Array.isArray(clientesDados)
                ? clientesDados
                : []
        );

        setProdutos(
            Array.isArray(produtosDados)
                ? produtosDados
                : []
        );

    }

    async function salvar(e) {

        e.preventDefault();

        if (!clienteId || !produtoId) {

            setTipo("erro");
            setMensagem("Selecione cliente e produto");

            return;

        }

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
            setMensagem("Venda criada com sucesso");

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

        <main className="nova-venda-page">

            <PageHeader

                titulo="Nova Venda"

                subtitulo="Registre uma nova venda"

            >

                <Button

                    variant="secondary"

                    onClick={() => navigate("/vendas")}

                >

                    <ArrowLeft size={18} />

                    Voltar

                </Button>

            </PageHeader>

            <FormCard

                titulo="Dados da Venda"

                subtitulo="Selecione o cliente, produto e quantidade"

            >

                <Mensagem

                    tipo={tipo}

                    texto={mensagem}

                />

                <form

                    className="venda-form"

                    onSubmit={salvar}

                >

                    <Select

                        label="Cliente"

                        value={clienteId}

                        onChange={(e) => setClienteId(e.target.value)}

                        options={[

                            {
                                value: "",
                                label: "Selecione"
                            },

                            ...clientes.map(cliente => ({

                                value: cliente.id,

                                label: cliente.nome

                            }))

                        ]}

                    />

                    <Select

                        label="Produto"

                        value={produtoId}

                        onChange={(e) => setProdutoId(e.target.value)}

                        options={[

                            {
                                value: "",
                                label: "Selecione"
                            },

                            ...produtos.map(produto => ({

                                value: produto.id,

                                label: produto.nome

                            }))

                        ]}

                    />

                    <Input

                        label="Quantidade"

                        type="number"

                        min="1"

                        value={quantidade}

                        onChange={(e) => setQuantidade(e.target.value)}

                    />

                    <Button
                        type="button"
                        variant="secondary"
                        onClick={() => navigate("/vendas")}
                    >
                        Cancelar
                    </Button>

                    <div className="venda-footer-actions">

                        <Button

                            type="submit"

                            variant="primary"

                        >

                            <Save size={18} />

                            Salvar Venda

                        </Button>

                    </div>

                </form>

            </FormCard>

        </main>

    );

}

export default NovaVenda;