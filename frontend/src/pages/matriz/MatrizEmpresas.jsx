import { useCallback, useEffect, useState } from "react";
import { Building2, Eye, Plus, Search, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

import { listarEmpresasMatriz } from "../../services/matrizService";

function Estado({ children, erro = false }) {
    return <div className={erro ? "matriz-error" : "matriz-loading"} role={erro ? "alert" : "status"} aria-live="polite">{children}</div>;
}

export default function MatrizEmpresas() {
    const [empresas, setEmpresas] = useState(null);
    const [busca, setBusca] = useState("");
    const [status, setStatus] = useState("");
    const [erro, setErro] = useState(null);

    const carregar = useCallback(async () => {
        setErro(null);
        try {
            setEmpresas(await listarEmpresasMatriz({ busca: busca || undefined, status: status || undefined }));
        } catch (error) {
            setErro(error.message);
        }
    }, [busca, status]);

    useEffect(() => {
        const timer = window.setTimeout(() => void carregar(), busca ? 240 : 0);
        return () => window.clearTimeout(timer);
    }, [carregar, busca]);

    return (
        <div>
            <div className="matriz-page-header">
                <div>
                    <div className="matriz-eyebrow">Matriz Pegs · tenants</div>
                    <h1>Empresas</h1>
                    <p>Consulte os ambientes cadastrados, seus módulos e responsáveis principais.</p>
                </div>
                <div className="matriz-page-actions"><Link className="matriz-button primary" to="/matriz/empresas/nova"><Plus size={17} /> Nova empresa</Link></div>
            </div>

            <section className="matriz-card matriz-section" style={{ marginBottom: 18 }}>
                <div className="matriz-filters">
                    <label className="matriz-search"><Search size={17} /><input value={busca} onChange={(event) => setBusca(event.target.value)} placeholder="Buscar por nome, e-mail ou CNPJ" aria-label="Buscar empresas" /></label>
                    <select className="matriz-select" value={status} onChange={(event) => setStatus(event.target.value)} aria-label="Filtrar por status">
                        <option value="">Todos os status</option>
                        <option value="ativo">Ativas</option>
                        <option value="inativo">Inativas</option>
                    </select>
                    <button type="button" className="matriz-button" onClick={() => void carregar()}><Search size={16} /> Atualizar</button>
                </div>
            </section>

            <section className="matriz-card matriz-section">
                <div className="matriz-section-heading">
                    <div><h2>Tenants cadastrados</h2><p>{empresas ? `${empresas.length} resultado(s) encontrado(s)` : "Carregando registros reais"}</p></div>
                    <Building2 size={20} color="var(--matriz-accent)" />
                </div>
                {erro ? <Estado erro>Não foi possível carregar as empresas. {erro}</Estado> : !empresas ? <Estado>Carregando empresas...</Estado> : empresas.length === 0 ? <div className="matriz-empty">Nenhuma empresa corresponde aos filtros atuais.</div> : (
                    <div className="matriz-table-scroll">
                        <table className="matriz-data-table matriz-empresas-table">
                            <thead><tr><th>Empresa</th><th>Tipo de negócio</th><th>Administrador principal</th><th>Módulos</th><th>Status</th><th>Identidade</th><th>Ações</th></tr></thead>
                            <tbody>
                                {empresas.map((empresa) => (
                                    <tr key={empresa.id}>
                                        <td><div className="matriz-tenant-name"><span className="matriz-tenant-dot">{empresa.nome.slice(0, 1).toUpperCase()}</span><span><strong>{empresa.nome}</strong><small>{empresa.email}</small></span></div></td>
                                        <td>{empresa.tipo_negocio || "Não informado"}</td>
                                        <td>{empresa.administrador_principal ? <><strong>{empresa.administrador_principal.nome}</strong><small className="matriz-cell-muted">{empresa.administrador_principal.email}</small></> : <span className="matriz-cell-muted">Não cadastrado</span>}</td>
                                        <td>{empresa.modulos_ativos}</td>
                                        <td><span className={`matriz-badge ${empresa.ativo ? "" : "inactive"}`}>{empresa.ativo ? "Ativa" : "Inativa"}</span></td>
                                        <td>{empresa.protegido ? <span className="matriz-badge protected"><ShieldCheck size={12} /> Protegida</span> : empresa.identidade_codigo || "—"}</td>
                                        <td><Link className="matriz-button" to={`/matriz/empresas/${empresa.id}`}><Eye size={15} /> Detalhes</Link></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>
        </div>
    );
}
