import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Eye, Layers3, Palette, UserRound } from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { obterPreviaDemonstracaoMatriz } from "../../services/matrizService";

export default function MatrizDemonstracaoPrevia() {
    const { empresaId } = useParams();
    const [demo, setDemo] = useState(null);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        obterPreviaDemonstracaoMatriz(empresaId).then(setDemo).catch((error) => setErro(error.message));
    }, [empresaId]);

    if (erro) return <div className="matriz-error" role="alert">Não foi possível carregar a prévia. {erro}</div>;
    if (!demo) return <div className="matriz-loading" role="status" aria-live="polite">Carregando prévia da demonstração...</div>;

    return (
        <div>
            <div className="matriz-page-header"><div><div className="matriz-eyebrow">Matriz Pegs · prévia controlada</div><h1>{demo.nome}</h1><p>Esta tela apresenta a identidade e a configuração inicial do tenant demo, sem expor dados de outros clientes.</p></div><Link className="matriz-button" to="/matriz/oportunidades"><ArrowLeft size={16} /> Voltar</Link></div>
            <section className="matriz-card matriz-preview-hero" style={{ "--preview-accent": demo.cor_primaria || "var(--matriz-accent)" }}><div className="matriz-preview-logo">{demo.logo_url ? <img src={demo.logo_url} alt={`Logo de ${demo.nome}`} /> : <span>{demo.nome.slice(0, 1).toUpperCase()}</span>}</div><div><span className="matriz-badge protected"><Eye size={12} /> Demonstração isolada</span><h2>{demo.nome}</h2><p>{demo.tipo_negocio || "Negócio de serviços"}</p><small>Criada por {demo.criado_por_usuario_nome || "Matriz Pegs"}</small></div></section>
            <div className="matriz-grid-2"><section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identidade configurada</h2><p>Esta é a aparência inicial da empresa.</p></div><Palette size={20} color="var(--preview-accent)" /></div><div className="matriz-preview-colors"><span style={{ background: demo.cor_primaria || "var(--matriz-accent)" }} /><span style={{ background: demo.cor_secundaria || "var(--matriz-accent)" }} /><div><strong>{demo.identidade_codigo || "pegs-demo"}</strong><small>Código de identidade</small></div></div></section><section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Acesso inicial</h2><p>Responsável cadastrado para iniciar o onboarding.</p></div><UserRound size={20} color="var(--matriz-accent)" /></div><div className="matriz-preview-info"><CheckCircle2 size={17} /><span>Administrador inicial configurado</span></div><small>O acesso utiliza as credenciais informadas na criação e permanece isolado deste ambiente.</small></section></div>
            <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Módulos selecionados</h2><p>A configuração pode ser ajustada antes da conversão.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div><div className="matriz-preview-modules">{demo.modulos_ativos.length ? demo.modulos_ativos.map((codigo) => <span key={codigo}>{codigo}</span>) : <div className="matriz-empty">Nenhum módulo ativo.</div>}</div></section>
        </div>
    );
}
