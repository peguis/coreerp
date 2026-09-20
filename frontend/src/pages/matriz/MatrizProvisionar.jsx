import { useEffect, useState } from "react";
import { ArrowLeft, Building2, KeyRound, Layers3, Save } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { listarCatalogoModulosMatriz, provisionarEmpresaMatriz } from "../../services/matrizService";

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
    administrador_senha: ""
};

export default function MatrizProvisionar() {
    const navigate = useNavigate();
    const [formulario, setFormulario] = useState(inicial);
    const [modulos, setModulos] = useState([]);
    const [selecionados, setSelecionados] = useState(null);
    const [erro, setErro] = useState(null);
    const [salvando, setSalvando] = useState(false);

    useEffect(() => {
        listarCatalogoModulosMatriz()
            .then((catalogo) => {
                setModulos(catalogo);
                setSelecionados(new Set(catalogo.map((modulo) => modulo.codigo)));
            })
            .catch((error) => setErro(error.message));
    }, []);

    function alterar(campo, valor) {
        setFormulario((atual) => ({ ...atual, [campo]: valor }));
    }

    function alternarModulo(codigo, obrigatorio) {
        if (obrigatorio) return;
        setSelecionados((atual) => {
            const proximo = new Set(atual || []);
            if (proximo.has(codigo)) proximo.delete(codigo);
            else proximo.add(codigo);
            return proximo;
        });
    }

    async function salvar(event) {
        event.preventDefault();
        setErro(null);
        if (!window.confirm("Confirma o provisionamento desta empresa e do administrador inicial?")) return;
        setSalvando(true);
        try {
            const dados = {
                ...formulario,
                logo_url: formulario.logo_url || null,
                cor_primaria: formulario.cor_primaria || null,
                cor_secundaria: formulario.cor_secundaria || null,
                telefone: formulario.telefone || null,
                modulos_iniciais: [...(selecionados || [])]
            };
            const empresa = await provisionarEmpresaMatriz(dados);
            navigate(`/matriz/empresas/${empresa.id}`, { state: { provisionada: true } });
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
                <div>
                    <div className="matriz-eyebrow">Matriz Pegs · provisionamento</div>
                    <h1>Nova empresa</h1>
                    <p>Crie um tenant isolado com seu administrador inicial e módulos de partida.</p>
                </div>
                <Link className="matriz-button" to="/matriz/empresas"><ArrowLeft size={16} /> Voltar para empresas</Link>
            </div>

            {erro && <div className="matriz-form-error" role="alert">{erro}</div>}
            <form className="matriz-provision-form" onSubmit={salvar}>
                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading"><div><h2>Dados da empresa</h2><p>Esses dados identificam o novo tenant na matriz.</p></div><Building2 size={20} color="var(--matriz-accent)" /></div>
                    <div className="matriz-form-grid">
                        {campo("nome", "Nome da empresa", "text", true)}
                        <label className="matriz-field"><span>Tipo de negócio</span><input value={formulario.tipo_negocio} onChange={(event) => alterar("tipo_negocio", event.target.value)} placeholder="Ex.: salão, studio, clínica" /></label>
                        {campo("cnpj", "CNPJ ou identificador", "text", true)}
                        {campo("email", "E-mail da empresa", "email", true)}
                        {campo("telefone", "Telefone")}
                    </div>
                </section>

                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading"><div><h2>Identidade inicial</h2><p>A identidade pode ser refinada depois nos detalhes do tenant.</p></div><span className="matriz-badge protected">Base Pegs-demo</span></div>
                    <div className="matriz-form-grid">
                        <label className="matriz-field"><span>Identidade inicial *</span><select required value={formulario.identidade_codigo} onChange={(event) => alterar("identidade_codigo", event.target.value)}><option value="pegs-demo">Pegs-demo (temporária)</option></select></label>
                        {campo("logo_url", "URL da logo (opcional)")}
                        {campo("cor_primaria", "Cor primária (opcional)", "text")}
                        {campo("cor_secundaria", "Cor secundária (opcional)", "text")}
                    </div>
                </section>

                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading"><div><h2>Administrador inicial</h2><p>Este usuário receberá o perfil de administrador do novo tenant.</p></div><KeyRound size={20} color="var(--matriz-accent)" /></div>
                    <div className="matriz-form-grid">
                        {campo("administrador_nome", "Nome completo", "text", true)}
                        {campo("administrador_email", "E-mail de acesso", "email", true)}
                        {campo("administrador_senha", "Senha temporária", "password", true)}
                    </div>
                </section>

                <section className="matriz-card matriz-section">
                    <div className="matriz-section-heading"><div><h2>Módulos iniciais</h2><p>Desativar aqui não apaga dados; apenas inicia o tenant sem novos registros nesses módulos.</p></div><Layers3 size={20} color="var(--matriz-accent)" /></div>
                    <div className="matriz-module-check-grid">
                        {modulos.map((modulo) => {
                            const marcado = selecionados?.has(modulo.codigo);
                            return <label className={`matriz-module-check ${marcado ? "checked" : ""}`} key={modulo.codigo}><input type="checkbox" checked={marcado || false} disabled={modulo.obrigatorio} onChange={() => alternarModulo(modulo.codigo, modulo.obrigatorio)} /><span><strong>{modulo.nome}</strong><small>{modulo.descricao || "Módulo disponível na plataforma."}</small></span>{modulo.obrigatorio && <em>Obrigatório</em>}</label>;
                        })}
                    </div>
                </section>

                <div className="matriz-form-actions"><Link className="matriz-button" to="/matriz/empresas">Cancelar</Link><button className="matriz-button primary" type="submit" disabled={salvando || !modulos.length}><Save size={16} /> {salvando ? "Provisionando..." : "Provisionar empresa"}</button></div>
            </form>
        </div>
    );
}
