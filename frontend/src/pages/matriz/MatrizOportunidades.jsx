import { useCallback, useEffect, useMemo, useState } from "react";
import {
    ArrowRight,
    BriefcaseBusiness,
    CalendarDays,
    CheckCircle2,
    Eye,
    Filter,
    MessageSquarePlus,
    Plus,
    RefreshCw,
    UserRound,
} from "lucide-react";
import { Link } from "react-router-dom";

import { buscarUsuarioLogado } from "../../services/usuarioService";
import {
    aprovarConversaoMatriz,
    atualizarOportunidadeMatriz,
    criarOportunidadeMatriz,
    listarOportunidadesMatriz,
    listarUsuariosMatriz,
    listarVendedoresMatriz,
    atualizarUsuarioMatriz,
    registrarInteracaoMatriz,
    solicitarConversaoMatriz,
} from "../../services/matrizService";

const STATUS = [
    ["NOVO", "Novo"],
    ["CONTATO_PENDENTE", "Contato pendente"],
    ["EM_DEMONSTRACAO", "Em demonstração"],
    ["PROPOSTA_ENVIADA", "Proposta enviada"],
    ["CONVERTIDO", "Convertido"],
    ["RECUSADO", "Recusado"],
    ["PERDIDO", "Perdido"],
];

const STATUS_LABEL = Object.fromEntries(STATUS);

const formularioInicial = {
    nome_negocio_contato: "",
    pessoa_responsavel: "",
    telefone: "",
    email: "",
    canal_contato: "",
    cidade_regiao: "",
    tipo_negocio: "",
    vendedor_id: "",
    origem: "",
    status: "NOVO",
    proxima_acao: "",
    proximo_contato: "",
    observacoes: "",
    modulos_interesse: "",
};

function Estado({ children, erro = false }) {
    return <div className={erro ? "matriz-error" : "matriz-loading"} role={erro ? "alert" : "status"} aria-live="polite">{children}</div>;
}

function statusClass(status) {
    return `matriz-opportunity-status status-${String(status || "").toLowerCase()}`;
}

function mapForm(oportunidade) {
    return {
        nome_negocio_contato: oportunidade.nome_negocio_contato || "",
        pessoa_responsavel: oportunidade.pessoa_responsavel || "",
        telefone: oportunidade.telefone || "",
        email: oportunidade.email || "",
        canal_contato: oportunidade.canal_contato || "",
        cidade_regiao: oportunidade.cidade_regiao || "",
        tipo_negocio: oportunidade.tipo_negocio || "",
        vendedor_id: String(oportunidade.vendedor_id || ""),
        origem: oportunidade.origem || "",
        status: oportunidade.status || "NOVO",
        proxima_acao: oportunidade.proxima_acao || "",
        proximo_contato: oportunidade.proximo_contato || "",
        observacoes: oportunidade.observacoes || "",
        modulos_interesse: (oportunidade.modulos_interesse || []).join(", "),
    };
}

export default function MatrizOportunidades() {
    const [usuario, setUsuario] = useState(null);
    const [oportunidades, setOportunidades] = useState(null);
    const [vendedores, setVendedores] = useState([]);
    const [usuariosMatriz, setUsuariosMatriz] = useState([]);
    const [filtros, setFiltros] = useState({ busca: "", status: "", vendedor_id: "", proxima_acao: "" });
    const [formulario, setFormulario] = useState(formularioInicial);
    const [editandoId, setEditandoId] = useState(null);
    const [selecionadaId, setSelecionadaId] = useState(null);
    const [interacao, setInteracao] = useState({ descricao: "", proxima_acao: "", proximo_contato: "", status: "" });
    const [erro, setErro] = useState(null);
    const [mensagem, setMensagem] = useState(null);
    const [salvando, setSalvando] = useState(false);

    const admin = usuario?.perfil === "pegs_admin";
    const selecionada = oportunidades?.find((item) => item.id === selecionadaId) || null;

    const carregar = useCallback(async () => {
        setErro(null);
        try {
            const params = Object.fromEntries(Object.entries(filtros).filter(([, value]) => value));
            const [lista, listaVendedores, listaUsuarios] = await Promise.all([
                listarOportunidadesMatriz(params),
                listarVendedoresMatriz(),
                admin ? listarUsuariosMatriz() : Promise.resolve([]),
            ]);
            setOportunidades(lista);
            setVendedores(listaVendedores);
            setUsuariosMatriz(listaUsuarios);
            setSelecionadaId((atual) => (lista.some((item) => item.id === atual) ? atual : null));
        } catch (error) {
            setErro(error.message);
        }
    }, [filtros, admin]);

    useEffect(() => {
        void Promise.resolve()
            .then(() => buscarUsuarioLogado())
            .then((dadosUsuario) => setUsuario(dadosUsuario))
            .catch((error) => setErro(error.message));
    }, []);

    useEffect(() => {
        void Promise.resolve()
            .then(() => carregar())
            .catch((error) => setErro(error.message));
    }, [carregar]);

    const totais = useMemo(() => ({
        total: oportunidades?.length || 0,
        novas: oportunidades?.filter((item) => item.status === "NOVO").length || 0,
        demonstracoes: oportunidades?.filter((item) => item.status === "EM_DEMONSTRACAO").length || 0,
        conversoes: oportunidades?.filter((item) => item.conversao_solicitada_em && item.status !== "CONVERTIDO").length || 0,
    }), [oportunidades]);

    function alterarFormulario(campo, valor) {
        setFormulario((atual) => ({ ...atual, [campo]: valor }));
    }

    function resetarFormulario() {
        setFormulario({ ...formularioInicial, vendedor_id: admin ? "" : String(usuario?.id || "") });
        setEditandoId(null);
    }

    async function salvarOportunidade(event) {
        event.preventDefault();
        setErro(null);
        setMensagem(null);
        setSalvando(true);
        try {
            const dados = {
                ...formulario,
                vendedor_id: formulario.vendedor_id ? Number(formulario.vendedor_id) : null,
                modulos_interesse: formulario.modulos_interesse.split(",").map((item) => item.trim()).filter(Boolean),
                proximo_contato: formulario.proximo_contato || null,
            };
            if (editandoId) await atualizarOportunidadeMatriz(editandoId, dados);
            else await criarOportunidadeMatriz(dados);
            setMensagem(editandoId ? "Oportunidade atualizada." : "Oportunidade criada.");
            resetarFormulario();
            await carregar();
        } catch (error) {
            setErro(error.message);
        } finally {
            setSalvando(false);
        }
    }

    async function salvarInteracao(event) {
        event.preventDefault();
        if (!selecionada) return;
        setErro(null);
        setMensagem(null);
        setSalvando(true);
        try {
            await registrarInteracaoMatriz(selecionada.id, {
                ...interacao,
                proximo_contato: interacao.proximo_contato || null,
                status: interacao.status || null,
            });
            setInteracao({ descricao: "", proxima_acao: "", proximo_contato: "", status: "" });
            setMensagem("Interação registrada.");
            await carregar();
        } catch (error) {
            setErro(error.message);
        } finally {
            setSalvando(false);
        }
    }

    async function executarAcao(acao, sucesso) {
        if (!selecionada || !window.confirm(sucesso)) return;
        setErro(null);
        setMensagem(null);
        setSalvando(true);
        try {
            await acao(selecionada.id);
            setMensagem(sucesso);
            await carregar();
        } catch (error) {
            setErro(error.message);
        } finally {
            setSalvando(false);
        }
    }

    async function alterarPerfil(usuarioAlvo, perfil) {
        if (usuarioAlvo.perfil === perfil || !window.confirm(`Alterar ${usuarioAlvo.nome} para o perfil ${perfil}?`)) return;
        setErro(null);
        setMensagem(null);
        try {
            await atualizarUsuarioMatriz(usuarioAlvo.id, { perfil });
            setMensagem("Perfil atualizado e ação registrada na auditoria.");
            await carregar();
        } catch (error) {
            setErro(error.message);
        }
    }

    return (
        <div>
            <div className="matriz-page-header">
                <div>
                    <div className="matriz-eyebrow">Matriz Pegs · comercial</div>
                    <h1>Oportunidades</h1>
                    <p>Organize contatos, demonstrações e próximos passos sem misturar dados dos tenants.</p>
                </div>
                <div className="matriz-page-actions">
                    <Link className="matriz-button" to="/matriz/demonstracoes/nova"><Plus size={16} /> Criar demonstração</Link>
                    <button className="matriz-button primary" type="button" onClick={() => { resetarFormulario(); document.querySelector(".matriz-opportunity-form")?.scrollIntoView({ behavior: "smooth" }); }}><BriefcaseBusiness size={16} /> Nova oportunidade</button>
                </div>
            </div>

            {erro && <div className="matriz-form-error" role="alert">{erro}</div>}
            {mensagem && <div className="matriz-success" role="status" aria-live="polite"><CheckCircle2 size={16} /> {mensagem}</div>}

            {admin && <section className="matriz-card matriz-section matriz-vendor-config"><div className="matriz-section-heading"><div><h2>Configuração de vendedores</h2><p>Defina quem atua no comercial da Pegs. O perfil não concede acesso aos tenants.</p></div><UserRound size={20} color="var(--matriz-accent)" /></div>{usuariosMatriz.length ? <div className="matriz-table-scroll"><table className="matriz-data-table"><thead><tr><th>Usuário</th><th>E-mail</th><th>Função</th><th>Status</th></tr></thead><tbody>{usuariosMatriz.filter((item) => item.perfil !== "pegs_admin").map((item) => <tr key={item.id}><td><strong>{item.nome}</strong></td><td>{item.email}</td><td><select className="matriz-select" value={item.perfil} onChange={(event) => void alterarPerfil(item, event.target.value)}><option value="admin">Administrador</option><option value="gerente">Gerente</option><option value="operador">Operador</option><option value="consulta">Consulta</option><option value="vendedor_pegs">Vendedor Pegs</option></select></td><td><span className={`matriz-badge ${item.ativo ? "" : "inactive"}`}>{item.ativo ? "Ativo" : "Inativo"}</span></td></tr>)}</tbody></table></div> : <div className="matriz-empty">Nenhum usuário adicional cadastrado na Matriz.</div>}</section>}

            <section className="matriz-kpi-grid matriz-opportunity-kpis" aria-label="Resumo comercial">
                <article className="matriz-card matriz-kpi"><div className="matriz-kpi-label"><BriefcaseBusiness size={16} /> Oportunidades</div><div className="matriz-kpi-value">{totais.total}</div><div className="matriz-kpi-detail">No filtro atual</div></article>
                <article className="matriz-card matriz-kpi"><div className="matriz-kpi-label"><Plus size={16} /> Novas</div><div className="matriz-kpi-value">{totais.novas}</div><div className="matriz-kpi-detail">Primeiro contato</div></article>
                <article className="matriz-card matriz-kpi"><div className="matriz-kpi-label"><Eye size={16} /> Em demonstração</div><div className="matriz-kpi-value">{totais.demonstracoes}</div><div className="matriz-kpi-detail">Tenants demo vinculados</div></article>
                <article className="matriz-card matriz-kpi"><div className="matriz-kpi-label"><ArrowRight size={16} /> Aguardando aprovação</div><div className="matriz-kpi-value">{totais.conversoes}</div><div className="matriz-kpi-detail">Conversões solicitadas</div></article>
            </section>

            <section className="matriz-card matriz-section matriz-opportunity-filters">
                <div className="matriz-section-heading"><div><h2>Filtros comerciais</h2><p>Busque por negócio, contato, status ou próxima ação.</p></div><Filter size={20} color="var(--matriz-accent)" /></div>
                <div className="matriz-filters">
                    <label className="matriz-search"><BriefcaseBusiness size={16} /><input value={filtros.busca} onChange={(event) => setFiltros((atual) => ({ ...atual, busca: event.target.value }))} placeholder="Buscar negócio ou contato" aria-label="Buscar oportunidades" /></label>
                    <select className="matriz-select" value={filtros.status} onChange={(event) => setFiltros((atual) => ({ ...atual, status: event.target.value }))} aria-label="Filtrar status"><option value="">Todos os status</option>{STATUS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select>
                    {admin && <select className="matriz-select" value={filtros.vendedor_id} onChange={(event) => setFiltros((atual) => ({ ...atual, vendedor_id: event.target.value }))} aria-label="Filtrar vendedor"><option value="">Todos os vendedores</option>{vendedores.map((vendedor) => <option key={vendedor.id} value={vendedor.id}>{vendedor.nome}</option>)}</select>}
                    <label className="matriz-filter-date"><CalendarDays size={15} /><input type="date" value={filtros.proximo_contato || ""} onChange={(event) => setFiltros((atual) => ({ ...atual, proximo_contato: event.target.value }))} aria-label="Filtrar próximo contato" /></label>
                    <button className="matriz-button" type="button" onClick={() => void carregar()}><RefreshCw size={15} /> Atualizar</button>
                </div>
            </section>

            <form className="matriz-card matriz-section matriz-opportunity-form" onSubmit={salvarOportunidade}>
                <div className="matriz-section-heading"><div><h2>{editandoId ? "Editar oportunidade" : "Nova oportunidade"}</h2><p>Registre o contexto comercial e mantenha a próxima ação visível.</p></div><BriefcaseBusiness size={20} color="var(--matriz-accent)" /></div>
                <div className="matriz-form-grid matriz-form-grid-3">
                    <label className="matriz-field"><span>Negócio ou contato *</span><input required value={formulario.nome_negocio_contato} onChange={(event) => alterarFormulario("nome_negocio_contato", event.target.value)} /></label>
                    <label className="matriz-field"><span>Pessoa responsável</span><input value={formulario.pessoa_responsavel} onChange={(event) => alterarFormulario("pessoa_responsavel", event.target.value)} /></label>
                    <label className="matriz-field"><span>Tipo de negócio</span><input value={formulario.tipo_negocio} onChange={(event) => alterarFormulario("tipo_negocio", event.target.value)} placeholder="Ex.: barbearia" /></label>
                    <label className="matriz-field"><span>Telefone</span><input value={formulario.telefone} onChange={(event) => alterarFormulario("telefone", event.target.value)} /></label>
                    <label className="matriz-field"><span>E-mail</span><input type="email" value={formulario.email} onChange={(event) => alterarFormulario("email", event.target.value)} /></label>
                    <label className="matriz-field"><span>Canal de contato</span><input value={formulario.canal_contato} onChange={(event) => alterarFormulario("canal_contato", event.target.value)} placeholder="WhatsApp, indicação..." /></label>
                    <label className="matriz-field"><span>Cidade ou região</span><input value={formulario.cidade_regiao} onChange={(event) => alterarFormulario("cidade_regiao", event.target.value)} /></label>
                    <label className="matriz-field"><span>Origem</span><input value={formulario.origem} onChange={(event) => alterarFormulario("origem", event.target.value)} placeholder="Indicação, anúncio..." /></label>
                    <label className="matriz-field"><span>Próxima ação</span><input value={formulario.proxima_acao} onChange={(event) => alterarFormulario("proxima_acao", event.target.value)} /></label>
                    <label className="matriz-field"><span>Próximo contato</span><input type="date" value={formulario.proximo_contato} onChange={(event) => alterarFormulario("proximo_contato", event.target.value)} /></label>
                    <label className="matriz-field"><span>Status</span><select value={formulario.status} onChange={(event) => alterarFormulario("status", event.target.value)}>{STATUS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
                    {admin && <label className="matriz-field"><span>Vendedor responsável *</span><select required value={formulario.vendedor_id} onChange={(event) => alterarFormulario("vendedor_id", event.target.value)}><option value="">Selecione</option>{vendedores.map((vendedor) => <option key={vendedor.id} value={vendedor.id}>{vendedor.nome}</option>)}</select></label>}
                </div>
                <div className="matriz-form-grid">
                    <label className="matriz-field"><span>Módulos de interesse</span><input value={formulario.modulos_interesse} onChange={(event) => alterarFormulario("modulos_interesse", event.target.value)} placeholder="Agenda, Financeiro, Clientes" /></label>
                    <label className="matriz-field"><span>Observações</span><textarea rows="2" value={formulario.observacoes} onChange={(event) => alterarFormulario("observacoes", event.target.value)} /></label>
                </div>
                <div className="matriz-form-actions"><button className="matriz-button" type="button" onClick={resetarFormulario}>Limpar</button><button className="matriz-button primary" type="submit" disabled={salvando}><Plus size={16} /> {salvando ? "Salvando..." : editandoId ? "Salvar alterações" : "Cadastrar oportunidade"}</button></div>
            </form>

            <section className="matriz-card matriz-section">
                <div className="matriz-section-heading"><div><h2>Pipeline comercial</h2><p>{oportunidades ? `${oportunidades.length} oportunidade(s) encontrada(s)` : "Carregando registros reais"}</p></div><UserRound size={20} color="var(--matriz-accent)" /></div>
                {!oportunidades ? <Estado>Carregando oportunidades...</Estado> : oportunidades.length === 0 ? <div className="matriz-empty">Nenhuma oportunidade corresponde aos filtros atuais.</div> : (
                    <>
                        <div className="matriz-table-scroll matriz-opportunity-desktop"><table className="matriz-data-table matriz-opportunities-table"><thead><tr><th>Negócio</th><th>Status</th><th>Vendedor</th><th>Próxima ação</th><th>Próximo contato</th><th>Demonstração</th><th>Ações</th></tr></thead><tbody>{oportunidades.map((item) => <tr key={item.id}><td><strong>{item.nome_negocio_contato}</strong><small className="matriz-cell-muted">{item.pessoa_responsavel || item.email || item.telefone || "Sem contato informado"}</small></td><td><span className={statusClass(item.status)}>{STATUS_LABEL[item.status] || item.status}</span></td><td>{item.vendedor_nome || "—"}</td><td>{item.proxima_acao || "—"}</td><td>{item.proximo_contato ? new Intl.DateTimeFormat("pt-BR").format(new Date(`${item.proximo_contato}T12:00:00`)) : "—"}</td><td>{item.tenant_demo_id ? <Link className="matriz-link" to={`/matriz/demonstracoes/${item.tenant_demo_id}/previa`}>{item.tenant_demo_nome || "Abrir prévia"}</Link> : "—"}</td><td><div className="matriz-inline-actions"><button className="matriz-button" type="button" onClick={() => { setSelecionadaId(item.id); setInteracao({ descricao: "", proxima_acao: item.proxima_acao || "", proximo_contato: item.proximo_contato || "", status: item.status }); }}>Detalhes</button><button className="matriz-button" type="button" onClick={() => { setEditandoId(item.id); setFormulario(mapForm(item)); document.querySelector(".matriz-opportunity-form")?.scrollIntoView({ behavior: "smooth" }); }}>Editar</button></div></td></tr>)}</tbody></table></div>
                        <div className="matriz-opportunity-mobile">{oportunidades.map((item) => <article className="matriz-opportunity-card" key={item.id}><div className="matriz-opportunity-card-top"><strong>{item.nome_negocio_contato}</strong><span className={statusClass(item.status)}>{STATUS_LABEL[item.status] || item.status}</span></div><p>{item.pessoa_responsavel || item.email || item.telefone || "Sem contato informado"}</p><span>Vendedor: {item.vendedor_nome || "—"}</span><span>Próxima ação: {item.proxima_acao || "—"}</span><div className="matriz-inline-actions"><button className="matriz-button" type="button" onClick={() => setSelecionadaId(item.id)}>Detalhes</button><button className="matriz-button" type="button" onClick={() => { setEditandoId(item.id); setFormulario(mapForm(item)); }}>Editar</button></div></article>)}</div>
                    </>
                )}
            </section>

            {selecionada && <section className="matriz-card matriz-section matriz-opportunity-detail"><div className="matriz-section-heading"><div><div className="matriz-eyebrow">Oportunidade selecionada</div><h2>{selecionada.nome_negocio_contato}</h2><p>{selecionada.vendedor_nome} · {STATUS_LABEL[selecionada.status] || selecionada.status}</p></div><MessageSquarePlus size={21} color="var(--matriz-accent)" /></div><div className="matriz-inline-actions matriz-opportunity-actions">{!selecionada.tenant_demo_id && <Link className="matriz-button primary" to={`/matriz/demonstracoes/nova?oportunidadeId=${selecionada.id}`}><Plus size={15} /> Criar demonstração</Link>}{selecionada.tenant_demo_id && <Link className="matriz-button" to={`/matriz/demonstracoes/${selecionada.tenant_demo_id}/previa`}><Eye size={15} /> Abrir prévia</Link>}{selecionada.tenant_demo_id && !selecionada.conversao_solicitada_em && selecionada.status !== "CONVERTIDO" && <button className="matriz-button" type="button" onClick={() => void executarAcao(solicitarConversaoMatriz, "Solicitar conversão desta demonstração para empresa real?")}>Solicitar conversão</button>}{admin && selecionada.conversao_solicitada_em && selecionada.status !== "CONVERTIDO" && <button className="matriz-button primary" type="button" onClick={() => void executarAcao(aprovarConversaoMatriz, "Confirma a aprovação desta empresa real?")}>Aprovar conversão</button>}</div><div className="matriz-opportunity-history"><h3>Registrar interação</h3><form onSubmit={salvarInteracao}><div className="matriz-form-grid"><label className="matriz-field"><span>Descrição *</span><textarea required rows="3" value={interacao.descricao} onChange={(event) => setInteracao((atual) => ({ ...atual, descricao: event.target.value }))} /></label><label className="matriz-field"><span>Próxima ação</span><input value={interacao.proxima_acao} onChange={(event) => setInteracao((atual) => ({ ...atual, proxima_acao: event.target.value }))} /></label><label className="matriz-field"><span>Próximo contato</span><input type="date" value={interacao.proximo_contato} onChange={(event) => setInteracao((atual) => ({ ...atual, proximo_contato: event.target.value }))} /></label><label className="matriz-field"><span>Atualizar status</span><select value={interacao.status} onChange={(event) => setInteracao((atual) => ({ ...atual, status: event.target.value }))}><option value="">Manter status</option>{STATUS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label></div><div className="matriz-form-actions"><button className="matriz-button primary" disabled={salvando}><MessageSquarePlus size={15} /> Registrar interação</button></div></form>{selecionada.interacoes?.length ? <div className="matriz-opportunity-timeline">{selecionada.interacoes.map((item) => <div className="matriz-opportunity-timeline-item" key={item.id}><strong>{item.usuario_nome || "Usuário"}</strong><span>{item.descricao}</span><small>{new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(new Date(item.criado_em))}</small></div>)}</div> : <div className="matriz-empty">Ainda não há interações registradas.</div>}</div></section>}
        </div>
    );
}
