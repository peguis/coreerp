import { useCallback, useEffect, useState } from "react";

import { buscarUsuarioLogado, listarUsuarios } from "../services/usuarioService";
import { listarProfissionais, criarProfissional, atualizarProfissional, desativarProfissional } from "../services/profissionalService";
import { getErrorMessage } from "../utils/errors";
import { formatarPercentual } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import SectionCard from "../components/ui/SectionCard";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


function Profissionais() {

    const [usuario, setUsuario] = useState(null);
    const [profissionais, setProfissionais] = useState([]);
    const [usuarios, setUsuarios] = useState([]);
    const [form, setForm] = useState({ usuario_id: "", area_atuacao: "", percentual_padrao: "" });
    const [editarId, setEditarId] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const carregar = useCallback(async () => {

        try {

            setCarregando(true);
            setErro("");
            const [usuarioDados, profissionaisDados, usuariosDados] = await Promise.all([
                buscarUsuarioLogado(),
                listarProfissionais({ pagina: 1, limite: 100 }),
                listarUsuarios()
            ]);
            setUsuario(usuarioDados);
            setProfissionais(Array.isArray(profissionaisDados) ? profissionaisDados : []);
            setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar os profissionais."));

        } finally {

            setCarregando(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    function limparForm() {

        setEditarId(null);
        setForm({ usuario_id: "", area_atuacao: "", percentual_padrao: "" });

    }

    function editar(profissional) {

        setEditarId(profissional.id);
        setForm({
            usuario_id: profissional.usuario_id,
            area_atuacao: profissional.area_atuacao,
            percentual_padrao: String(profissional.percentual_padrao)
        });

    }

    async function salvar(evento) {

        evento.preventDefault();
        if (salvando) return;
        setErro("");
        setMensagem("");

        if (!form.area_atuacao || (ehAdmin && form.percentual_padrao === "") || (!editarId && !form.usuario_id)) {

            setErro("Informe usuário, área e percentual padrão.");
            return;

        }

        try {

            setSalvando(true);
            if (editarId) {
                const dados = { area_atuacao: form.area_atuacao };
                if (ehAdmin) dados.percentual_padrao = Number(form.percentual_padrao);
                await atualizarProfissional(editarId, dados);
                setMensagem("Profissional atualizado com sucesso.");

            } else {
                await criarProfissional({
                    usuario_id: Number(form.usuario_id),
                    area_atuacao: form.area_atuacao,
                    percentual_padrao: Number(form.percentual_padrao)
                });
                setMensagem("Profissional cadastrado com sucesso.");

            }
            limparForm();
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível salvar o profissional."));

        } finally {

            setSalvando(false);

        }

    }

    async function alternarAtivo(profissional) {

        try {

            setErro("");
            if (profissional.ativo) await desativarProfissional(profissional.id);
            else await atualizarProfissional(profissional.id, { ativo: true });
            setMensagem(profissional.ativo ? "Profissional desativado." : "Profissional ativado.");
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível alterar o status do profissional."));

        }

    }

    function nomeUsuario(usuarioId) {

        return usuarios.find((usuario) => usuario.id === usuarioId)?.nome || `Usuário #${usuarioId}`;

    }

    const usuariosDisponiveis = usuarios.filter((usuario) =>
        usuario.ativo && !profissionais.some((item) => item.usuario_id === usuario.id)
    );
    const ehAdmin = ["pegs_admin", "admin"].includes(usuario?.perfil);
    const ehGerente = usuario?.perfil === "gerente";

    return (

        <main className="piloto-page">
            <PageHeader titulo="Profissionais" subtitulo="Gerencie os vínculos, áreas de atuação e percentuais padrão da empresa." />
            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}
            {ehAdmin ? <FormCard titulo={editarId ? "Editar profissional" : "Novo profissional"} subtitulo="Cadastre a área de atuação usada pela empresa. O percentual padrão pode ser substituído somente no atendimento por ADMIN/GERENTE.">
                <form className="piloto-form-grid" onSubmit={salvar}>
                    {!editarId && <Select label="Usuário vinculado" value={form.usuario_id} onChange={(evento) => setForm((atual) => ({ ...atual, usuario_id: evento.target.value }))} options={usuariosDisponiveis.map((usuarioItem) => ({ value: usuarioItem.id, label: `${usuarioItem.nome} — ${usuarioItem.email}` }))} required />}
                    <Input label="Área de atuação" value={form.area_atuacao} onChange={(evento) => setForm((atual) => ({ ...atual, area_atuacao: evento.target.value }))} placeholder="Ex.: BARBEARIA, TATTOO, SALÃO ou STUDIO" required />
                    <Input label="Percentual padrão" type="number" min="0" max="100" step="0.01" value={form.percentual_padrao} onChange={(evento) => setForm((atual) => ({ ...atual, percentual_padrao: evento.target.value }))} required />
                    <div className="piloto-form-actions piloto-form-full"><Button type="button" variant="secondary" onClick={limparForm}>Limpar</Button><Button type="submit" variant="primary" disabled={salvando}>{salvando ? "Salvando..." : editarId ? "Salvar alterações" : "Cadastrar profissional"}</Button></div>
                </form>
            </FormCard> : ehGerente && editarId ? <FormCard titulo="Alterar função do profissional" subtitulo="O gerente pode atualizar a área de atuação do profissional conforme a operação da empresa.">
                <form className="piloto-form-grid" onSubmit={salvar}>
                    <Input label="Área de atuação" value={form.area_atuacao} onChange={(evento) => setForm((atual) => ({ ...atual, area_atuacao: evento.target.value }))} placeholder="Ex.: BARBEARIA, TATTOO, SALÃO ou STUDIO" required />
                    <div className="piloto-form-actions piloto-form-full"><Button type="button" variant="secondary" onClick={limparForm}>Cancelar</Button><Button type="submit" variant="primary" disabled={salvando}>{salvando ? "Salvando..." : "Salvar função"}</Button></div>
                </form>
            </FormCard> : !ehGerente && <Mensagem tipo="sucesso" texto="GERENTE possui acesso à consulta. Alterações de profissionais são exclusivas do ADMIN." />}
            <SectionCard>
                {carregando ? <Loading texto="Carregando profissionais..." /> : profissionais.length === 0 ? <div className="piloto-empty">Nenhum profissional cadastrado.</div> : <><div className="piloto-table-wrap"><table className="piloto-table"><thead><tr><th>Usuário</th><th>Área</th><th>Percentual padrão</th><th>Status</th>{(ehAdmin || ehGerente) && <th>Ações</th>}</tr></thead><tbody>{profissionais.map((item) => <tr key={item.id}><td>{nomeUsuario(item.usuario_id)}</td><td>{item.area_atuacao}</td><td>{formatarPercentual(item.percentual_padrao)}</td><td>{item.ativo ? "Ativo" : "Inativo"}</td>{(ehAdmin || ehGerente) && <td><div className="piloto-inline-actions">{ehAdmin && <Button size="small" variant="secondary" onClick={() => editar(item)}>Editar</Button>}{ehGerente && <Button size="small" variant="secondary" onClick={() => editar(item)}>Alterar função</Button>}{ehAdmin && <Button size="small" variant={item.ativo ? "danger" : "success"} onClick={() => alternarAtivo(item)}>{item.ativo ? "Desativar" : "Ativar"}</Button>}</div></td>}</tr>)}</tbody></table></div><div className="piloto-mobile-cards">{profissionais.map((item) => <article className="piloto-item-card" key={item.id}><header><strong>{nomeUsuario(item.usuario_id)}</strong><span>{item.ativo ? "Ativo" : "Inativo"}</span></header><dl><div><dt>Área</dt><dd>{item.area_atuacao}</dd></div><div><dt>Percentual padrão</dt><dd>{formatarPercentual(item.percentual_padrao)}</dd></div></dl>{(ehAdmin || ehGerente) && <div className="piloto-inline-actions">{ehAdmin && <Button size="small" variant="secondary" onClick={() => editar(item)}>Editar</Button>}{ehGerente && <Button size="small" variant="secondary" onClick={() => editar(item)}>Alterar função</Button>}{ehAdmin && <Button size="small" variant={item.ativo ? "danger" : "success"} onClick={() => alternarAtivo(item)}>{item.ativo ? "Desativar" : "Ativar"}</Button>}</div>}</article>)}</div></>}
            </SectionCard>
        </main>

    );

}


export default Profissionais;
