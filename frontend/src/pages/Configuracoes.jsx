import { useCallback, useEffect, useState } from "react";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import SectionCard from "../components/ui/SectionCard";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";
import {
    atualizarUsuario,
    atualizarModuloEmpresa,
    buscarUsuarioLogado,
    criarUsuario,
    listarModulosEmpresa,
    listarUsuarios
} from "../services/usuarioService";
import { atualizarConfiguracaoEmpresa, buscarEmpresaAtual, buscarOnboardingEmpresa } from "../services/empresaService";
import { getErrorMessage } from "../utils/errors";

import "./Configuracoes.css";


const PERFIS = [
    { value: "admin", label: "Administrador" },
    { value: "gerente", label: "Gerente" },
    { value: "operador", label: "Operador" },
    { value: "consulta", label: "Consulta" },
    { value: "usuario", label: "Usuário" },
    { value: "profissional", label: "Profissional" }
];


const FORM_INICIAL = {
    nome: "",
    email: "",
    senha: "",
    perfil: "profissional"
};


const EMPRESA_FORM_INICIAL = {
    nome_exibicao: "",
    logo_url: "",
    cor_primaria: "",
    cor_secundaria: "",
    tema: "dark",
    tipo_negocio: ""
};


function Configuracoes() {

    const [usuario, setUsuario] = useState(null);
    const [usuarios, setUsuarios] = useState([]);
    const [modulos, setModulos] = useState([]);
    const [empresa, setEmpresa] = useState(null);
    const [onboarding, setOnboarding] = useState(null);
    const [empresaForm, setEmpresaForm] = useState(EMPRESA_FORM_INICIAL);
    const [salvandoEmpresa, setSalvandoEmpresa] = useState(false);
    const [form, setForm] = useState(FORM_INICIAL);
    const [editarId, setEditarId] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [alterandoStatus, setAlterandoStatus] = useState(null);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const carregar = useCallback(async () => {

        try {

            setCarregando(true);
            setErro("");
            const [usuarioDados, usuariosDados, modulosDados, empresaDados, onboardingDados] = await Promise.all([
                buscarUsuarioLogado(),
                listarUsuarios(),
                listarModulosEmpresa(),
                buscarEmpresaAtual(),
                buscarOnboardingEmpresa()
            ]);
            setUsuario(usuarioDados);
            setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);
            setModulos(Array.isArray(modulosDados) ? modulosDados : []);
            setEmpresa(empresaDados);
            setOnboarding(onboardingDados);
            setEmpresaForm({
                nome_exibicao: empresaDados.nome || "",
                logo_url: empresaDados.logo_url || "",
                cor_primaria: empresaDados.cor_primaria || "",
                cor_secundaria: empresaDados.cor_secundaria || "",
                tema: empresaDados.tema || "dark",
                tipo_negocio: empresaDados.tipo_negocio || ""
            });

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar os usuários."));

        } finally {

            setCarregando(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    const ehAdmin = usuario?.perfil === "admin";

    function alterar(campo, valor) {

        setForm((atual) => ({ ...atual, [campo]: valor }));

    }

    function alterarEmpresa(campo, valor) {
        setEmpresaForm((atual) => ({ ...atual, [campo]: valor }));
    }

    async function salvarConfiguracaoEmpresa(evento) {
        evento.preventDefault();
        if (salvandoEmpresa) return;
        try {
            setErro("");
            setMensagem("");
            setSalvandoEmpresa(true);
            const atualizada = await atualizarConfiguracaoEmpresa({
                ...empresaForm,
                nome_exibicao: empresaForm.nome_exibicao.trim(),
                logo_url: empresaForm.logo_url.trim() || null,
                cor_primaria: empresaForm.cor_primaria.trim() || null,
                cor_secundaria: empresaForm.cor_secundaria.trim() || null,
                tipo_negocio: empresaForm.tipo_negocio.trim() || null
            });
            setEmpresa(atualizada);
            setMensagem("Identidade da empresa atualizada. Recarregue a página para aplicar o shell completo.");
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível salvar a identidade da empresa."));
        } finally {
            setSalvandoEmpresa(false);
        }
    }

    function limparForm() {

        setEditarId(null);
        setForm(FORM_INICIAL);

    }

    function editar(usuarioItem) {

        setEditarId(usuarioItem.id);
        setForm({
            nome: usuarioItem.nome,
            email: usuarioItem.email,
            senha: "",
            perfil: usuarioItem.perfil
        });
        setErro("");
        setMensagem("");

    }

    async function salvar(evento) {

        evento.preventDefault();
        if (salvando) return;
        setErro("");
        setMensagem("");

        if (form.nome.trim().length < 3) {
            setErro("O nome deve possuir no mínimo 3 caracteres.");
            return;
        }

        if (!form.email.trim()) {
            setErro("Informe o e-mail do usuário.");
            return;
        }

        if (!editarId && form.senha.length < 6) {
            setErro("A senha inicial deve possuir no mínimo 6 caracteres.");
            return;
        }

        if (editarId && form.senha && form.senha.length < 6) {
            setErro("A nova senha deve possuir no mínimo 6 caracteres.");
            return;
        }

        try {

            setSalvando(true);
            const dados = {
                nome: form.nome.trim(),
                email: form.email.trim(),
                perfil: form.perfil
            };

            if (editarId) {

                if (form.senha) {
                    dados.senha = form.senha;
                }
                await atualizarUsuario(editarId, dados);
                setMensagem("Usuário atualizado com sucesso.");

            } else {

                await criarUsuario({
                    ...dados,
                    senha: form.senha,
                    empresa_id: usuario.empresa_id
                });
                setMensagem("Usuário cadastrado com sucesso.");

            }

            limparForm();
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível salvar o usuário."));

        } finally {

            setSalvando(false);

        }

    }

    async function alternarAtivo(usuarioItem) {

        if (alterandoStatus) return;

        try {

            setErro("");
            setMensagem("");
            setAlterandoStatus(usuarioItem.id);
            await atualizarUsuario(usuarioItem.id, { ativo: !usuarioItem.ativo });
            setMensagem(usuarioItem.ativo ? "Usuário desativado." : "Usuário ativado.");
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível alterar o status do usuário."));

        } finally {

            setAlterandoStatus(null);

        }

    }

    async function alternarModulo(modulo) {
        if (modulo.obrigatorio || alterandoStatus) return;

        try {
            setErro("");
            setMensagem("");
            setAlterandoStatus(`modulo-${modulo.codigo}`);
            await atualizarModuloEmpresa(modulo.codigo, !modulo.ativo);
            setMensagem(modulo.ativo ? "Módulo desativado. O histórico foi preservado." : "Módulo ativado.");
            await carregar();
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível alterar o módulo."));
        } finally {
            setAlterandoStatus(null);
        }
    }

    function nomePerfil(perfil) {

        return PERFIS.find((item) => item.value === perfil)?.label || perfil;

    }

    return (

        <main className="configuracoes-page">
            <PageHeader titulo="Configurações" subtitulo="Gerencie os usuários da empresa e as preferências do sistema" />
            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}

            <SectionCard titulo="Usuários" subtitulo="Crie o acesso do barbeiro ou tatuador antes de vinculá-lo em Profissionais.">
                {!ehAdmin && <Mensagem tipo="sucesso" texto="Somente ADMIN pode criar, editar ou alterar o status de usuários." />}
                {ehAdmin && <FormCard titulo={editarId ? "Editar usuário" : "Novo usuário"} subtitulo="A senha inicial é usada somente no cadastro e nunca é exibida depois.">
                    <form className="configuracoes-form" onSubmit={salvar}>
                        <Input label="Nome" value={form.nome} onChange={(evento) => alterar("nome", evento.target.value)} required />
                        <Input label="E-mail" type="email" value={form.email} onChange={(evento) => alterar("email", evento.target.value)} required />
                        <Select label="Perfil" value={form.perfil} onChange={(evento) => alterar("perfil", evento.target.value)} options={PERFIS} required />
                        <Input label={editarId ? "Nova senha (opcional)" : "Senha inicial"} type="password" value={form.senha} onChange={(evento) => alterar("senha", evento.target.value)} placeholder={editarId ? "Deixe vazio para manter" : "Mínimo de 6 caracteres"} required={!editarId} />
                        <div className="configuracoes-form-actions">
                            {editarId && <Button type="button" variant="secondary" onClick={limparForm}>Cancelar edição</Button>}
                            <Button type="submit" variant="primary" disabled={salvando}>{salvando ? "Salvando..." : editarId ? "Salvar alterações" : "Cadastrar usuário"}</Button>
                        </div>
                    </form>
                </FormCard>}
            </SectionCard>

            <SectionCard>
                {carregando ? <Loading texto="Carregando usuários..." /> : usuarios.length === 0 ? <div className="configuracoes-empty">Nenhum usuário encontrado.</div> : <>
                    <div className="configuracoes-table-wrap">
                        <table className="configuracoes-table"><thead><tr><th>Nome</th><th>E-mail</th><th>Perfil</th><th>Status</th>{ehAdmin && <th>Ações</th>}</tr></thead><tbody>{usuarios.map((usuarioItem) => <tr key={usuarioItem.id}><td>{usuarioItem.nome}</td><td>{usuarioItem.email}</td><td>{nomePerfil(usuarioItem.perfil)}</td><td>{usuarioItem.ativo ? "Ativo" : "Inativo"}</td>{ehAdmin && <td><div className="configuracoes-actions"><Button size="small" variant="secondary" onClick={() => editar(usuarioItem)}>Editar</Button><Button size="small" variant={usuarioItem.ativo ? "danger" : "success"} disabled={alterandoStatus === usuarioItem.id} onClick={() => alternarAtivo(usuarioItem)}>{usuarioItem.ativo ? "Desativar" : "Ativar"}</Button></div></td>}</tr>)}</tbody></table>
                    </div>
                    <div className="configuracoes-mobile-cards">{usuarios.map((usuarioItem) => <article className="configuracoes-user-card" key={usuarioItem.id}><header><strong>{usuarioItem.nome}</strong><span>{usuarioItem.ativo ? "Ativo" : "Inativo"}</span></header><dl><div><dt>E-mail</dt><dd>{usuarioItem.email}</dd></div><div><dt>Perfil</dt><dd>{nomePerfil(usuarioItem.perfil)}</dd></div></dl>{ehAdmin && <div className="configuracoes-actions"><Button size="small" variant="secondary" onClick={() => editar(usuarioItem)}>Editar</Button><Button size="small" variant={usuarioItem.ativo ? "danger" : "success"} disabled={alterandoStatus === usuarioItem.id} onClick={() => alternarAtivo(usuarioItem)}>{usuarioItem.ativo ? "Desativar" : "Ativar"}</Button></div>}</article>)}</div>
                </>}
            </SectionCard>

            {ehAdmin && modulos.length > 0 && <SectionCard titulo="Módulos da empresa" subtitulo="A ativação controla a disponibilidade da funcionalidade. As permissões dos usuários continuam independentes.">
                <div className="configuracoes-modulos-grid">
                    {modulos.map((modulo) => <article className={`configuracoes-modulo-card ${modulo.ativo ? "ativo" : "inativo"}`} key={modulo.codigo}>
                        <div>
                            <strong>{modulo.nome}</strong>
                            <p>{modulo.descricao || "Funcionalidade da plataforma Pegs."}</p>
                        </div>
                        <Button
                            size="small"
                            variant={modulo.ativo ? "danger" : "success"}
                            disabled={modulo.obrigatorio || alterandoStatus === `modulo-${modulo.codigo}`}
                            onClick={() => alternarModulo(modulo)}
                        >
                            {modulo.ativo ? "Desativar" : "Ativar"}
                        </Button>
                    </article>)}
                </div>
            </SectionCard>}

            {usuario && empresa && <SectionCard titulo="Identidade da empresa" subtitulo="A Pegs mantém a estrutura do produto e aplica a identidade configurada para cada empresa.">
                <form className="configuracoes-form" onSubmit={salvarConfiguracaoEmpresa}>
                    <Input label="Nome exibido" value={empresaForm.nome_exibicao} onChange={(evento) => alterarEmpresa("nome_exibicao", evento.target.value)} required />
                    <Input label="Tipo de negócio" value={empresaForm.tipo_negocio} onChange={(evento) => alterarEmpresa("tipo_negocio", evento.target.value)} placeholder="Ex.: Barbearia e Tattoo" />
                    <Input label="Logo (URL ou caminho público)" value={empresaForm.logo_url} onChange={(evento) => alterarEmpresa("logo_url", evento.target.value)} placeholder="Opcional" />
                    <Select label="Tema" value={empresaForm.tema} onChange={(evento) => alterarEmpresa("tema", evento.target.value)} options={[{ value: "dark", label: "Escuro" }, { value: "light", label: "Claro (preparado)" }]} />
                    <Input label="Cor primária" value={empresaForm.cor_primaria} onChange={(evento) => alterarEmpresa("cor_primaria", evento.target.value)} placeholder="Ex.: #D9AB3F" />
                    <Input label="Cor secundária" value={empresaForm.cor_secundaria} onChange={(evento) => alterarEmpresa("cor_secundaria", evento.target.value)} placeholder="Ex.: #EDC45C" />
                    <div className="configuracoes-form-actions">
                        <Button type="submit" variant="primary" disabled={salvandoEmpresa}>{salvandoEmpresa ? "Salvando..." : "Salvar identidade"}</Button>
                    </div>
                </form>
            </SectionCard>}

            {onboarding && <SectionCard titulo="Configuração inicial" subtitulo="Acompanhe o que falta para deixar a empresa pronta para operar.">
                <div className="configuracoes-onboarding-summary">
                    <strong>{onboarding.percentual_concluido}% concluído</strong>
                    <span>{onboarding.concluido ? "Configuração essencial concluída." : "Complete os itens obrigatórios para iniciar a operação."}</span>
                </div>
                <div className="configuracoes-onboarding-list">
                    {onboarding.itens.map((item) => <div className={`configuracoes-onboarding-item ${item.concluido ? "concluido" : "pendente"}`} key={item.codigo}>
                        <span className="configuracoes-onboarding-icon" aria-hidden="true">{item.concluido ? "✓" : "!"}</span>
                        <div><strong>{item.titulo}</strong><p>{item.descricao}</p></div>
                        <small>{item.concluido ? "Concluído" : item.obrigatorio ? "Pendente" : "Opcional"}</small>
                    </div>)}
                </div>
            </SectionCard>}
        </main>

    );

}


export default Configuracoes;
