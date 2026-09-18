import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    ArrowLeft,
    CircleDollarSign,
    CreditCard,
    Save,
    StickyNote,
    UserRound
} from "lucide-react";

import {
    buscarUsuarioLogado,
    listarUsuarios
} from "../services/usuarioService";
import { listarClientes } from "../services/clienteService";
import { listarProfissionais } from "../services/profissionalService";
import { listarServicos } from "../services/servicoService";
import { criarAtendimento } from "../services/atendimentoService";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import Button from "../components/forms/Button";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./NovoAtendimento.css";


const PERFIS_COM_OVERRIDE = ["admin", "gerente"];


const FORMAS_PAGAMENTO = [
    { value: "PIX", label: "PIX" },
    { value: "DINHEIRO", label: "Dinheiro" },
    { value: "CARTAO_DEBITO", label: "Cartão de débito" },
    { value: "CARTAO_CREDITO", label: "Cartão de crédito" }
];


function NovoAtendimento() {

    const navigate = useNavigate();

    const [usuario, setUsuario] = useState(null);
    const [clientes, setClientes] = useState([]);
    const [profissionais, setProfissionais] = useState([]);
    const [servicos, setServicos] = useState([]);
    const [usuarios, setUsuarios] = useState([]);

    const [profissionalId, setProfissionalId] = useState("");
    const [servicoId, setServicoId] = useState("");
    const [clienteId, setClienteId] = useState("");
    const [valor, setValor] = useState("");
    const [formaPagamento, setFormaPagamento] = useState("");
    const [percentualOverride, setPercentualOverride] = useState("");
    const [observacao, setObservacao] = useState("");

    const [carregandoDados, setCarregandoDados] = useState(true);
    const [carregando, setCarregando] = useState(false);
    const [mensagem, setMensagem] = useState("");
    const [tipoMensagem, setTipoMensagem] = useState("");

    const podeUsarOverride = PERFIS_COM_OVERRIDE.includes(usuario?.perfil);
    const ehProfissional = usuario?.perfil === "profissional";
    const rotaVoltar = ehProfissional ? "/inicio" : "/dashboard";

    const carregarDados = useCallback(async () => {

        try {

            const usuarioDados = await buscarUsuarioLogado();
            const [clientesDados, servicosDados] = await Promise.all([
                listarClientes(),
                listarServicos({ ativo: true, pagina: 1, limite: 100 })
            ]);

            setUsuario(usuarioDados);
            setClientes(Array.isArray(clientesDados) ? clientesDados : []);
            setServicos(Array.isArray(servicosDados) ? servicosDados : []);

            if (PERFIS_COM_OVERRIDE.includes(usuarioDados.perfil)) {

                const [profissionaisDados, usuariosDados] = await Promise.all([
                    listarProfissionais({
                        ativo: true,
                        pagina: 1,
                        limite: 100
                    }),
                    listarUsuarios()
                ]);

                setProfissionais(
                    Array.isArray(profissionaisDados)
                        ? profissionaisDados
                        : []
                );
                setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);

            }

        } catch (erro) {

            setTipoMensagem("erro");
            setMensagem(
                erro.response?.data?.detail ||
                "Não foi possível carregar os dados do atendimento."
            );

        } finally {

            setCarregandoDados(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregarDados);

    }, [carregarDados]);

    function montarPayload() {

        const dados = {
            servico_id: Number(servicoId),
            cliente_id: clienteId ? Number(clienteId) : null,
            valor: Number(valor),
            forma_pagamento: formaPagamento,
            observacao: observacao.trim() || null
        };

        if (!ehProfissional) {

            dados.profissional_id = Number(profissionalId);

        }

        if (podeUsarOverride && percentualOverride.trim() !== "") {

            dados.percentual_profissional_override = Number(
                percentualOverride
            );

        }

        return dados;

    }

    function selecionarServico(evento) {

        const id = evento.target.value;
        setServicoId(id);

        if (valor !== "") return;

        const servico = servicos.find((item) => String(item.id) === id);
        if (servico) setValor(String(servico.preco_padrao));

    }

    async function salvar(evento) {

        evento.preventDefault();
        if (carregando) return;
        setMensagem("");

        if (!usuario || ![...PERFIS_COM_OVERRIDE, "profissional"].includes(usuario.perfil)) {

            setTipoMensagem("erro");
            setMensagem("Seu perfil não possui permissão para registrar atendimentos.");
            return;

        }

        if (!servicoId || !valor || !formaPagamento) {

            setTipoMensagem("erro");
            setMensagem("Preencha serviço, valor e forma de pagamento.");
            return;

        }

        if (!ehProfissional && !profissionalId) {

            setTipoMensagem("erro");
            setMensagem("Selecione o profissional responsável.");
            return;

        }

        if (
            podeUsarOverride
            && percentualOverride.trim() !== ""
            && (
                Number.isNaN(Number(percentualOverride))
                || Number(percentualOverride) < 0
                || Number(percentualOverride) > 100
            )
        ) {

            setTipoMensagem("erro");
            setMensagem("A comissão excepcional deve estar entre 0 e 100.");
            return;

        }

        try {

            setCarregando(true);
            await criarAtendimento(montarPayload());

            setTipoMensagem("sucesso");
            setMensagem("Atendimento registrado com sucesso.");
            setValor("");
            setFormaPagamento("");
            setPercentualOverride("");
            setObservacao("");
            setClienteId("");

        } catch (erro) {

            setTipoMensagem("erro");
            setMensagem(
                erro.response?.data?.detail ||
                "Erro ao registrar atendimento."
            );

        } finally {

            setCarregando(false);

        }

    }

    return (

        <main className="novo-atendimento-page">

            <PageHeader
                titulo="Novo Atendimento"
                subtitulo="Registre um serviço realizado na barbearia ou no estúdio de tattoo"
            >
                <Button
                    variant="secondary"
                    disabled={carregandoDados || !usuario}
                    onClick={() => navigate(rotaVoltar)}
                >
                    <ArrowLeft size={18} />
                    Voltar
                </Button>
            </PageHeader>

            <FormCard
                className="novo-atendimento-card"
                titulo="Dados do atendimento"
                subtitulo="A comissão é definida pelo backend e fica registrada no atendimento"
            >

                <Mensagem
                    tipo={tipoMensagem}
                    texto={mensagem}
                />

                {carregandoDados ? (

                    <Loading texto="Carregando dados do atendimento..." />

                ) : (

                    <form
                        className="atendimento-form"
                        onSubmit={salvar}
                    >
                        <section className="atendimento-form-section">
                            <header className="atendimento-section-heading">
                                <UserRound size={18} aria-hidden="true" />
                                <div><strong>Responsável e serviço</strong><span>Identifique quem realizou o atendimento e o serviço concluído.</span></div>
                            </header>

                            <div className="atendimento-form-grid">
                                {!ehProfissional && (
                                    <Select
                                        label="Profissional responsável"
                                        value={profissionalId}
                                        onChange={(evento) => setProfissionalId(evento.target.value)}
                                        options={profissionais.map((profissional) => ({
                                            value: profissional.id,
                                            label: `${usuarios.find((item) => item.id === profissional.usuario_id)?.nome || `Profissional #${profissional.id}`} — ${profissional.area_atuacao}`
                                        }))}
                                        required
                                    />
                                )}

                                <Select
                                    label="Serviço"
                                    value={servicoId}
                                    onChange={selecionarServico}
                                    options={servicos.map((servico) => ({
                                        value: servico.id,
                                        label: `${servico.nome} — preço padrão ${Number(servico.preco_padrao).toFixed(2)}`
                                    }))}
                                    required
                                />

                                <Select
                                    className="atendimento-field-full"
                                    label="Cliente (opcional)"
                                    value={clienteId}
                                    onChange={(evento) => setClienteId(evento.target.value)}
                                    options={clientes.map((cliente) => ({
                                        value: cliente.id,
                                        label: cliente.nome
                                    }))}
                                />
                            </div>
                        </section>

                        <section className="atendimento-form-section">
                            <header className="atendimento-section-heading">
                                <CreditCard size={18} aria-hidden="true" />
                                <div><strong>Pagamento e comissão</strong><span>O valor informado entra no caixa com a forma de pagamento selecionada.</span></div>
                            </header>

                            <div className="atendimento-form-grid">
                                <Input
                                    label="Valor do atendimento"
                                    type="number"
                                    min="0.01"
                                    step="0.01"
                                    value={valor}
                                    onChange={(evento) => setValor(evento.target.value)}
                                    placeholder="0,00"
                                    required
                                />

                                <Select
                                    label="Forma de pagamento"
                                    value={formaPagamento}
                                    onChange={(evento) => setFormaPagamento(evento.target.value)}
                                    options={FORMAS_PAGAMENTO}
                                    required
                                />

                                {podeUsarOverride && (
                                    <div className="comissao-excepcional atendimento-field-full">
                                        <div className="comissao-excepcional-heading"><CircleDollarSign size={18} aria-hidden="true" /><strong>Comissão excepcional</strong></div>
                                        <Input
                                            label="Percentual opcional"
                                            type="number"
                                            min="0"
                                            max="100"
                                            step="0.01"
                                            value={percentualOverride}
                                            onChange={(evento) => setPercentualOverride(evento.target.value)}
                                            placeholder="Ex.: 80,00"
                                        />
                                        <p>Se ficar vazio, será usada a comissão padrão do profissional. Este percentual vale somente para este atendimento e não altera o cadastro.</p>
                                    </div>
                                )}
                            </div>
                        </section>

                        <section className="atendimento-form-section">
                            <header className="atendimento-section-heading">
                                <StickyNote size={18} aria-hidden="true" />
                                <div><strong>Observações</strong><span>Registre apenas informações úteis para a operação.</span></div>
                            </header>

                            <Textarea
                                label="Observação (opcional)"
                                value={observacao}
                                onChange={(evento) => setObservacao(evento.target.value)}
                                placeholder="Detalhes adicionais do atendimento"
                                rows={4}
                            />
                        </section>

                        <div className="atendimento-footer-actions">

                            <Button
                                type="button"
                                variant="secondary"
                                disabled={carregandoDados || !usuario}
                                onClick={() => navigate(rotaVoltar)}
                            >
                                Cancelar
                            </Button>

                            <Button
                                type="submit"
                                variant="primary"
                                disabled={carregando || carregandoDados}
                            >
                                <Save size={18} />
                                {carregando ? "Salvando..." : "Registrar Atendimento"}
                            </Button>

                        </div>

                    </form>

                )}

            </FormCard>

        </main>

    );

}


export default NovoAtendimento;
