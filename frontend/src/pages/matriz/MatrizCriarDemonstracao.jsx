import { useEffect, useRef, useState } from "react";
import { ArrowLeft, Building2, Layers3, Save, ShieldCheck } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import {
    criarDemonstracaoMatriz,
    listarCatalogoModulosMatriz,
} from "../../services/matrizService";
import { SectionLoading } from "../../components/loading/LoadingPrimitives";

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

const modulosSugeridosPorModelo = {
    barbearia: ["dashboard", "agenda", "clientes", "servicos", "profissionais", "atendimentos", "repasses", "financeiro"],
    salao: ["dashboard", "agenda", "clientes", "servicos", "profissionais", "atendimentos", "financeiro"],
    tatuagem: ["dashboard", "agenda", "clientes", "servicos", "profissionais", "recursos", "atendimentos", "repasses", "financeiro"],
    servicos: ["dashboard", "agenda", "clientes", "servicos", "profissionais", "atendimentos"],
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
    const [etapa, setEtapa] = useState(1);
    const [template, setTemplate] = useState("personalizado");
    const [dadosApresentacao, setDadosApresentacao] = useState(false);
    const chaveIdempotencia = useRef(null);
    const requisicaoEmAndamento = useRef(false);

    useEffect(() => {
        let ativo = true;
        listarCatalogoModulosMatriz()
            .then((catalogo) => {
                if (!ativo) return;
                setModulos(catalogo);
                setSelecionados(new Set(catalogo.filter((modulo) => modulo.obrigatorio).map((modulo) => modulo.codigo)));
            })
            .catch((error) => ativo && setErro(error.message));
        return () => { ativo = false; };
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

    function selecionarModelo(valor) {
        setTemplate(valor);
        if (valor !== "personalizado") {
            setFormulario((atual) => ({ ...atual, tipo_negocio: valor === "barbearia" ? "Barbearia" : valor === "salao" ? "Salão" : valor === "tatuagem" ? "Estúdio de tattoo" : "Serviços" }));
            const disponiveis = new Set(modulos.map((modulo) => modulo.codigo));
            const sugeridos = (modulosSugeridosPorModelo[valor] || []).filter((codigo) => disponiveis.has(codigo));
            const obrigatorios = modulos.filter((modulo) => modulo.obrigatorio).map((modulo) => modulo.codigo);
            setSelecionados(new Set([...obrigatorios, ...sugeridos]));
        }
    }

    async function salvar(event) {
        event.preventDefault();
        if (requisicaoEmAndamento.current) return;
        setErro(null);
        if (etapa < 3) {
            if (etapa === 2 && selecionados.size === 0) {
                setErro("Selecione ao menos um módulo para a demonstração.");
                return;
            }
            setEtapa((atual) => atual + 1);
            return;
        }
        if (!window.confirm("Confirma a criação desta demonstração isolada?")) return;
        requisicaoEmAndamento.current = true;
        setSalvando(true);
        try {
            const armazenamentoChave = `matriz-demo-key:${oportunidadeId || "nova"}`;
            chaveIdempotencia.current ||= sessionStorage.getItem(armazenamentoChave) || globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`;
            sessionStorage.setItem(armazenamentoChave, chaveIdempotencia.current);
            const demo = await criarDemonstracaoMatriz({
                ...formulario,
                identidade_codigo: "pegs-demo",
                logo_url: formulario.logo_url || null,
                cor_primaria: formulario.cor_primaria || null,
                cor_secundaria: formulario.cor_secundaria || null,
                telefone: formulario.telefone || null,
                modulos_iniciais: [...selecionados],
                template,
                dados_apresentacao: dadosApresentacao,
                chave_idempotencia: chaveIdempotencia.current,
                vendedor_id: null,
                oportunidade_id: oportunidadeId ? Number(oportunidadeId) : null,
            });
            sessionStorage.removeItem(armazenamentoChave);
            navigate(`/matriz/demonstracoes/${demo.id}/previa`, { state: { criada: true } });
        } catch (error) {
            setErro(error.message);
        } finally {
            requisicaoEmAndamento.current = false;
            setSalvando(false);
        }
    }

    const campo = (nome, label, tipo = "text", obrigatorio = false) => (
        <label className="matriz-field" key={nome}>
            <span>{label}{obrigatorio && " *"}</span>
            <input required={obrigatorio && ((etapa === 1 && ["nome", "cnpj", "email"].includes(nome)) || etapa === 3)} type={tipo} value={formulario[nome]} onChange={(event) => alterar(nome, event.target.value)} />
        </label>
    );

    return (
        <div>
            <div className="matriz-page-header">
                <div><div className="matriz-eyebrow">Matriz Pegs · demonstração</div><h1>Criar demonstração</h1><p>Monte uma prévia isolada para apresentar a Pegs sem criar dados operacionais fictícios.</p></div>
                <Link className="matriz-button" to="/matriz/oportunidades"><ArrowLeft size={16} /> Voltar para oportunidades</Link>
            </div>
            <div className="matriz-wizard-progress" role="list" aria-label="Etapas da criação">{["Negócio", "Prévia", "Acesso e revisão"].map((nome, indice) => <div role="listitem" key={nome} className={etapa >= indice + 1 ? "active" : ""} aria-current={etapa === indice + 1 ? "step" : undefined}><span>{indice + 1}</span>{nome}</div>)}</div>
            {etapa === 3 && <section className="matriz-card matriz-section"><h2>Revise a demonstração</h2><p><strong>Negócio:</strong> {formulario.nome} · {formulario.tipo_negocio || "Personalizado"}</p><p><strong>Módulos selecionados:</strong> {modulos.filter((item) => selecionados.has(item.codigo)).map((item) => item.nome).join(", ") || "Nenhum"}</p><p><strong>Dados ilustrativos:</strong> {dadosApresentacao ? "Sim, identificados como exemplo" : "Não; ambiente vazio"}</p></section>}
            {erro && <div className="matriz-form-error" role="alert">{erro}</div>}
            <form className={"matriz-provision-form wizard-step-" + etapa} onSubmit={salvar}>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identificação da demonstração</h2><p>A demonstração terá identidade própria e permanecerá separada dos tenants reais.</p></div><Building2 size={20} color="var(--matriz-accent)" /></div><label className="matriz-field"><span>Modelo inicial</span><select value={template} onChange={(event) => selecionarModelo(event.target.value)}><option value="barbearia">Barbearia</option><option value="salao">Salão</option><option value="tatuagem">Estúdio de tattoo</option><option value="servicos">Serviços</option><option value="personalizado">Personalizado</option></select></label><div className="matriz-form-grid">{campo("nome", "Nome do negócio *", "text", true)}{campo("tipo_negocio", "Tipo de negócio", "text", false)}{campo("cnpj", "CNPJ ou identificador *", "text", true)}{campo("email", "E-mail do negócio *", "email", true)}{campo("telefone", "Telefone")}</div></section>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Identidade da prévia</h2><p>Logo e cores podem ser ajustadas na configuração do tenant depois.</p></div><span className="matriz-badge protected"><ShieldCheck size={12} /> Ambiente demo</span></div><div className="matriz-form-grid">{campo("logo_url", "URL da logo (opcional)")}{campo("cor_primaria", "Cor primária (opcional)")}{campo("cor_secundaria", "Cor secundária (opcional)")}</div></section>
                <section className="matriz-card matriz-section"><div className="matriz-section-heading"><div><h2>Acesso de prévia</h2><p>Crie o administrador inicial para a demonstração.</p></div><ShieldCheck size={20} color="var(--matriz-accent)" /></div><div className="matriz-form-grid">{campo("administrador_nome", "Nome do administrador *", "text", true)}{campo("administrador_email", "E-mail de acesso *", "email", true)}{campo("administrador_senha", "Senha temporária *", "password", true)}</div></section>
                <section className="matriz-card matriz-section" aria-busy={!modulos.length && !erro}><div className="matriz-section-heading"><div><h2>Módulos da prévia</h2><p>Selecione as funcionalidades que serão apresentadas.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div>{!modulos.length && !erro ? <SectionLoading message="Carregando catálogo de módulos..." /> : <div className="matriz-module-check-grid">{modulos.map((modulo) => { const marcado = selecionados.has(modulo.codigo); return <label className={`matriz-module-check ${marcado ? "checked" : ""}`} key={modulo.codigo}><input type="checkbox" checked={marcado} disabled={modulo.obrigatorio} onChange={() => alternarModulo(modulo.codigo, modulo.obrigatorio)} /><span><strong>{modulo.nome}</strong><small>{modulo.descricao || "Módulo disponível na plataforma."}</small></span>{modulo.obrigatorio && <em>Obrigatório</em>}</label>; })}</div>}<label className="matriz-module-check"><input type="checkbox" checked={dadosApresentacao} onChange={(event) => setDadosApresentacao(event.target.checked)} /><span><strong>Incluir dados ilustrativos de apresentação</strong><small>Opcional. Os registros serão claramente identificados e existirão apenas neste tenant demo.</small></span></label></section>
                <div className="matriz-form-actions"><Link className="matriz-button" to="/matriz/oportunidades">Cancelar</Link><button className="matriz-button primary" type="submit" disabled={salvando || !modulos.length} aria-busy={salvando || undefined}><Save size={16} /> {salvando ? "Criando..." : "Criar demonstração"}</button></div>
            </form>
        </div>
    );
}
