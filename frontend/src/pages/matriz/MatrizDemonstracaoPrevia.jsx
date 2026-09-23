import { useCallback, useEffect, useState } from "react";
import { Archive, ArrowLeft, CheckCircle2, Eye, Layers3, Palette, UserRound } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { arquivarDemonstracaoMatriz, obterPreviaDemonstracaoMatriz } from "../../services/matrizService";
import { buscarUsuarioLogado } from "../../services/usuarioService";
import { LoadingError, PageLoading } from "../../components/loading/LoadingPrimitives";

export default function MatrizDemonstracaoPrevia() {
    const { empresaId } = useParams();
    const [demo, setDemo] = useState(null);
    const [erro, setErro] = useState(null);
    const [admin, setAdmin] = useState(false);
    const [arquivando, setArquivando] = useState(false);

    const carregar = useCallback(() => {
        setErro(null);
        setDemo(null);
        obterPreviaDemonstracaoMatriz(empresaId).then(setDemo).catch((error) => setErro(error.message));
    }, [empresaId]);

    useEffect(() => {
        let ativo = true;
        let limpar;
        void Promise.resolve().then(() => {
            if (ativo) limpar = carregar();
        });
        return () => {
            ativo = false;
            limpar?.();
        };
    }, [carregar]);

    useEffect(() => {
        buscarUsuarioLogado().then((usuario) => setAdmin(usuario.perfil === "pegs_admin")).catch(() => setAdmin(false));
    }, []);

    if (erro) return <LoadingError message={`Não foi possível carregar a prévia. ${erro}`} onRetry={() => void carregar()} />;
    if (!demo) return <PageLoading message="Carregando prévia da demonstração..." />;

    return (
        <div>
            <div className="matriz-page-header"><div><div className="matriz-eyebrow">Matriz Pegs · prévia controlada</div><h1>{demo.nome}</h1><p>Ambiente de demonstração isolado. Acesso ao sistema ocorre pelo login do administrador demo.</p></div><div className="matriz-page-actions"><a className="matriz-button" href={demo.url_acesso || "/login"} target="_blank" rel="noreferrer"><Eye size={16} /> Abrir login do ambiente</a>{admin && demo.ativo && <button className="matriz-button" type="button" disabled={arquivando} onClick={async () => { if (!window.confirm("Arquivar esta demonstração? Os dados serão preservados.")) return; setArquivando(true); try { await arquivarDemonstracaoMatriz(demo.id); await carregar(); } catch (error) { setErro(error.message); } finally { setArquivando(false); } }}><Archive size={16} /> {arquivando ? "Arquivando..." : "Arquivar demo"}</button>}<Link className="matriz-button" to="/matriz/oportunidades"><ArrowLeft size={16} /> Voltar</Link></div></div>
            <section className="matriz-card matriz-preview-hero" style={{ "--preview-accent": demo.cor_primaria || "var(--matriz-accent)" }}><div className="matriz-preview-logo">{demo.logo_url ? <img src={demo.logo_url} alt={`Logo de ${demo.nome}`} /> : <span>{demo.nome.slice(0, 1).toUpperCase()}</span>}</div><div><span className="matriz-badge protected"><Eye size={12} /> Demonstração isolada</span><h2>{demo.nome}</h2><p>{demo.tipo_negocio || "Negócio de serviços"}</p><small>Criada por {demo.criado_por_usuario_nome || "Matriz Pegs"}</small></div></section>
            <div className="matriz-grid-2"><section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identidade configurada</h2><p>Esta é a aparência inicial da empresa.</p></div><Palette size={20} color="var(--preview-accent)" /></div><div className="matriz-preview-colors"><span style={{ background: demo.cor_primaria || "var(--matriz-accent)" }} /><span style={{ background: demo.cor_secundaria || "var(--matriz-accent)" }} /><div><strong>{demo.identidade_codigo || "pegs-demo"}</strong><small>Código de identidade</small></div></div></section><section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Acesso inicial</h2><p>Responsável cadastrado para iniciar o onboarding.</p></div><UserRound size={20} color="var(--matriz-accent)" /></div><div className="matriz-preview-info"><CheckCircle2 size={17} /><span>Administrador inicial configurado</span></div><small>O acesso utiliza as credenciais informadas na criação e permanece isolado deste ambiente.</small></section></div>
            <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Módulos selecionados</h2><p>A configuração pode ser ajustada antes da conversão.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div><div className="matriz-preview-modules">{demo.modulos_ativos.length ? demo.modulos_ativos.map((codigo) => <span key={codigo}>{codigo}</span>) : <div className="matriz-empty">Nenhum módulo ativo.</div>}</div></section>
        </div>
    );
}
