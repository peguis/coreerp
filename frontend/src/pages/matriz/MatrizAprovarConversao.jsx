import { useState } from "react";
import { CheckCircle2, X } from "lucide-react";

const inicial = { cnpj: "", email: "", administrador_nome: "", administrador_email: "", administrador_senha: "" };

export default function MatrizAprovarConversao({ oportunidade, onConfirmar, onFechar, salvando }) {
    const [dados, setDados] = useState(inicial);
    const campo = (name, label, type = "text") => <label className="matriz-field" key={name}><span>{label} *</span><input required minLength={name.includes("senha") ? 6 : undefined} type={type} value={dados[name]} onChange={(event) => setDados((atual) => ({ ...atual, [name]: event.target.value }))} /></label>;
    return <div className="matriz-modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onFechar()}>
        <section className="matriz-card matriz-section matriz-conversion-modal" role="dialog" aria-modal="true" aria-labelledby="conversion-title">
            <div className="matriz-section-heading"><div><div className="matriz-eyebrow">Revisão e aprovação</div><h2 id="conversion-title">Criar empresa real</h2></div><button className="matriz-button" type="button" aria-label="Fechar" onClick={onFechar}><X size={17} /></button></div>
            <p>Será criado um tenant separado a partir da configuração do demo. A demonstração original será preservada. Informe os dados definitivos da empresa e do administrador.</p>
            <div className="matriz-conversion-summary"><strong>{oportunidade.nome_negocio_contato}</strong><span>Demo: {oportunidade.tenant_demo_nome || "—"}</span><span>Responsável comercial: {oportunidade.vendedor_nome || "—"}</span><span>Origem: conversão aprovada pela Matriz Pegs</span></div>
            <form onSubmit={(event) => { event.preventDefault(); void onConfirmar(dados); }}>
                <div className="matriz-form-grid">{campo("cnpj", "CNPJ / identificador definitivo")}{campo("email", "E-mail da empresa", "email")}{campo("administrador_nome", "Administrador responsável")}{campo("administrador_email", "E-mail do administrador", "email")}{campo("administrador_senha", "Senha inicial", "password")}</div>
                <div className="matriz-form-actions"><button className="matriz-button" type="button" onClick={onFechar} disabled={salvando}>Cancelar</button><button className="matriz-button primary" type="submit" disabled={salvando}><CheckCircle2 size={15} />{salvando ? "Criando tenant..." : "Aprovar e criar tenant"}</button></div>
            </form>
        </section>
    </div>;
}
