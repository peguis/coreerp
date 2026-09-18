import { useCallback, useEffect, useState } from "react";

import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Select from "../components/forms/Select";
import Textarea from "../components/forms/Textarea";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";
import {
    atualizarRecursoAgenda,
    criarRecursoAgenda,
    listarRecursosAgenda
} from "../services/agendaService";
import {
    atualizarServico,
    criarServico,
    listarServicos
} from "../services/servicoService";
import { getErrorMessage } from "../utils/errors";

import "./ConfiguracaoAgenda.css";


const STATUS_RECURSO = [
    { value: "ATIVO", label: "Ativo" },
    { value: "MANUTENCAO", label: "Em manutenção" },
    { value: "INATIVO", label: "Inativo" }
];


const FORM_RECURSO_INICIAL = {
    nome: "",
    tipo: "",
    status: "ATIVO"
};


const FORM_SERVICO_INICIAL = {
    nome: "",
    categoria: "",
    descricao: "",
    preco_padrao: "",
    duracao_minutos: "40",
    requer_recurso: "false",
    tipo_recurso: "",
    modo_selecao_recurso: "AUTOMATICO"
};


function statusRecurso(recurso) {
    return recurso.status || (recurso.ativo ? "ATIVO" : "INATIVO");
}


function rotuloStatusRecurso(status) {
    return STATUS_RECURSO.find((item) => item.value === status)?.label || status;
}


function formatarMoeda(valor) {
    return Number(valor || 0).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}


export default function ConfiguracaoAgenda() {
    const [recursos, setRecursos] = useState([]);
    const [servicos, setServicos] = useState([]);
    const [recursoForm, setRecursoForm] = useState(FORM_RECURSO_INICIAL);
    const [servicoForm, setServicoForm] = useState(FORM_SERVICO_INICIAL);
    const [editarRecursoId, setEditarRecursoId] = useState(null);
    const [editarServicoId, setEditarServicoId] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [salvandoRecurso, setSalvandoRecurso] = useState(false);
    const [salvandoServico, setSalvandoServico] = useState(false);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const carregar = useCallback(async () => {
        try {
            setCarregando(true);
            setErro("");
            const [recursosDados, servicosDados] = await Promise.all([
                listarRecursosAgenda(),
                listarServicos({ pagina: 1, limite: 100 })
            ]);
            setRecursos(Array.isArray(recursosDados) ? recursosDados : []);
            setServicos(Array.isArray(servicosDados) ? servicosDados : []);
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível carregar a configuração da operação."));
        } finally {
            setCarregando(false);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(carregar);
    }, [carregar]);

    function limparRecursoForm() {
        setEditarRecursoId(null);
        setRecursoForm(FORM_RECURSO_INICIAL);
    }

    function limparServicoForm() {
        setEditarServicoId(null);
        setServicoForm(FORM_SERVICO_INICIAL);
    }

    function editarRecurso(recurso) {
        setEditarRecursoId(recurso.id);
        setRecursoForm({
            nome: recurso.nome,
            tipo: recurso.tipo,
            status: statusRecurso(recurso)
        });
        setErro("");
        setMensagem("");
    }

    function editarServico(servico) {
        setEditarServicoId(servico.id);
        setServicoForm({
            nome: servico.nome,
            categoria: servico.categoria || "",
            descricao: servico.descricao || "",
            preco_padrao: String(servico.preco_padrao ?? ""),
            duracao_minutos: String(servico.duracao_minutos || 40),
            requer_recurso: String(Boolean(servico.requer_recurso)),
            tipo_recurso: servico.tipo_recurso || "",
            modo_selecao_recurso: servico.modo_selecao_recurso || "AUTOMATICO"
        });
        setErro("");
        setMensagem("");
    }

    async function salvarRecurso(evento) {
        evento.preventDefault();
        if (salvandoRecurso) return;
        if (!recursoForm.nome.trim() || !recursoForm.tipo.trim()) {
            setErro("Informe o nome e o tipo do recurso.");
            return;
        }
        try {
            setSalvandoRecurso(true);
            setErro("");
            const dados = {
                nome: recursoForm.nome.trim(),
                tipo: recursoForm.tipo.trim().toUpperCase(),
                status: recursoForm.status
            };
            if (editarRecursoId) {
                await atualizarRecursoAgenda(editarRecursoId, dados);
                setMensagem("Recurso atualizado com sucesso.");
            } else {
                await criarRecursoAgenda(dados);
                setMensagem("Recurso cadastrado com sucesso.");
            }
            limparRecursoForm();
            await carregar();
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível salvar o recurso."));
        } finally {
            setSalvandoRecurso(false);
        }
    }

    async function alterarStatusRecurso(recurso, status) {
        try {
            setErro("");
            await atualizarRecursoAgenda(recurso.id, { status });
            setMensagem(`Recurso ${rotuloStatusRecurso(status).toLowerCase()}.`);
            await carregar();
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível alterar o status do recurso."));
        }
    }

    async function salvarServico(evento) {
        evento.preventDefault();
        if (salvandoServico) return;
        if (!servicoForm.nome.trim() || !servicoForm.categoria.trim()) {
            setErro("Informe o nome e a categoria do serviço.");
            return;
        }
        if (servicoForm.preco_padrao === "" || !servicoForm.duracao_minutos) {
            setErro("Informe o preço e a duração do serviço.");
            return;
        }
        if (servicoForm.requer_recurso === "true" && !servicoForm.tipo_recurso.trim()) {
            setErro("Informe o tipo de recurso necessário.");
            return;
        }
        try {
            setSalvandoServico(true);
            setErro("");
            const dados = {
                nome: servicoForm.nome.trim(),
                categoria: servicoForm.categoria.trim(),
                descricao: servicoForm.descricao.trim() || null,
                preco_padrao: Number(servicoForm.preco_padrao),
                duracao_minutos: Number(servicoForm.duracao_minutos),
                requer_recurso: servicoForm.requer_recurso === "true",
                tipo_recurso: servicoForm.requer_recurso === "true"
                    ? servicoForm.tipo_recurso.trim().toUpperCase()
                    : null,
                modo_selecao_recurso: servicoForm.modo_selecao_recurso
            };
            if (editarServicoId) {
                await atualizarServico(editarServicoId, dados);
                setMensagem("Serviço atualizado com sucesso.");
            } else {
                await criarServico(dados);
                setMensagem("Serviço cadastrado com sucesso.");
            }
            limparServicoForm();
            await carregar();
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível salvar o serviço."));
        } finally {
            setSalvandoServico(false);
        }
    }

    async function alternarServico(servico) {
        try {
            setErro("");
            await atualizarServico(servico.id, { ativo: !servico.ativo });
            setMensagem(servico.ativo ? "Serviço desativado sem apagar o histórico." : "Serviço ativado.");
            await carregar();
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível alterar o status do serviço."));
        }
    }

    return (
        <main className="configuracao-agenda-page">
            <PageHeader
                titulo="Configuração da operação"
                subtitulo="Cadastre os recursos e serviços reais da HYPE. Alterações futuras não reescrevem o histórico."
            />
            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}

            <div className="configuracao-agenda-intro">
                <strong>Área gerencial</strong>
                <span>Somente ADMIN/DONO e GERENTE podem alterar recursos, manutenção, preços e durações.</span>
            </div>

            <div className="configuracao-agenda-grid">
                <FormCard
                    titulo={editarRecursoId ? "Editar recurso" : "Novo recurso"}
                    subtitulo="Use um nome individual para cada maca, cadeira ou estação."
                >
                    <form className="configuracao-agenda-form" onSubmit={salvarRecurso}>
                        <Input label="Identificação" value={recursoForm.nome} onChange={(evento) => setRecursoForm((atual) => ({ ...atual, nome: evento.target.value }))} placeholder="Ex.: Cadeira 1" required />
                        <Input label="Tipo" value={recursoForm.tipo} onChange={(evento) => setRecursoForm((atual) => ({ ...atual, tipo: evento.target.value }))} placeholder="Ex.: CADEIRA" required />
                        <Select label="Status" value={recursoForm.status} onChange={(evento) => setRecursoForm((atual) => ({ ...atual, status: evento.target.value }))} options={STATUS_RECURSO} required />
                        <div className="configuracao-agenda-form-actions">
                            {editarRecursoId && <Button type="button" variant="secondary" onClick={limparRecursoForm}>Cancelar</Button>}
                            <Button type="submit" variant="primary" loading={salvandoRecurso}>{editarRecursoId ? "Salvar recurso" : "Cadastrar recurso"}</Button>
                        </div>
                    </form>
                </FormCard>

                <SectionCard titulo="Recursos cadastrados" subtitulo="Recursos em manutenção ou inativos não podem receber novos agendamentos.">
                    {carregando ? <Loading texto="Carregando recursos..." /> : recursos.length === 0 ? <div className="configuracao-agenda-empty">Nenhum recurso cadastrado.</div> : (
                        <div className="configuracao-agenda-lista">
                            {recursos.map((recurso) => {
                                const status = statusRecurso(recurso);
                                return (
                                    <article className={`configuracao-agenda-item recurso-status-${status.toLowerCase()}`} key={recurso.id}>
                                        <div>
                                            <strong>{recurso.nome}</strong>
                                            <span>{recurso.tipo} · {rotuloStatusRecurso(status)}</span>
                                        </div>
                                        <div className="configuracao-agenda-actions">
                                            <Button size="small" variant="secondary" onClick={() => editarRecurso(recurso)}>Editar</Button>
                                            {status !== "ATIVO" && <Button size="small" variant="success" onClick={() => alterarStatusRecurso(recurso, "ATIVO")}>Ativar</Button>}
                                            {status !== "MANUTENCAO" && <Button size="small" variant="secondary" onClick={() => alterarStatusRecurso(recurso, "MANUTENCAO")}>Manutenção</Button>}
                                            {status !== "INATIVO" && <Button size="small" variant="danger" onClick={() => alterarStatusRecurso(recurso, "INATIVO")}>Desativar</Button>}
                                        </div>
                                    </article>
                                );
                            })}
                        </div>
                    )}
                </SectionCard>
            </div>

            <FormCard
                titulo={editarServicoId ? "Editar serviço" : "Novo serviço"}
                subtitulo="A duração inicial sugerida é de 40 minutos para facilitar o cadastro de corte; o gerente pode alterá-la."
            >
                <form className="configuracao-agenda-form configuracao-agenda-form-servico" onSubmit={salvarServico}>
                    <Input label="Nome do serviço" value={servicoForm.nome} onChange={(evento) => setServicoForm((atual) => ({ ...atual, nome: evento.target.value }))} placeholder="Ex.: Corte masculino" required />
                    <Input label="Categoria" value={servicoForm.categoria} onChange={(evento) => setServicoForm((atual) => ({ ...atual, categoria: evento.target.value }))} placeholder="Ex.: Barbearia ou Tattoo" required />
                    <Input label="Preço padrão" type="number" min="0" step="0.01" value={servicoForm.preco_padrao} onChange={(evento) => setServicoForm((atual) => ({ ...atual, preco_padrao: evento.target.value }))} placeholder="0,00" required />
                    <Input label="Duração média (minutos)" type="number" min="1" max="1440" value={servicoForm.duracao_minutos} onChange={(evento) => setServicoForm((atual) => ({ ...atual, duracao_minutos: evento.target.value }))} required />
                    <Select label="Precisa de recurso físico?" value={servicoForm.requer_recurso} onChange={(evento) => setServicoForm((atual) => ({ ...atual, requer_recurso: evento.target.value }))} options={[{ value: "false", label: "Não" }, { value: "true", label: "Sim" }]} />
                    {servicoForm.requer_recurso === "true" && <Input label="Tipo de recurso necessário" value={servicoForm.tipo_recurso} onChange={(evento) => setServicoForm((atual) => ({ ...atual, tipo_recurso: evento.target.value }))} placeholder="Ex.: MACA ou CADEIRA" required />}
                    {servicoForm.requer_recurso === "true" && <Select label="Seleção do recurso" value={servicoForm.modo_selecao_recurso} onChange={(evento) => setServicoForm((atual) => ({ ...atual, modo_selecao_recurso: evento.target.value }))} options={[{ value: "AUTOMATICO", label: "Automática" }, { value: "MANUAL", label: "Manual" }]} />}
                    <Textarea className="configuracao-agenda-form-full" label="Descrição (opcional)" value={servicoForm.descricao} onChange={(evento) => setServicoForm((atual) => ({ ...atual, descricao: evento.target.value }))} rows={3} />
                    <div className="configuracao-agenda-form-actions configuracao-agenda-form-full">
                        {editarServicoId && <Button type="button" variant="secondary" onClick={limparServicoForm}>Cancelar</Button>}
                        <Button type="submit" variant="primary" loading={salvandoServico}>{editarServicoId ? "Salvar serviço" : "Cadastrar serviço"}</Button>
                    </div>
                </form>
            </FormCard>

            <SectionCard titulo="Serviços cadastrados" subtitulo="Preço e duração novos valem para os próximos agendamentos; os antigos guardam seus próprios snapshots.">
                {carregando ? <Loading texto="Carregando serviços..." /> : servicos.length === 0 ? <div className="configuracao-agenda-empty">Nenhum serviço cadastrado.</div> : (
                    <div className="configuracao-agenda-tabela-wrap">
                        <table className="configuracao-agenda-tabela">
                            <thead><tr><th>Serviço</th><th>Categoria</th><th>Preço</th><th>Duração</th><th>Recurso</th><th>Status</th><th>Ações</th></tr></thead>
                            <tbody>{servicos.map((servico) => <tr key={servico.id}>
                                <td><strong>{servico.nome}</strong></td>
                                <td>{servico.categoria || "-"}</td>
                                <td>{formatarMoeda(servico.preco_padrao)}</td>
                                <td>{servico.duracao_minutos} min</td>
                                <td>{servico.requer_recurso ? `${servico.tipo_recurso} · ${servico.modo_selecao_recurso === "MANUAL" ? "manual" : "automático"}` : "Não exige"}</td>
                                <td>{servico.ativo ? "Ativo" : "Inativo"}</td>
                                <td><div className="configuracao-agenda-actions"><Button size="small" variant="secondary" onClick={() => editarServico(servico)}>Editar</Button><Button size="small" variant={servico.ativo ? "danger" : "success"} onClick={() => alternarServico(servico)}>{servico.ativo ? "Desativar" : "Ativar"}</Button></div></td>
                            </tr>)}</tbody>
                        </table>
                    </div>
                )}
            </SectionCard>
        </main>
    );
}
