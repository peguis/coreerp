import { useCallback, useEffect, useState } from "react";
import { ClipboardList, Filter, RefreshCw } from "lucide-react";

import { listarAuditoriaMatriz, listarEmpresasMatriz } from "../../services/matrizService";

const dataHora = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" });

function formatarData(value) {
    if (!value) return "—";
    const data = new Date(value);
    return Number.isNaN(data.valueOf()) ? "—" : dataHora.format(data);
}

function Estado({ children, erro = false }) {
    return <div className={erro ? "matriz-error" : "matriz-loading"} role={erro ? "alert" : "status"} aria-live="polite">{children}</div>;
}

export default function MatrizAuditoria() {
    const [registros, setRegistros] = useState(null);
    const [empresas, setEmpresas] = useState([]);
    const [empresaId, setEmpresaId] = useState("");
    const [acao, setAcao] = useState("");
    const [erro, setErro] = useState(null);

    const carregar = useCallback(async () => {
        setErro(null);
        try {
            setRegistros(await listarAuditoriaMatriz({ empresa_id: empresaId || undefined, acao: acao || undefined, limite: 100 }));
        } catch (error) {
            setErro(error.message);
        }
    }, [acao, empresaId]);

    useEffect(() => {
        void Promise.resolve().then(async () => {
            try {
                const lista = await listarEmpresasMatriz();
                setEmpresas(lista);
                await carregar();
            } catch (error) {
                setErro(error.message);
            }
        });
    }, [carregar]);

    return (
        <div>
            <div className="matriz-page-header">
                <div><div className="matriz-eyebrow">Matriz Pegs · segurança</div><h1>Auditoria</h1><p>Consulte provisionamentos, alterações de identidade, módulos e demais ações administrativas reais.</p></div>
                <button type="button" className="matriz-button" onClick={() => void carregar()}><RefreshCw size={16} /> Atualizar</button>
            </div>
            <section className="matriz-card matriz-section" style={{ marginBottom: 18 }}>
                <div className="matriz-filters"><label className="matriz-field matriz-filter-field"><span>Empresa</span><select className="matriz-select" value={empresaId} onChange={(event) => setEmpresaId(event.target.value)}><option value="">Todas as empresas</option>{empresas.map((empresa) => <option value={empresa.id} key={empresa.id}>{empresa.nome}</option>)}</select></label><label className="matriz-field matriz-filter-field"><span>Ação</span><input value={acao} onChange={(event) => setAcao(event.target.value)} placeholder="Ex.: PROVISIONAR_EMPRESA" /></label><button type="button" className="matriz-button" onClick={() => void carregar()}><Filter size={16} /> Filtrar</button></div>
            </section>
            <section className="matriz-card matriz-section">
                <div className="matriz-section-heading"><div><h2>Registro administrativo</h2><p>{registros ? `${registros.length} registro(s) encontrado(s)` : "Carregando registros reais"}</p></div><ClipboardList size={20} color="var(--matriz-accent)" /></div>
                {erro ? <Estado erro>Não foi possível carregar a auditoria. {erro}</Estado> : !registros ? <Estado>Carregando auditoria...</Estado> : registros.length === 0 ? <div className="matriz-empty">Nenhum registro corresponde aos filtros atuais.</div> : <div className="matriz-table-scroll"><table className="matriz-data-table"><thead><tr><th>Data e hora</th><th>Empresa afetada</th><th>Usuário responsável</th><th>Ação</th><th>Recurso</th><th>Detalhes</th></tr></thead><tbody>{registros.map((registro) => <tr key={registro.id}><td>{formatarData(registro.criado_em)}</td><td>{registro.empresa_nome || `Empresa #${registro.empresa_id}`}</td><td>{registro.usuario_nome || "Sistema"}</td><td><span className="matriz-badge protected">{registro.acao}</span></td><td>{registro.recurso}{registro.recurso_id ? ` #${registro.recurso_id}` : ""}</td><td>{registro.detalhes ? JSON.stringify(registro.detalhes) : "—"}</td></tr>)}</tbody></table></div>}
            </section>
        </div>
    );
}
