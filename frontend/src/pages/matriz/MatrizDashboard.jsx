import { useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, ArrowRight, Building2, ClipboardList, Layers3, Plus, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

import { buscarDashboardMatriz } from "../../services/matrizService";

const dataFormatada = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" });
const dataHoraFormatada = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" });

function dataFormatadaSegura(value, comHora = false) {
    if (!value) return "—";
    const data = new Date(value);
    return Number.isNaN(data.valueOf()) ? "—" : (comHora ? dataHoraFormatada.format(data) : dataFormatada.format(data));
}

function EstadoMatriz({ children, erro = false }) {
    return <div className={erro ? "matriz-error" : "matriz-loading"} role={erro ? "alert" : "status"} aria-live="polite">{children}</div>;
}

export default function MatrizDashboard() {
    const [dados, setDados] = useState(null);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        let ativo = true;
        buscarDashboardMatriz()
            .then((resposta) => ativo && setDados(resposta))
            .catch((error) => ativo && setErro(error.message));
        return () => { ativo = false; };
    }, []);

    const maiorUso = useMemo(
        () => Math.max(...(dados?.modulos_mais_utilizados || []).map((modulo) => modulo.empresas_ativas), 1),
        [dados]
    );

    if (erro) return <EstadoMatriz erro>Não foi possível carregar os dados administrativos. {erro}</EstadoMatriz>;
    if (!dados) return <EstadoMatriz>Carregando visão geral da Matriz...</EstadoMatriz>;

    return (
        <div>
            <div className="matriz-page-header">
                <div>
                    <div className="matriz-eyebrow">Pegs Core · administração central</div>
                    <h1>Visão geral</h1>
                    <p>Acompanhe empresas, módulos e atividades da plataforma sem misturar dados operacionais dos tenants.</p>
                </div>
                <div className="matriz-page-actions">
                    <Link className="matriz-button primary" to="/matriz/empresas/nova"><Plus size={17} /> Nova empresa</Link>
                </div>
            </div>

            <section className="matriz-kpi-grid" aria-label="Indicadores da plataforma">
                <article className="matriz-card matriz-kpi">
                    <div className="matriz-kpi-label"><Building2 size={16} /> Empresas cadastradas</div>
                    <div className="matriz-kpi-value">{dados.total_empresas}</div>
                    <div className="matriz-kpi-detail">Todos os tenants registrados</div>
                </article>
                <article className="matriz-card matriz-kpi">
                    <div className="matriz-kpi-label"><Activity size={16} /> Empresas ativas</div>
                    <div className="matriz-kpi-value">{dados.empresas_ativas}</div>
                    <div className="matriz-kpi-detail">Podem operar normalmente</div>
                </article>
                <article className="matriz-card matriz-kpi">
                    <div className="matriz-kpi-label"><Layers3 size={16} /> Módulos catalogados</div>
                    <div className="matriz-kpi-value">{dados.modulos_mais_utilizados.length}</div>
                    <div className="matriz-kpi-detail">Disponíveis para configuração</div>
                </article>
                <article className="matriz-card matriz-kpi">
                    <div className="matriz-kpi-label"><AlertTriangle size={16} /> Alertas administrativos</div>
                    <div className="matriz-kpi-value">{dados.alertas.length}</div>
                    <div className="matriz-kpi-detail">Pendências que exigem atenção</div>
                </article>
            </section>

            <div className="matriz-grid-2">
                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading">
                        <div><h2>Uso dos módulos</h2><p>Empresas ativas por módulo no catálogo atual.</p></div>
                        <Layers3 size={19} color="var(--matriz-accent)" />
                    </div>
                    {dados.modulos_mais_utilizados.length ? (
                        <div className="matriz-module-list">
                            {dados.modulos_mais_utilizados.map((modulo) => (
                                <div className="matriz-module-row" key={modulo.codigo}>
                                    <span>{modulo.nome}</span>
                                    <div className="matriz-module-bar" aria-label={`${modulo.empresas_ativas} empresas ativas`}>
                                        <span style={{ width: `${Math.max((modulo.empresas_ativas / maiorUso) * 100, modulo.empresas_ativas ? 8 : 0)}%` }} />
                                    </div>
                                    <strong>{modulo.empresas_ativas}</strong>
                                </div>
                            ))}
                        </div>
                    ) : <div className="matriz-empty">Nenhum módulo foi catalogado ainda.</div>}
                </section>

                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading">
                        <div><h2>Alertas administrativos</h2><p>Informações que merecem acompanhamento.</p></div>
                        <ShieldCheck size={19} color="var(--matriz-accent)" />
                    </div>
                    {dados.alertas.length ? (
                        <div className="matriz-alert-list">
                            {dados.alertas.map((alerta) => (
                                <Link className="matriz-alert" key={`${alerta.empresa_id}-${alerta.titulo}`} to={alerta.empresa_id ? `/matriz/empresas/${alerta.empresa_id}` : "/matriz/empresas"}>
                                    <span className="matriz-alert-icon"><AlertTriangle size={16} /></span>
                                    <span><strong>{alerta.titulo}</strong><span>{alerta.descricao}</span></span>
                                    <ArrowRight size={16} color="var(--matriz-muted)" />
                                </Link>
                            ))}
                        </div>
                    ) : <div className="matriz-empty">Nenhum alerta administrativo no momento.</div>}
                </section>
            </div>

            <section className="matriz-card matriz-section" style={{ marginBottom: 18 }}>
                <div className="matriz-section-heading">
                    <div><h2>Empresas criadas recentemente</h2><p>Tenants mais novos no ambiente da plataforma.</p></div>
                    <Link className="matriz-link" to="/matriz/empresas">Ver todas <ArrowRight size={13} /></Link>
                </div>
                {dados.empresas_recentes.length ? (
                    <div className="matriz-table-scroll">
                        <table className="matriz-tenant-table">
                            <thead><tr><th>Empresa</th><th>Tipo</th><th>Módulos ativos</th><th>Status</th><th>Criação</th><th /></tr></thead>
                            <tbody>
                                {dados.empresas_recentes.map((empresa) => (
                                    <tr key={empresa.id}>
                                        <td><div className="matriz-tenant-name"><span className="matriz-tenant-dot">{empresa.nome.slice(0, 1).toUpperCase()}</span><span><strong>{empresa.nome}</strong><small>{empresa.email}</small></span></div></td>
                                        <td>{empresa.tipo_negocio || "Não informado"}</td>
                                        <td>{empresa.modulos_ativos}</td>
                                        <td><span className={`matriz-badge ${empresa.ativo ? "" : "inactive"}`}>{empresa.ativo ? "Ativa" : "Inativa"}</span>{empresa.protegido && <span className="matriz-badge protected" style={{ marginLeft: 6 }}>Protegida</span>}</td>
                                        <td>{dataFormatadaSegura(empresa.created_at)}</td>
                                        <td><Link className="matriz-link" to={`/matriz/empresas/${empresa.id}`}>Abrir</Link></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : <div className="matriz-empty">Nenhuma empresa cadastrada.</div>}
            </section>

            <section className="matriz-card matriz-section">
                <div className="matriz-section-heading">
                    <div><h2>Últimas ações da auditoria</h2><p>Registros administrativos mais recentes.</p></div>
                    <Link className="matriz-link" to="/matriz/auditoria">Ver auditoria <ArrowRight size={13} /></Link>
                </div>
                {dados.ultimas_auditorias.length ? (
                    <div className="matriz-audit-list">
                        {dados.ultimas_auditorias.slice(0, 5).map((registro) => (
                            <div className="matriz-audit-item" key={registro.id}>
                                <ClipboardList size={17} color="var(--matriz-accent)" />
                                <div><strong>{registro.acao} · {registro.recurso}</strong><span>{registro.empresa_nome || "Empresa não identificada"} · {registro.usuario_nome || "Sistema"} · {dataFormatadaSegura(registro.criado_em, true)}</span></div>
                            </div>
                        ))}
                    </div>
                ) : <div className="matriz-empty">A auditoria ainda não possui registros.</div>}
            </section>
        </div>
    );
}
