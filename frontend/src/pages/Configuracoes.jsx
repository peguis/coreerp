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
    buscarUsuarioLogado,
    criarUsuario,
    listarUsuarios
} from "../services/usuarioService";
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


function Configuracoes() {

    const [usuario, setUsuario] = useState(null);
    const [usuarios, setUsuarios] = useState([]);
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
            const [usuarioDados, usuariosDados] = await Promise.all([
                buscarUsuarioLogado(),
                listarUsuarios()
            ]);
            setUsuario(usuarioDados);
            setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);

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
        </main>

    );

}


export default Configuracoes;
