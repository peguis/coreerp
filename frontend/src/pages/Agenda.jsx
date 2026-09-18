import { useCallback, useEffect, useMemo, useState } from "react";

import { atualizarAgendamento, criarAgendamento, listarAgendamentos, listarRecursosAgenda } from "../services/agendaService";
import { buscarUsuarioLogado, listarUsuarios } from "../services/usuarioService";
import { listarClientes } from "../services/clienteService";
import { listarProfissionais } from "../services/profissionalService";
import { listarServicos } from "../services/servicoService";
import { getErrorMessage } from "../utils/errors";

import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";
import Checkbox from "../components/forms/Checkbox";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Agenda.css";


const FORM_INICIAL = {
    profissional_id: "",
    servico_id: "",
    cliente_id: "",
    cliente_avulso_nome: "",
    recurso_id: "",
    usar_recurso_manual: false,
    inicio_em: "",
    duracao_minutos: "",
    observacao: ""
};


function dataLocalInput(data) {
    const valor = new Date(data);
    const ajuste = valor.getTime() - valor.getTimezoneOffset() * 60000;
    return new Date(ajuste).toISOString().slice(0, 16);
}


function isoLocal(valor) {
    return new Date(valor).toISOString();
}


function dataSelecionadaInicial() {
    return new Date().toISOString().slice(0, 10);
}


function intervaloDoDia(data) {
    const inicio = new Date(`${data}T00:00:00`);
    const fim = new Date(inicio);
    fim.setDate(fim.getDate() + 1);
    return {
        inicio_de: inicio.toISOString(),
        inicio_ate: fim.toISOString()
    };
}


function dataLocalDoAgendamento(valor) {
    const dataAgendamento = new Date(valor);
    const ano = dataAgendamento.getFullYear();
    const mes = String(dataAgendamento.getMonth() + 1).padStart(2, "0");
    const dia = String(dataAgendamento.getDate()).padStart(2, "0");
    return `${ano}-${mes}-${dia}`;
}


function rotuloStatus(status) {
    return {
        AGENDADO: "Agendado",
        CONFIRMADO: "Confirmado",
        CONCLUIDO: "Concluído",
        CANCELADO: "Cancelado",
        NAO_COMPARECEU: "Não compareceu"
    }[status] || status;
}


function nomeProfissional(profissional, usuarios) {
    return usuarios.get(profissional.usuario_id) || `Profissional #${profissional.id}`;
}


function tiposRecursoCompativeis(tipoRecurso, tipoServico) {
    const normalizar = (valor) => String(valor || "").trim().toUpperCase().replace(/\s+/g, " ");
    const recurso = normalizar(tipoRecurso);
    const servico = normalizar(tipoServico);
    return recurso === servico || recurso.startsWith(`${servico} `) || servico.startsWith(`${recurso} `);
}


export default function Agenda() {
    const [usuario, setUsuario] = useState(null);
    const [usuarios, setUsuarios] = useState(new Map());
    const [clientes, setClientes] = useState([]);
    const [profissionais, setProfissionais] = useState([]);
    const [servicos, setServicos] = useState([]);
    const [recursos, setRecursos] = useState([]);
    const [agendamentos, setAgendamentos] = useState([]);
    const [proximosAgendamentos, setProximosAgendamentos] = useState([]);
    const [data, setData] = useState(dataSelecionadaInicial);
    const [form, setForm] = useState(FORM_INICIAL);
    const [editarId, setEditarId] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [carregandoProximos, setCarregandoProximos] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const administrativo = ["admin", "gerente"].includes(usuario?.perfil);
    const servicoSelecionado = servicos.find((item) => String(item.id) === String(form.servico_id));
    const recursosDoServico = recursos.filter((item) => (
        item.ativo && (item.status || "ATIVO") === "ATIVO" && servicoSelecionado?.requer_recurso && tiposRecursoCompativeis(item.tipo, servicoSelecionado.tipo_recurso)
    ));
    const nomesUsuarios = usuarios;

    const carregarBase = useCallback(async () => {
        try {
            const usuarioDados = await buscarUsuarioLogado();
            const [clientesDados, servicosDados, recursosDados] = await Promise.all([
                listarClientes(),
                listarServicos({ ativo: true, pagina: 1, limite: 100 }),
                listarRecursosAgenda({ ativo: true })
            ]);

            setUsuario(usuarioDados);
            setClientes(Array.isArray(clientesDados) ? clientesDados : []);
            setServicos(Array.isArray(servicosDados) ? servicosDados : []);
            setRecursos(Array.isArray(recursosDados) ? recursosDados : []);

            if (["admin", "gerente"].includes(usuarioDados.perfil)) {
                const [profissionaisDados, usuariosDados] = await Promise.all([
                    listarProfissionais({ ativo: true, pagina: 1, limite: 100 }),
                    listarUsuarios()
                ]);
                setProfissionais(Array.isArray(profissionaisDados) ? profissionaisDados : []);
                setUsuarios(new Map((Array.isArray(usuariosDados) ? usuariosDados : []).map((item) => [item.id, item.nome])));
            }
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível carregar os dados da agenda."));
        }
    }, []);

    const carregarAgenda = useCallback(async () => {
        try {
            setCarregando(true);
            setErro("");
            const dados = await listarAgendamentos(intervaloDoDia(data));
            setAgendamentos(Array.isArray(dados) ? dados : []);
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível carregar a agenda."));
        } finally {
            setCarregando(false);
        }
    }, [data]);

    const carregarProximosAgendamentos = useCallback(async () => {
        try {
            setCarregandoProximos(true);
            const dados = await listarAgendamentos({ inicio_de: new Date().toISOString() });
            setProximosAgendamentos(Array.isArray(dados) ? dados : []);
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível carregar a visão geral da agenda."));
        } finally {
            setCarregandoProximos(false);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(() => carregarBase());
    }, [carregarBase]);

    useEffect(() => {
        void Promise.resolve().then(() => carregarAgenda());
    }, [carregarAgenda]);

    useEffect(() => {
        void Promise.resolve().then(() => carregarProximosAgendamentos());
    }, [carregarProximosAgendamentos]);

    function alterar(campo, valor) {
        setForm((atual) => ({ ...atual, [campo]: valor }));
        if (campo === "servico_id") {
            const servico = servicos.find((item) => String(item.id) === String(valor));
            setForm((atual) => ({
                ...atual,
                servico_id: valor,
                duracao_minutos: servico?.duracao_minutos ? String(servico.duracao_minutos) : "",
                recurso_id: "",
                usar_recurso_manual: servico?.modo_selecao_recurso === "MANUAL"
            }));
        }
    }

    function novoAgendamento() {
        setEditarId(null);
        setMensagem("");
        setErro("");
        setForm({
            ...FORM_INICIAL,
            inicio_em: `${data}T10:00`,
            profissional_id: administrativo ? "" : undefined
        });
    }

    function editarAgendamento(item) {
        setEditarId(item.id);
        setMensagem("");
        setErro("");
        setForm({
            profissional_id: item.profissional_id ? String(item.profissional_id) : "",
            servico_id: item.servico_id ? String(item.servico_id) : "",
            cliente_id: item.cliente_id ? String(item.cliente_id) : "",
            cliente_avulso_nome: item.cliente_avulso_nome || "",
            recurso_id: item.recurso_id ? String(item.recurso_id) : "",
            usar_recurso_manual: servicoSelecionado?.modo_selecao_recurso === "MANUAL",
            inicio_em: dataLocalInput(item.inicio_em),
            duracao_minutos: String(item.duracao_minutos || ""),
            observacao: item.observacao || ""
        });
    }

    function podeAlterar(item) {
        return administrativo || item.criado_por_usuario_id === usuario?.id;
    }

    async function salvar(evento) {
        evento.preventDefault();
        if (salvando) return;
        setErro("");
        setMensagem("");
        if (!form.servico_id || !form.inicio_em || !form.duracao_minutos) {
            setErro("Informe serviço, data, horário e duração.");
            return;
        }
        if (administrativo && !form.profissional_id) {
            setErro("Selecione o profissional responsável.");
            return;
        }
        const usarRecursoManual = servicoSelecionado?.requer_recurso && (
            servicoSelecionado.modo_selecao_recurso === "MANUAL" || form.usar_recurso_manual
        );
        if (usarRecursoManual && !form.recurso_id) {
            setErro("Escolha a maca ou recurso deste agendamento.");
            return;
        }

        const dados = {
            servico_id: Number(form.servico_id),
            cliente_id: form.cliente_id ? Number(form.cliente_id) : null,
            cliente_avulso_nome: form.cliente_id ? null : (form.cliente_avulso_nome.trim() || null),
            inicio_em: isoLocal(form.inicio_em),
            duracao_minutos: Number(form.duracao_minutos),
            usar_recurso_manual: Boolean(usarRecursoManual),
            observacao: form.observacao.trim() || null
        };
        if (administrativo) dados.profissional_id = Number(form.profissional_id);
        if (usarRecursoManual) {
            dados.recurso_id = Number(form.recurso_id);
        }

        try {
            setSalvando(true);
            if (editarId) {
                await atualizarAgendamento(editarId, dados);
                setMensagem("Agendamento atualizado com sucesso.");
            } else {
                await criarAgendamento(dados);
                setMensagem("Agendamento criado com sucesso.");
            }
            setEditarId(null);
            setForm(FORM_INICIAL);
            await Promise.all([carregarAgenda(), carregarProximosAgendamentos()]);
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível salvar o agendamento."));
        } finally {
            setSalvando(false);
        }
    }

    async function cancelar(item) {
        if (!window.confirm("Cancelar este agendamento?")) return;
        try {
            setErro("");
            setMensagem("");
            await atualizarAgendamento(item.id, { status: "CANCELADO" });
            setMensagem("Agendamento cancelado. O recurso foi liberado.");
            await Promise.all([carregarAgenda(), carregarProximosAgendamentos()]);
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível cancelar o agendamento."));
        }
    }

    const ordenados = useMemo(() => [...agendamentos].sort((a, b) => new Date(a.inicio_em) - new Date(b.inicio_em)), [agendamentos]);
    const ativos = ordenados.filter((item) => !["CANCELADO", "NAO_COMPARECEU"].includes(item.status));
    const selecionadoManual = servicoSelecionado?.requer_recurso && (
        servicoSelecionado.modo_selecao_recurso === "MANUAL" || form.usar_recurso_manual
    );

    return (
        <main className="agenda-page">
            <PageHeader titulo="Agenda" subtitulo="Organize atendimentos, profissionais e recursos do HYPE.">
                <Button variant="primary" onClick={novoAgendamento}>Novo agendamento</Button>
            </PageHeader>

            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}

            <section className="agenda-toolbar">
                <Input label="Dia da agenda" type="date" value={data} onChange={(evento) => setData(evento.target.value)} />
                <div className="agenda-toolbar-summary">
                    <span>Compromissos do dia</span>
                    <strong>{ativos.length}</strong>
                </div>
                <Button variant="secondary" onClick={() => { void Promise.all([carregarAgenda(), carregarProximosAgendamentos()]); }}>Atualizar</Button>
            </section>

            <FormCard titulo={editarId ? "Editar agendamento" : "Novo agendamento"} subtitulo="A duração vem do serviço e pode ser ajustada para este horário.">
                <form className="agenda-form" onSubmit={salvar}>
                    {administrativo && (
                        <Select
                            label="Profissional"
                            value={form.profissional_id || ""}
                            onChange={(evento) => alterar("profissional_id", evento.target.value)}
                            options={profissionais.map((item) => ({ value: item.id, label: nomeProfissional(item, nomesUsuarios) }))}
                            required
                        />
                    )}
                    <Select
                        label="Serviço"
                        value={form.servico_id}
                        onChange={(evento) => alterar("servico_id", evento.target.value)}
                        options={servicos.map((item) => ({ value: item.id, label: item.nome }))}
                        required
                    />
                    <Input label="Data e horário" type="datetime-local" value={form.inicio_em} onChange={(evento) => alterar("inicio_em", evento.target.value)} required />
                    <Input label="Duração (minutos)" type="number" min="1" max="1440" value={form.duracao_minutos} onChange={(evento) => alterar("duracao_minutos", evento.target.value)} required />
                    <Select
                        label="Cliente cadastrado"
                        value={form.cliente_id}
                        onChange={(evento) => alterar("cliente_id", evento.target.value)}
                        options={clientes.map((item) => ({ value: item.id, label: item.nome }))}
                        placeholder="Cliente avulso"
                    />
                    {!form.cliente_id && <Input label="Nome do cliente avulso" value={form.cliente_avulso_nome} onChange={(evento) => alterar("cliente_avulso_nome", evento.target.value)} placeholder="Opcional" />}
                    {servicoSelecionado?.requer_recurso && (
                        <div className="agenda-resource-choice">
                            <Checkbox
                                label={servicoSelecionado.modo_selecao_recurso === "MANUAL" ? "Selecionar recurso manualmente (obrigatório)" : "Escolher maca ou recurso manualmente"}
                                checked={Boolean(form.usar_recurso_manual || servicoSelecionado.modo_selecao_recurso === "MANUAL")}
                                disabled={servicoSelecionado.modo_selecao_recurso === "MANUAL"}
                                onChange={(evento) => alterar("usar_recurso_manual", evento.target.checked)}
                            />
                            {servicoSelecionado.modo_selecao_recurso !== "MANUAL" && <span>Se desmarcado, o sistema escolherá automaticamente um recurso livre.</span>}
                        </div>
                    )}
                    {selecionadoManual && (
                        <Select
                            label="Maca ou recurso"
                            value={form.recurso_id}
                            onChange={(evento) => alterar("recurso_id", evento.target.value)}
                            options={recursosDoServico.map((item) => ({ value: item.id, label: item.nome }))}
                            placeholder="Selecione o recurso"
                            required
                        />
                    )}
                    {servicoSelecionado?.requer_recurso && !selecionadoManual && (
                        <div className="agenda-auto-note"><strong>Reserva automática</strong><span>O sistema escolherá uma maca livre para este horário.</span></div>
                    )}
                    <Textarea className="agenda-form-full" label="Observação (opcional)" value={form.observacao} onChange={(evento) => alterar("observacao", evento.target.value)} rows={3} />
                    <div className="agenda-form-actions agenda-form-full">
                        {editarId && <Button type="button" variant="secondary" onClick={() => { setEditarId(null); setForm(FORM_INICIAL); }}>Cancelar edição</Button>}
                        <Button type="submit" variant="primary" loading={salvando}>{editarId ? "Salvar alterações" : "Criar agendamento"}</Button>
                    </div>
                </form>
            </FormCard>

            <SectionCard titulo="Visão geral da agenda" subtitulo="Todos os próximos agendamentos aparecem aqui, independentemente do dia selecionado.">
                {carregandoProximos ? <Loading texto="Carregando próximos agendamentos..." /> : proximosAgendamentos.length === 0 ? (
                    <div className="agenda-empty">Nenhum próximo agendamento encontrado.</div>
                ) : (
                    <div className="agenda-list">
                        {proximosAgendamentos.map((item) => {
                            const restrito = item.detalhes_restritos;
                            return (
                                <article className={`agenda-item agenda-overview-item ${restrito ? "agenda-item-restrito" : ""}`} key={`proximo-${item.id}`}>
                                    <div className="agenda-item-time">
                                        <strong>{new Date(item.inicio_em).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" })}</strong>
                                        <span>{new Date(item.inicio_em).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })} · {item.duracao_minutos} min</span>
                                    </div>
                                    <div className="agenda-item-content">
                                        {restrito ? (
                                            <><strong>Recurso reservado</strong><span>{item.recurso_nome || "Recurso ocupado"}</span></>
                                        ) : (
                                            <><strong>{item.servico_id ? servicos.find((servico) => servico.id === item.servico_id)?.nome || "Serviço" : "Serviço"}</strong><span>{item.cliente_nome || item.cliente_avulso_nome || "Cliente avulso"}</span>{administrativo && <small>{item.profissional_id ? nomeProfissional(profissionais.find((profissional) => profissional.id === item.profissional_id) || {}, nomesUsuarios) : "-"}</small>}</>
                                        )}
                                    </div>
                                    <div className="agenda-item-meta">
                                        <span className={`agenda-status agenda-status-${item.status.toLowerCase()}`}>{rotuloStatus(item.status)}</span>
                                        {!restrito && item.recurso_nome && <small>{item.recurso_nome}</small>}
                                        <Button size="small" variant="secondary" onClick={() => setData(dataLocalDoAgendamento(item.inicio_em))}>Ver dia</Button>
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                )}
            </SectionCard>

            <SectionCard titulo="Agenda do dia" subtitulo="Profissionais veem os próprios detalhes e apenas a ocupação dos recursos de terceiros.">
                {carregando ? <Loading texto="Carregando agenda..." /> : ordenados.length === 0 ? (
                    <div className="agenda-empty">Nenhum agendamento para este dia.</div>
                ) : (
                    <div className="agenda-list">
                        {ordenados.map((item) => {
                            const restrito = item.detalhes_restritos;
                            return (
                                <article className={`agenda-item ${restrito ? "agenda-item-restrito" : ""}`} key={item.id}>
                                    <div className="agenda-item-time">
                                        <strong>{new Date(item.inicio_em).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}</strong>
                                        <span>{item.duracao_minutos} min</span>
                                    </div>
                                    <div className="agenda-item-content">
                                        {restrito ? (
                                            <><strong>Recurso reservado</strong><span>{item.recurso_nome || "Recurso ocupado"}</span></>
                                        ) : (
                                            <><strong>{item.servico_id ? servicos.find((servico) => servico.id === item.servico_id)?.nome || "Serviço" : "Serviço"}</strong><span>{item.cliente_nome || item.cliente_avulso_nome || "Cliente avulso"}</span><small>{item.preco_aplicado == null ? "Preço não informado" : `Snapshot: ${Number(item.preco_aplicado).toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}`}</small>{administrativo && <small>{item.profissional_id ? nomeProfissional(profissionais.find((profissional) => profissional.id === item.profissional_id) || {}, nomesUsuarios) : "-"}</small>}</>
                                        )}
                                    </div>
                                    <div className="agenda-item-meta">
                                        <span className={`agenda-status agenda-status-${item.status.toLowerCase()}`}>{rotuloStatus(item.status)}</span>
                                        {!restrito && item.recurso_nome && <small>{item.recurso_nome}</small>}
                                        {!restrito && podeAlterar(item) && item.status !== "CANCELADO" && <div className="agenda-item-actions"><Button size="small" variant="secondary" onClick={() => editarAgendamento(item)}>Editar</Button><Button size="small" variant="danger" onClick={() => cancelar(item)}>Cancelar</Button></div>}
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                )}
            </SectionCard>

        </main>
    );
}
