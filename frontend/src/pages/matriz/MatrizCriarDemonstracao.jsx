import { useEffect, useState } from "react";
import { ArrowLeft, Building2, Layers3, Save, ShieldCheck } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import {
    criarDemonstracaoMatriz,
    listarCatalogoModulosMatriz,
} from "../../services/matrizService";

const inicial = {
    nome: "",
    tipo_negocio: "",
    identidade_codigo: "pegs-demo",
    logo_url: "",
    cor_primaria: "",
    cor_secundaria: "",
    cnpj: "",
    email: "",
    telefone: "",
    administrador_nome: "",
    administrador_email: "",
    administrador_senha: "",
};

export default function MatrizCriarDemonstracao() {
    const navigate = useNavigate();
    const location = useLocation();
    const oportunidadeId = new URLSearchParams(location.search).get("oportunidadeId");
    const [formulario, setFormulario] = useState(inicial);
    const [modulos, setModulos] = useState([]);
    const [selecionados, setSelecionados] = useState(new Set());
    const [erro, setErro] = useState(null);
    const [salvando, setSalvando] = useState(false);

    useEffect(() => {
        listarCatalogoModulosMatriz()
            .then((catalogo) => {
                setModulos(catalogo);
                setSelecionados(new Set(catalogo.filter((modulo) => modulo.obrigatorio).map((modulo) => modulo.codigo)));
            })
            .catch((error) => setErro(error.message));
    }, []);

    function alterar(campo, valor) {
        setFormulario((atual) => ({ ...atual, [campo]: valor }));
    }

    function alternarModulo(codigo, obrigatorio) {
        if (obrigatorio) return;
        setSelecionados((atual) => {
            const proximo = new Set(atual);
            if (proximo.has(codigo)) proximo.delete(codigo);
            else proximo.add(codigo);
            return proximo;
        });
    }

    async function salvar(event) {
        event.preventDefault();
        setErro(null);
        if (!window.confirm("Confirma a criação desta demonstração isolada?")) return;
        setSalvando(true);
        try {
            const demo = await criarDemonstracaoMatriz({
                ...formulario,
                identidade_codigo: "pegs-demo",
                logo_url: formulario.logo_url || null,
                cor_primaria: formulario.cor_primaria || null,
                cor_secundaria: formulario.cor_secundaria || null,
                telefone: formulario.telefone || null,
                modulos_iniciais: [...selecionados],
                vendedor_id: null,
                oportunidade_id: oportunidadeId ? Number(oportunidadeId) : null,
            });
            navigate(`/matriz/demonstracoes/${demo.id}/previa`, { state: { criada: true } });
        } catch (error) {
            setErro(error.message);
        } finally {
            setSalvando(false);
        }
    }

    const campo = (nome, label, tipo = "text", obrigatorio = false) => (
        <label className="matriz-field" key={nome}>
            <span>{label}{obrigatorio && " *"}</span>
            <input required={obrigatorio} type={tipo} value={formulario[nome]} onChange={(event) => alterar(nome, event.target.value)} />
        </label>
    );

    return (
        <div>
            <div className="matriz-page-header">
                <div><div className="matriz-eyebrow">Matriz Pegs · demonstração</div><h1>Criar demonstração</h1><p>Monte uma prévia isolada para apresentar a Pegs sem criar dados operacionais fictícios.</p></div>
                <Link className="matriz-button" to="/matriz/oportunidades"><ArrowLeft size={16} /> Voltar para oportunidades</Link>
            </div>
            {erro && <div className="matriz-form-error" role="alert">{erro}</div>}
            <form className="matriz-provision-form" onSubmit={salvar}>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identificação da demonstração</h2><p>A demonstração terá identidade própria e permanecerá separada dos tenants reais.</p></div><Building2 size={20} color="var(--matriz-accent)" /></div><div className="matriz-form-grid">{campo("nome", "Nome do negócio *", "text", true)}{campo("tipo_negocio", "Tipo de negócio", "text", false)}{campo("cnpj", "CNPJ ou identificador *", "text", true)}{campo("email", "E-mail do negócio *", "email", true)}{campo("telefone", "Telefone")}</div></section>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identidade da prévia</h2><p>Logo e cores podem ser ajustadas na configuração do tenant depois.</p></div><span className="matriz-badge protected"><ShieldCheck size={12} /> Ambiente demo</span></div><div className="matriz-form-grid">{campo("logo_url", "URL da logo (opcional)")}{campo("cor_primaria", "Cor primária (opcional)")}{campo("cor_secundaria", "Cor secundária (opcional)")}</div></section>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Acesso de prévia</h2><p>Crie o administrador inicial para a demonstração.</p></div><ShieldCheck size={20} color="var(--matriz-accent)" /></div><div className="matriz-form-grid">{campo("administrador_nome", "Nome do administrador *", "text", true)}{campo("administrador_email", "E-mail de acesso *", "email", true)}{campo("administrador_senha", "Senha temporária *", "password", true)}</div></section>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Módulos da prévia</h2><p>Selecione apenas o que será apresentado. A demonstração nasce sem registros operacionais.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div><div className="matriz-module-check-grid">{modulos.map((modulo) => { const marcado = selecionados.has(modulo.codigo); return <label className={`matriz-module-check ${marcado ? "checked" : ""}`} key={modulo.codigo}><input type="checkbox" checked={marcado} disabled={modulo.obrigatorio} onChange={() => alternarModulo(modulo.codigo, modulo.obrigatorio)} /><span><strong>{modulo.nome}</strong><small>{modulo.descricao || "Módulo disponível na plataforma."}</small></span>{modulo.obrigatorio && <em>Obrigatório</em>}</label>; })}</div></section>
                <div className="matriz-form-actions"><Link className="matriz-button" to="/matriz/oportunidades">Cancelar</Link><button className="matriz-button primary" type="submit" disabled={salvando || !modulos.length}><Save size={16} /> {salvando ? "Criando..." : "Criar demonstração"}</button></div>
            </form>
        </div>
    );
}
