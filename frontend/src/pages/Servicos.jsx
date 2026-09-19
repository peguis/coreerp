import { useCallback, useEffect, useState } from "react";

import {
    atualizarServico,
    criarServico,
    desativarServico,
    listarServicos
} from "../services/servicoService";
import { buscarUsuarioLogado } from "../services/usuarioService";
import { getErrorMessage } from "../utils/errors";
import { formatarMoeda } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import SectionCard from "../components/ui/SectionCard";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";
import SearchInput from "../components/forms/SearchInput";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


const FORM_INICIAL = {
    nome: "",
    categoria: "",
    descricao: "",
    preco_padrao: "",
    duracao_minutos: "40",
    requer_recurso: "false",
    tipo_recurso: "",
    modo_selecao_recurso: "AUTOMATICO"
};


function Servicos() {

    const [servicos, setServicos] = useState([]);
    const [usuario, setUsuario] = useState(null);
    const [pesquisa, setPesquisa] = useState("");
    const [form, setForm] = useState(FORM_INICIAL);
    const [editarId, setEditarId] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const carregar = useCallback(async () => {

        try {

            setCarregando(true);
            setErro("");
            const [usuarioDados, dados] = await Promise.all([
                buscarUsuarioLogado(),
                listarServicos({ pagina: 1, limite: 100 })
            ]);
            setUsuario(usuarioDados);
            setServicos(Array.isArray(dados) ? dados : []);

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar os serviços."));

        } finally {

            setCarregando(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    function alterar(campo, valor) {

        setForm((atual) => ({ ...atual, [campo]: valor }));

    }

    function editar(servico) {

        setEditarId(servico.id);
        setForm({
            nome: servico.nome,
            categoria: servico.categoria || "",
            descricao: servico.descricao || "",
            preco_padrao: String(servico.preco_padrao),
            duracao_minutos: String(servico.duracao_minutos || 40),
            requer_recurso: String(Boolean(servico.requer_recurso)),
            tipo_recurso: servico.tipo_recurso || "",
            modo_selecao_recurso: servico.modo_selecao_recurso || "AUTOMATICO"
        });
        setMensagem("");

    }

    function limparForm() {

        setEditarId(null);
        setForm(FORM_INICIAL);

    }

    async function salvar(evento) {

        evento.preventDefault();
        if (salvando) return;
        setErro("");
        setMensagem("");

        if (!form.nome.trim() || !form.categoria.trim() || form.preco_padrao === "" || !form.duracao_minutos || (form.requer_recurso === "true" && !form.tipo_recurso.trim())) {

            setErro("Informe nome e preço padrão do serviço.");
            return;

        }

        try {

            setSalvando(true);
            const dados = {
                nome: form.nome.trim(),
                categoria: form.categoria.trim(),
                descricao: form.descricao.trim() || null,
                preco_padrao: Number(form.preco_padrao),
                duracao_minutos: Number(form.duracao_minutos),
                requer_recurso: form.requer_recurso === "true",
                tipo_recurso: form.requer_recurso === "true" ? form.tipo_recurso.trim().toUpperCase() || null : null,
                modo_selecao_recurso: form.modo_selecao_recurso
            };

            if (editarId) {

                await atualizarServico(editarId, dados);
                setMensagem("Serviço atualizado com sucesso.");

            } else {

                await criarServico(dados);
                setMensagem("Serviço cadastrado com sucesso.");

            }

            limparForm();
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível salvar o serviço."));

        } finally {

            setSalvando(false);

        }

    }

    async function alternarAtivo(servico) {

        try {

            setErro("");
            setMensagem("");
            if (servico.ativo && ["pegs_admin", "admin"].includes(usuario?.perfil)) {
                await desativarServico(servico.id);

            } else {
                await atualizarServico(servico.id, { ativo: !servico.ativo });

            }
            setMensagem(servico.ativo ? "Serviço desativado." : "Serviço ativado.");
            await carregar();

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível alterar o status do serviço."));

        }

    }

    const filtrados = servicos.filter((servico) =>
        `${servico.nome} ${servico.descricao || ""}`
            .toLowerCase()
            .includes(pesquisa.trim().toLowerCase())
    );

    return (

        <main className="piloto-page">
            <PageHeader titulo="Serviços" subtitulo="Cadastre os serviços oferecidos pela empresa." />
            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}
            <FormCard titulo={editarId ? "Editar serviço" : "Novo serviço"} subtitulo="O preço padrão é uma referência para o registro do atendimento.">
                <form className="piloto-form-grid" onSubmit={salvar}>
                    <Input label="Nome" value={form.nome} onChange={(evento) => alterar("nome", evento.target.value)} required />
                    <Input label="Categoria" value={form.categoria} onChange={(evento) => alterar("categoria", evento.target.value)} placeholder="Ex.: Corte, tatuagem ou sessão" required />
                    <Input label="Preço padrão" type="number" min="0" step="0.01" value={form.preco_padrao} onChange={(evento) => alterar("preco_padrao", evento.target.value)} required />
                    <Input label="Duração padrão (minutos)" type="number" min="1" max="1440" value={form.duracao_minutos} onChange={(evento) => alterar("duracao_minutos", evento.target.value)} required />
                    <Select label="Exige recurso físico" value={form.requer_recurso} onChange={(evento) => alterar("requer_recurso", evento.target.value)} options={[{ value: "false", label: "Não" }, { value: "true", label: "Sim" }]} />
                    {form.requer_recurso === "true" && <Input label="Tipo de recurso" value={form.tipo_recurso} onChange={(evento) => alterar("tipo_recurso", evento.target.value)} placeholder="Ex.: MACA" required />}
                    {form.requer_recurso === "true" && <Select label="Seleção do recurso" value={form.modo_selecao_recurso} onChange={(evento) => alterar("modo_selecao_recurso", evento.target.value)} options={[{ value: "AUTOMATICO", label: "Automática" }, { value: "MANUAL", label: "Manual" }]} />}
                    <Textarea className="piloto-form-full" label="Descrição (opcional)" value={form.descricao} onChange={(evento) => alterar("descricao", evento.target.value)} rows={3} />
                    <div className="piloto-form-actions piloto-form-full">
                        {editarId && <Button type="button" variant="secondary" onClick={limparForm}>Cancelar edição</Button>}
                        <Button type="submit" variant="primary" disabled={salvando}>{salvando ? "Salvando..." : editarId ? "Salvar alterações" : "Cadastrar serviço"}</Button>
                    </div>
                </form>
            </FormCard>
            <SectionCard>
                <SearchInput value={pesquisa} onChange={(evento) => setPesquisa(evento.target.value)} placeholder="Pesquisar serviço..." />
            </SectionCard>
            <SectionCard>
                {carregando ? <Loading texto="Carregando serviços..." /> : filtrados.length === 0 ? <div className="piloto-empty">Nenhum serviço encontrado.</div> : (
                    <div className="piloto-table-wrap">
                        <table className="piloto-table"><thead><tr><th>Nome</th><th>Categoria</th><th>Descrição</th><th>Preço padrão</th><th>Duração</th><th>Recurso</th><th>Status</th><th>Ações</th></tr></thead><tbody>{filtrados.map((servico) => <tr key={servico.id}><td>{servico.nome}</td><td>{servico.categoria || "-"}</td><td>{servico.descricao || "-"}</td><td className="monetario">{formatarMoeda(servico.preco_padrao)}</td><td>{servico.duracao_minutos} min</td><td>{servico.requer_recurso ? `${servico.tipo_recurso} · ${servico.modo_selecao_recurso === "MANUAL" ? "manual" : "automático"}` : "-"}</td><td>{servico.ativo ? "Ativo" : "Inativo"}</td><td><div className="piloto-inline-actions"><Button size="small" variant="secondary" onClick={() => editar(servico)}>Editar</Button><Button size="small" variant={servico.ativo ? "danger" : "success"} onClick={() => alternarAtivo(servico)}>{servico.ativo ? "Desativar" : "Ativar"}</Button></div></td></tr>)}</tbody></table>
                    </div>
                )}
                <div className="piloto-mobile-cards">{filtrados.map((servico) => <article className="piloto-item-card" key={servico.id}><header><strong>{servico.nome}</strong><span>{servico.ativo ? "Ativo" : "Inativo"}</span></header><dl><div><dt>Descrição</dt><dd>{servico.descricao || "-"}</dd></div><div><dt>Preço padrão</dt><dd>{formatarMoeda(servico.preco_padrao)}</dd></div><div><dt>Duração</dt><dd>{servico.duracao_minutos} min</dd></div><div><dt>Recurso</dt><dd>{servico.requer_recurso ? `${servico.tipo_recurso} · ${servico.modo_selecao_recurso === "MANUAL" ? "manual" : "automático"}` : "-"}</dd></div></dl><div className="piloto-inline-actions"><Button size="small" variant="secondary" onClick={() => editar(servico)}>Editar</Button><Button size="small" variant={servico.ativo ? "danger" : "success"} onClick={() => alternarAtivo(servico)}>{servico.ativo ? "Desativar" : "Ativar"}</Button></div></article>)}</div>
            </SectionCard>
        </main>

    );

}


export default Servicos;
