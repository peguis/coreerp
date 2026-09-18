import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { CalendarDays, CalendarPlus, ChevronLeft, ChevronRight, Clock3, RefreshCw, Scissors, UserRound, Wrench } from "lucide-react";

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
    preco_aplicado: "",
    inicio_em: "",
    duracao_minutos: "",
    observacao: ""
};

const TONS_DO_CALENDARIO = [
    "agenda-calendar-tone-blue",
    "agenda-calendar-tone-gold",
    "agenda-calendar-tone-green",
    "agenda-calendar-tone-violet"
];


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


function servicoEhTattoo(servico) {
    const texto = `${servico?.categoria || ""} ${servico?.nome || ""}`.toUpperCase();
    return ["TATTOO", "TATOO", "TATUAGEM"].some((marca) => texto.includes(marca));
}


function servicoCompativelComArea(servico, area) {
    if (!area) return true;
    return area === "TATTOO" ? servicoEhTattoo(servico) : !servicoEhTattoo(servico);
}


function classeDaArea(area) {
    const areaNormalizada = String(area || "").toUpperCase();
    if (areaNormalizada === "TATTOO") return "agenda-area-tattoo";
    if (areaNormalizada === "BARBEARIA") return "agenda-area-barbearia";
    return "agenda-area-neutral";
}


function tomDoCalendario(item) {
    const identificador = String(item.profissional_id || item.servico_id || item.id || "");
    const codigo = Array.from(identificador).reduce((total, caractere) => total + caractere.charCodeAt(0), 0);
    return TONS_DO_CALENDARIO[codigo % TONS_DO_CALENDARIO.length];
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
    const formularioRef = useRef(null);

    const administrativo = ["admin", "gerente"].includes(usuario?.perfil);
    const profissionalSelecionado = profissionais.find((item) => String(item.id) === String(form.profissional_id));
    const areaDaAgenda = administrativo ? profissionalSelecionado?.area_atuacao : usuario?.area_atuacao;
    const servicosVisiveis = servicos.filter((item) => servicoCompativelComArea(item, areaDaAgenda));
    const servicoSelecionado = servicos.find((item) => String(item.id) === String(form.servico_id));
    const podeEditarValor = servicoEhTattoo(servicoSelecionado);
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
                preco_aplicado: servico?.preco_padrao != null ? String(servico.preco_padrao) : "",
                recurso_id: "",
                usar_recurso_manual: servico?.modo_selecao_recurso === "MANUAL"
            }));
        }
        if (campo === "profissional_id") {
            const profissional = profissionais.find((item) => String(item.id) === String(valor));
            const servicoAtual = servicos.find((item) => String(item.id) === String(form.servico_id));
            if (servicoAtual && !servicoCompativelComArea(servicoAtual, profissional?.area_atuacao)) {
                setForm((atual) => ({ ...atual, profissional_id: valor, servico_id: "", duracao_minutos: "", preco_aplicado: "", recurso_id: "", usar_recurso_manual: false }));
            }
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
        requestAnimationFrame(() => formularioRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
    }

    function editarAgendamento(item) {
        const servico = servicos.find((itemServico) => itemServico.id === item.servico_id);
        setEditarId(item.id);
        setMensagem("");
        setErro("");
        setForm({
            profissional_id: item.profissional_id ? String(item.profissional_id) : "",
            servico_id: item.servico_id ? String(item.servico_id) : "",
            cliente_id: item.cliente_id ? String(item.cliente_id) : "",
            cliente_avulso_nome: item.cliente_avulso_nome || "",
            recurso_id: item.recurso_id ? String(item.recurso_id) : "",
            usar_recurso_manual: servico?.modo_selecao_recurso === "MANUAL",
            preco_aplicado: item.preco_aplicado != null ? String(item.preco_aplicado) : String(servico?.preco_padrao ?? ""),
            inicio_em: dataLocalInput(item.inicio_em),
            duracao_minutos: String(item.duracao_minutos || ""),
            observacao: item.observacao || ""
        });
        requestAnimationFrame(() => formularioRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
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
        if (podeEditarValor && form.preco_aplicado !== "") {
            dados.preco_aplicado = Number(form.preco_aplicado);
        }
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
    const agendaColunas = administrativo
        ? profissionais.map((item) => ({ id: item.id, nome: nomeProfissional(item, nomesUsuarios), area: item.area_atuacao }))
        : [{ id: "proprio", nome: usuario?.nome || "Minha agenda", area: usuario?.area_atuacao || "" }];
    const horasAgenda = Array.from({ length: 12 }, (_, indice) => 8 + indice);
    const agendaTotalColunas = Math.max(agendaColunas.length, 1);

    function posicaoBloco(item) {
        const inicio = new Date(item.inicio_em);
        const minutos = Math.max(0, ((inicio.getHours() - 8) * 60) + inicio.getMinutes());
        const coluna = administrativo ? agendaColunas.findIndex((pessoa) => String(pessoa.id) === String(item.profissional_id)) : 0;
        const largura = 100 / agendaTotalColunas;
        return {
            top: `${minutos * 0.8}px`,
            height: `${Math.max(Number(item.duracao_minutos || 40) * 0.8, 40)}px`,
            left: `${Math.max(coluna, 0) * largura}%`,
            width: `calc(${largura}% - 8px)`
        };
    }
    const selecionadoManual = servicoSelecionado?.requer_recurso && (
        servicoSelecionado.modo_selecao_recurso === "MANUAL" || form.usar_recurso_manual
    );

    function areaDoAgendamento(item) {
        if (!administrativo) return usuario?.area_atuacao || "";
        return profissionais.find((profissional) => String(profissional.id) === String(item.profissional_id))?.area_atuacao || "";
    }

    function moverData(quantidadeDeDias) {
        const proximaData = new Date(`${data}T12:00:00`);
        proximaData.setDate(proximaData.getDate() + quantidadeDeDias);
        setData(proximaData.toISOString().slice(0, 10));
    }

    function irParaHoje() {
        setData(dataSelecionadaInicial());
    }

    return (
        <main className="agenda-page">
            <PageHeader titulo="Agenda" subtitulo="Organize atendimentos, profissionais e recursos do HYPE.">
                <Button variant="primary" onClick={novoAgendamento}><CalendarPlus size={17} />Novo agendamento</Button>
            </PageHeader>

            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}

            <section className="agenda-toolbar">
                <Input label="Dia da agenda" type="date" value={data} onChange={(evento) => setData(evento.target.value)} />
                <div className="agenda-toolbar-summary">
                    <CalendarDays size={20} aria-hidden="true" />
                    <div>
                        <span>Compromissos do dia</span>
                        <strong>{ativos.length}</strong>
                    </div>
                </div>
                <Button variant="secondary" loading={carregando || carregandoProximos} onClick={() => { void Promise.all([carregarAgenda(), carregarProximosAgendamentos()]); }}><RefreshCw size={16} />Atualizar</Button>
            </section>

            <FormCard className="agenda-form-card" titulo={editarId ? "Editar agendamento" : "Novo agendamento"} subtitulo="A duração vem do serviço e pode ser ajustada para este horário.">
                <form ref={formularioRef} className="agenda-form" onSubmit={salvar}>
                    <div className="agenda-form-heading agenda-form-full">
                        <Clock3 size={18} aria-hidden="true" />
                        <div><strong>Serviço e horário</strong><span>Defina o responsável, o serviço e quando o atendimento acontecerá.</span></div>
                    </div>
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
                        options={servicosVisiveis.map((item) => ({ value: item.id, label: item.nome }))}
                        required
                    />
                    <Input label="Data e horário" type="datetime-local" value={form.inicio_em} onChange={(evento) => alterar("inicio_em", evento.target.value)} required />
                    <Input label="Duração (minutos)" type="number" min="1" max="1440" value={form.duracao_minutos} onChange={(evento) => alterar("duracao_minutos", evento.target.value)} required />
                    {podeEditarValor && <Input label="Valor desta tattoo" type="number" min="0" step="0.01" value={form.preco_aplicado} onChange={(evento) => alterar("preco_aplicado", evento.target.value)} placeholder="Valor combinado com o cliente" />}
                    <div className="agenda-form-heading agenda-form-full">
                        <UserRound size={18} aria-hidden="true" />
                        <div><strong>Cliente</strong><span>Vincule um cadastro existente ou informe um cliente avulso.</span></div>
                    </div>
                    <Select
                        label="Cliente cadastrado"
                        value={form.cliente_id}
                        onChange={(evento) => alterar("cliente_id", evento.target.value)}
                        options={clientes.map((item) => ({ value: item.id, label: item.nome }))}
                        placeholder="Cliente avulso"
                    />
                    {!form.cliente_id && <Input label="Nome do cliente avulso" value={form.cliente_avulso_nome} onChange={(evento) => alterar("cliente_avulso_nome", evento.target.value)} placeholder="Opcional" />}
                    {servicoSelecionado?.requer_recurso && (
                        <>
                            <div className="agenda-form-heading agenda-form-full">
                                <Wrench size={18} aria-hidden="true" />
                                <div><strong>Recurso</strong><span>Escolha uma maca ou deixe o sistema reservar uma opção livre.</span></div>
                            </div>
                            <div className="agenda-resource-choice">
                                <Checkbox
                                    label={servicoSelecionado.modo_selecao_recurso === "MANUAL" ? "Selecionar recurso manualmente (obrigatório)" : "Escolher maca ou recurso manualmente"}
                                    checked={Boolean(form.usar_recurso_manual || servicoSelecionado.modo_selecao_recurso === "MANUAL")}
                                    disabled={servicoSelecionado.modo_selecao_recurso === "MANUAL"}
                                    onChange={(evento) => alterar("usar_recurso_manual", evento.target.checked)}
                                />
                                {servicoSelecionado.modo_selecao_recurso !== "MANUAL" && <span>Se desmarcado, o sistema escolherá automaticamente um recurso livre.</span>}
                            </div>
                        </>
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
                    <div className="agenda-form-heading agenda-form-full">
                        <Scissors size={18} aria-hidden="true" />
                        <div><strong>Detalhes finais</strong><span>Inclua observações úteis para a equipe.</span></div>
                    </div>
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
                            const area = areaDoAgendamento(item);
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
                                        {!restrito && area && <span className={`agenda-area-badge ${classeDaArea(area)}`}>{area}</span>}
                                        {!restrito && item.recurso_nome && <small>{item.recurso_nome}</small>}
                                        <Button size="small" variant="secondary" onClick={() => setData(dataLocalDoAgendamento(item.inicio_em))}>Ver dia</Button>
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                )}
            </SectionCard>

            <section className="agenda-calendar-card">
                <div className="agenda-calendar-toolbar">
                    <div className="agenda-calendar-date-navigation">
                        <button type="button" className="agenda-calendar-nav-button" onClick={() => moverData(-1)} aria-label="Ver dia anterior"><ChevronLeft size={18} /></button>
                        <div className="agenda-calendar-date-copy"><span className="agenda-calendar-overline">VISÃO DO DIA</span><strong>{new Date(`${data}T12:00:00`).toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long", year: "numeric" })}</strong></div>
                        <button type="button" className="agenda-calendar-nav-button" onClick={() => moverData(1)} aria-label="Ver próximo dia"><ChevronRight size={18} /></button>
                        <button type="button" className="agenda-calendar-today" onClick={irParaHoje}>Hoje</button>
                    </div>
                    <div className="agenda-calendar-legend" aria-label="Legenda dos status da agenda">
                        <span><i className="agenda-legend-dot agenda-legend-scheduled" />Agendado</span>
                        <span><i className="agenda-legend-dot agenda-legend-confirmed" />Confirmado</span>
                        <span><i className="agenda-legend-dot agenda-legend-cancelled" />Cancelado</span>
                    </div>
                </div>
                {carregando ? <Loading texto="Carregando agenda visual..." /> : (
                    <div className="agenda-calendar-shell" style={{ "--agenda-column-count": agendaTotalColunas }}>
                        <div className="agenda-calendar-head"><span>Horário</span>{agendaColunas.map((pessoa) => <span key={pessoa.id}><strong>{pessoa.nome}</strong><small>{pessoa.area}</small></span>)}</div>
                        <div className="agenda-calendar-body">
                            <div className="agenda-calendar-hours">{horasAgenda.map((hora) => <span key={hora}>{String(hora).padStart(2, "0")}:00</span>)}</div>
                            <div className="agenda-calendar-grid">
                                {horasAgenda.map((hora) => <span className="agenda-calendar-line" key={hora} style={{ top: `${(hora - 8) * 48}px` }} />)}
                                {ordenados.map((item) => {
                                    const restrito = item.detalhes_restritos;
                                    const servico = servicos.find((servicoAtual) => servicoAtual.id === item.servico_id);
                                    const status = String(item.status || "AGENDADO").toLowerCase();
                                    const titulo = restrito ? "Recurso reservado" : servico?.nome || "Atendimento";
                                    const detalhe = restrito ? item.recurso_nome || "Recurso ocupado" : item.cliente_nome || item.cliente_avulso_nome || "Cliente avulso";
                                    return <article className={`agenda-calendar-block ${tomDoCalendario(item)} status-${status} ${restrito ? "restricted" : ""}`} key={`visual-${item.id}`} style={posicaoBloco(item)} aria-label={`${titulo}: ${detalhe}. ${rotuloStatus(item.status)}.`}><strong>{titulo}</strong><span>{detalhe}</span><small>{item.duracao_minutos} min{item.recurso_nome ? ` · ${item.recurso_nome}` : ""}</small></article>;
                                })}
                            </div>
                        </div>
                    </div>
                )}
            </section>

            <SectionCard titulo="Agenda do dia" subtitulo="Profissionais veem os próprios detalhes e apenas a ocupação dos recursos de terceiros.">
                {carregando ? <Loading texto="Carregando agenda..." /> : ordenados.length === 0 ? (
                    <div className="agenda-empty">Nenhum agendamento para este dia.</div>
                ) : (
                    <div className="agenda-list">
                        {ordenados.map((item) => {
                            const restrito = item.detalhes_restritos;
                            const area = areaDoAgendamento(item);
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
                                        {!restrito && area && <span className={`agenda-area-badge ${classeDaArea(area)}`}>{area}</span>}
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
