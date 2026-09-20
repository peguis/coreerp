import { useCallback, useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, ClipboardList, Layers3, LockKeyhole, Save, ShieldCheck, Users } from "lucide-react";
import { Link, useLocation, useParams } from "react-router-dom";

import { atualizarIdentidadeEmpresaMatriz, atualizarModuloEmpresaMatriz, atualizarUsuarioEmpresaMatriz, buscarDetalheEmpresaMatriz } from "../../services/matrizService";

const dataHora = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" });
function formatarData(value) {
    if (!value) return "—";
    const data = new Date(value);
    return Number.isNaN(data.valueOf()) ? "—" : dataHora.format(data);
}

function Estado({ children, erro = false }) {
    return <div className={erro ? "matriz-error" : "matriz-loading"} role={erro ? "alert" : "status"} aria-live="polite">{children}</div>;
}

export default function MatrizEmpresaDetalhe() {
    const { empresaId } = useParams();
    const location = useLocation();
    const [detalhe, setDetalhe] = useState(null);
    const [aba, setAba] = useState("visao-geral");
    const [erro, setErro] = useState(null);
    const [salvando, setSalvando] = useState(false);
    const [identidade, setIdentidade] = useState(null);

    const carregar = useCallback(async () => {
        setErro(null);
        try {
            const resposta = await buscarDetalheEmpresaMatriz(empresaId);
            setDetalhe(resposta);
            setIdentidade({
                nome_exibicao: resposta.empresa.nome,
                identidade_codigo: resposta.empresa.identidade_codigo || "pegs-demo",
                logo_url: resposta.empresa.logo_url || "",
                cor_primaria: resposta.empresa.cor_primaria || "",
                cor_secundaria: resposta.empresa.cor_secundaria || "",
                tema: resposta.empresa.tema || "",
                tipo_negocio: resposta.empresa.tipo_negocio || "",
                ativo: resposta.empresa.ativo
            });
        } catch (error) {
            setErro(error.message);
        }
    }, [empresaId]);

    useEffect(() => { void Promise.resolve().then(carregar); }, [carregar]);

    async function salvarIdentidade(event) {
        event.preventDefault();
        if (!identidade || detalhe.empresa.protegido) return;
        setSalvando(true);
        setErro(null);
        try {
            const atualizada = await atualizarIdentidadeEmpresaMatriz(empresaId, identidade);
            setDetalhe((atual) => ({ ...atual, empresa: { ...atual.empresa, ...atualizada } }));
        } catch (error) {
            setErro(error.message);
        } finally {
            setSalvando(false);
        }
    }

    async function alternarModulo(modulo) {
        if (detalhe.empresa.protegido || modulo.obrigatorio) return;
        const acao = modulo.ativo ? "desativar" : "ativar";
        if (!window.confirm(`Confirma ${acao} o módulo ${modulo.nome}? Os dados históricos não serão apagados.`)) return;
        try {
            await atualizarModuloEmpresaMatriz(empresaId, modulo.codigo, !modulo.ativo);
            await carregar();
        } catch (error) {
            setErro(error.message);
        }
    }

    async function alternarUsuario(usuario) {
        if (empresa.protegido) return;
        const acao = usuario.ativo ? "desativar" : "ativar";
        if (!window.confirm(`Confirma ${acao} o acesso de ${usuario.nome}?`)) return;
        try {
            await atualizarUsuarioEmpresaMatriz(empresaId, usuario.id, { ativo: !usuario.ativo });
            await carregar();
        } catch (error) {
            setErro(error.message);
        }
    }

    function alterarIdentidade(campo, valor) {
        setIdentidade((atual) => ({ ...atual, [campo]: valor }));
    }

    if (erro && !detalhe) return <Estado erro>Não foi possível carregar o tenant. {erro}</Estado>;
    if (!detalhe || !identidade) return <Estado>Carregando detalhes da empresa...</Estado>;

    const { empresa, modulos, usuarios, auditoria } = detalhe;
    const abas = [
        ["visao-geral", "Visão geral", CheckCircle2],
        ["identidade", "Identidade", ShieldCheck],
        ["modulos", "Módulos", Layers3],
        ["usuarios", "Usuários", Users],
        ["auditoria", "Auditoria", ClipboardList]
    ];

    return (
        <div>
            <div className="matriz-page-header">
                <div>
                    <div className="matriz-eyebrow">Matriz Pegs · tenant {empresa.id}</div>
                    <h1>{empresa.nome}</h1>
                    <p>{empresa.tipo_negocio || "Tipo de negócio não informado"} · {empresa.email}</p>
                </div>
                <Link className="matriz-button" to="/matriz/empresas"><ArrowLeft size={16} /> Voltar para empresas</Link>
            </div>

            {location.state?.provisionada && <div className="matriz-success" role="status"><CheckCircle2 size={17} /> Empresa provisionada e auditoria registrada com sucesso.</div>}
            {erro && <div className="matriz-form-error" role="alert">{erro}</div>}

            <div className="matriz-tenant-summary">
                <div className="matriz-card matriz-summary-card"><span className="matriz-summary-label">Status</span><strong><span className={`matriz-badge ${empresa.ativo ? "" : "inactive"}`}>{empresa.ativo ? "Ativa" : "Inativa"}</span></strong></div>
                <div className="matriz-card matriz-summary-card"><span className="matriz-summary-label">Módulos ativos</span><strong>{empresa.modulos_ativos}</strong></div>
                <div className="matriz-card matriz-summary-card"><span className="matriz-summary-label">Administrador principal</span><strong>{empresa.administrador_principal?.nome || "Não cadastrado"}</strong></div>
                <div className="matriz-card matriz-summary-card"><span className="matriz-summary-label">Identidade</span><strong>{empresa.protegido ? "HYPE protegida" : empresa.identidade_codigo || "Não definida"}</strong></div>
            </div>

            <div className="matriz-detail-tabs" role="tablist" aria-label="Seções do tenant">
                {abas.map(([codigo, nome, Icon]) => <button type="button" role="tab" aria-selected={aba === codigo} className={aba === codigo ? "active" : ""} onClick={() => setAba(codigo)} key={codigo}><Icon size={16} /> {nome}</button>)}
            </div>

            {aba === "visao-geral" && <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Configuração inicial</h2><p>Resumo do ambiente para administração da plataforma.</p></div><BuildingPlaceholder /></div><div className="matriz-overview-grid"><div><span className="matriz-summary-label">CNPJ / identificador</span><strong>{empresa.cnpj}</strong></div><div><span className="matriz-summary-label">Telefone</span><strong>{empresa.telefone || "Não informado"}</strong></div><div><span className="matriz-summary-label">Criada em</span><strong>{formatarData(empresa.created_at)}</strong></div><div><span className="matriz-summary-label">Logo configurada</span><strong>{empresa.logo_url ? "Sim" : "Usa identidade padrão"}</strong></div></div></section>}

            {aba === "identidade" && <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identidade da empresa</h2><p>Altere somente o que o backend suporta com segurança.</p></div>{empresa.protegido && <span className="matriz-badge protected"><LockKeyhole size={12} /> HYPE protegida</span>}</div>{empresa.protegido ? <div className="matriz-protected-box"><LockKeyhole size={18} /><div><strong>A identidade da HYPE STUDIO está protegida.</strong><span>Esta Fase 5.1 não altera a identidade, módulos ou dados do primeiro tenant real.</span></div></div> : <form className="matriz-form-grid" onSubmit={salvarIdentidade}><label className="matriz-field"><span>Nome exibido *</span><input required value={identidade.nome_exibicao} onChange={(event) => alterarIdentidade("nome_exibicao", event.target.value)} /></label><label className="matriz-field"><span>Identidade inicial</span><select value={identidade.identidade_codigo} onChange={(event) => alterarIdentidade("identidade_codigo", event.target.value)}><option value="pegs-demo">Pegs-demo (temporária)</option><option value="hype">HYPE (protegida)</option></select></label><label className="matriz-field"><span>Tipo de negócio</span><input value={identidade.tipo_negocio} onChange={(event) => alterarIdentidade("tipo_negocio", event.target.value)} /></label><label className="matriz-field"><span>URL da logo</span><input value={identidade.logo_url} onChange={(event) => alterarIdentidade("logo_url", event.target.value)} /></label><label className="matriz-field"><span>Cor primária</span><input value={identidade.cor_primaria} onChange={(event) => alterarIdentidade("cor_primaria", event.target.value)} placeholder="#6F8CFF" /></label><label className="matriz-field"><span>Cor secundária</span><input value={identidade.cor_secundaria} onChange={(event) => alterarIdentidade("cor_secundaria", event.target.value)} placeholder="#9BB0FF" /></label><label className="matriz-toggle"><input type="checkbox" checked={identidade.ativo} onChange={(event) => alterarIdentidade("ativo", event.target.checked)} /><span><strong>Empresa ativa</strong><small>Empresas inativas não recebem novas operações.</small></span></label><div className="matriz-form-actions"><button className="matriz-button primary" type="submit" disabled={salvando}><Save size={16} /> {salvando ? "Salvando..." : "Salvar identidade"}</button></div></form>}</section>}

            {aba === "modulos" && <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Módulos do tenant</h2><p>Desativar um módulo bloqueia novos registros, mas preserva o histórico.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div><div className="matriz-detail-module-list">{modulos.map((modulo) => <div className="matriz-detail-module" key={modulo.codigo}><div><strong>{modulo.nome}</strong><span>{modulo.descricao || "Módulo disponível na plataforma."}</span></div><div className="matriz-module-actions">{modulo.obrigatorio && <span className="matriz-badge protected">Obrigatório</span>}<span className={`matriz-badge ${modulo.ativo ? "" : "inactive"}`}>{modulo.ativo ? "Ativo" : "Inativo"}</span><button className="matriz-button" type="button" disabled={empresa.protegido || modulo.obrigatorio} onClick={() => void alternarModulo(modulo)}>{modulo.ativo ? "Desativar" : "Ativar"}</button></div></div>)}</div></section>}

            {aba === "usuarios" && <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Administradores e usuários</h2><p>Responsáveis vinculados exclusivamente a este tenant.</p></div><Users size={20} color="var(--matriz-accent)" /></div>{usuarios.length ? <div className="matriz-table-scroll"><table className="matriz-data-table"><thead><tr><th>Nome</th><th>E-mail</th><th>Perfil</th><th>Status</th><th>Criação</th><th>Ação</th></tr></thead><tbody>{usuarios.map((usuario) => <tr key={usuario.id}><td><strong>{usuario.nome}</strong></td><td>{usuario.email}</td><td>{usuario.perfil}</td><td><span className={`matriz-badge ${usuario.ativo ? "" : "inactive"}`}>{usuario.ativo ? "Ativo" : "Inativo"}</span></td><td>{formatarData(usuario.created_at)}</td><td><button className="matriz-button" type="button" disabled={empresa.protegido} onClick={() => void alternarUsuario(usuario)}>{usuario.ativo ? "Desativar" : "Ativar"}</button></td></tr>)}</tbody></table></div> : <div className="matriz-empty">Nenhum usuário cadastrado neste tenant.</div>}</section>}

            {aba === "auditoria" && <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Auditoria do tenant</h2><p>Alterações administrativas registradas pelo backend.</p></div><ClipboardList size={20} color="var(--matriz-accent)" /></div>{auditoria.length ? <div className="matriz-audit-list">{auditoria.map((registro) => <div className="matriz-audit-item" key={registro.id}><ClipboardList size={17} color="var(--matriz-accent)" /><div><strong>{registro.acao} · {registro.recurso}</strong><span>{registro.usuario_nome || "Sistema"} · {formatarData(registro.criado_em, true)}</span></div></div>)}</div> : <div className="matriz-empty">Nenhuma ação auditada para este tenant.</div>}</section>}
        </div>
    );
}

function BuildingPlaceholder() {
    return <div aria-hidden="true" style={{ color: "var(--matriz-accent)" }}><ShieldCheck size={20} /></div>;
}
