import { useCallback, useEffect, useMemo, useState } from "react";

import { listarUsuarios } from "../services/usuarioService";
import { listarProfissionais } from "../services/profissionalService";
import { listarAtendimentos } from "../services/atendimentoService";
import { criarRepasse, listarPendencias, listarRepasses } from "../services/repasseService";
import { getErrorMessage } from "../utils/errors";
import { formatarMoeda, formatarDataHora } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import Select from "../components/forms/Select";
import Input from "../components/forms/Input";
import Textarea from "../components/forms/Textarea";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


const FORMAS = [
    { value: "PIX", label: "PIX" },
    { value: "DINHEIRO", label: "Dinheiro" },
    { value: "TRANSFERENCIA", label: "Transferência" }
];


function Repasses() {

    const [profissionais, setProfissionais] = useState([]);
    const [usuarios, setUsuarios] = useState([]);
    const [repasses, setRepasses] = useState([]);
    const [pendencia, setPendencia] = useState(null);
    const [atendimentos, setAtendimentos] = useState([]);
    const [profissionalId, setProfissionalId] = useState("");
    const [formaPagamento, setFormaPagamento] = useState("");
    const [observacao, setObservacao] = useState("");
    const [valores, setValores] = useState({});
    const [carregando, setCarregando] = useState(true);
    const [carregandoPendencia, setCarregandoPendencia] = useState(false);
    const [salvando, setSalvando] = useState(false);
    const [erro, setErro] = useState("");
    const [mensagem, setMensagem] = useState("");

    const carregar = useCallback(async () => {

        try {

            setCarregando(true);
            setErro("");
            const [profissionaisDados, usuariosDados, repassesDados] = await Promise.all([
                listarProfissionais({ ativo: true, pagina: 1, limite: 100 }),
                listarUsuarios(),
                listarRepasses({ pagina: 1, limite: 100 })
            ]);
            setProfissionais(Array.isArray(profissionaisDados) ? profissionaisDados : []);
            setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);
            setRepasses(Array.isArray(repassesDados) ? repassesDados : []);

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar os repasses."));

        } finally {

            setCarregando(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    const nomes = useMemo(() => new Map(profissionais.map((item) => [
        item.id,
        usuarios.find((usuario) => usuario.id === item.usuario_id)?.nome || `Profissional #${item.id}`
    ])), [profissionais, usuarios]);

    async function selecionarProfissional(evento) {

        const id = evento.target.value;
        setProfissionalId(id);
        setPendencia(null);
        setAtendimentos([]);
        setValores({});
        setErro("");

        if (!id) return;

        try {

            setCarregandoPendencia(true);
            const [pendenciasDados, atendimentosDados] = await Promise.all([
                listarPendencias(Number(id)),
                listarAtendimentos({ profissional_id: Number(id), pagina: 1, limite: 100 })
            ]);
            const pendenciaEncontrada = pendenciasDados.find(
                (item) => item.profissional_id === Number(id)
            );
            setPendencia(pendenciaEncontrada ? {
                ...pendenciaEncontrada,
                atendimentos: pendenciaEncontrada.atendimentos.filter(
                    (item) => Number(item.valor_pendente) > 0
                )
            } : null);
            setAtendimentos(Array.isArray(atendimentosDados) ? atendimentosDados : []);

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar as pendências."));

        } finally {

            setCarregandoPendencia(false);

        }

    }

    function nomeServico(id) {

        const atendimento = atendimentos.find((item) => item.id === id);
        return atendimento ? `Atendimento #${id}` : `Atendimento #${id}`;

    }

    function alterarValor(item, valor) {

        setValores((atual) => ({ ...atual, [item.atendimento_id]: valor }));

    }

    function valorInvalido(item) {

        const valor = valores[item.atendimento_id];
        return valor !== undefined && valor !== "" && Number(valor) > Number(item.valor_pendente);

    }

    async function salvar(evento) {

        evento.preventDefault();
        if (salvando) return;
        setErro("");
        setMensagem("");

        if (!profissionalId || !formaPagamento) {

            setErro("Selecione o profissional e a forma de pagamento.");
            return;

        }

        const itens = (pendencia?.atendimentos || [])
            .filter((item) => valores[item.atendimento_id] !== undefined && valores[item.atendimento_id] !== "")
            .map((item) => ({
                atendimento_id: item.atendimento_id,
                valor: Number(valores[item.atendimento_id])
            }));

        if (!itens.length) {

            setErro("Informe ao menos um valor de repasse.");
            return;

        }

        if (pendencia.atendimentos.some(valorInvalido)) {

            setErro("O valor informado não pode ser maior que a pendência do atendimento.");
            return;

        }

        if (itens.some((item) => !Number.isFinite(item.valor) || item.valor <= 0)) {

            setErro("Os valores de repasse devem ser maiores que zero.");
            return;

        }

        try {

            setSalvando(true);
            await criarRepasse({
                profissional_id: Number(profissionalId),
                forma_pagamento: formaPagamento,
                observacao: observacao.trim() || null,
                itens
            });
            setMensagem("Repasse registrado com sucesso.");
            setFormaPagamento("");
            setObservacao("");
            setValores({});
            await carregar();
            await selecionarProfissional({ target: { value: profissionalId } });

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível registrar o repasse."));

        } finally {

            setSalvando(false);

        }

    }

    return (

        <main className="piloto-page">
            <PageHeader titulo="Repasses" subtitulo="Registre pagamentos usando as pendências e snapshots retornados pelo backend." />
            {(erro || mensagem) && <Mensagem tipo={erro ? "erro" : "sucesso"} texto={erro || mensagem} />}
            <SectionCard>
                <Select label="Profissional" value={profissionalId} onChange={selecionarProfissional} options={profissionais.map((item) => ({ value: item.id, label: nomes.get(item.id) }))} required />
            </SectionCard>
            {carregandoPendencia && <Loading texto="Carregando pendências..." />}
            {profissionalId && !carregandoPendencia && (
                <SectionCard>
                    <h2 className="piloto-section-title">Pendências de {nomes.get(Number(profissionalId))}</h2>
                    {!pendencia || pendencia.atendimentos.length === 0 ? <div className="piloto-empty">Nenhuma pendência para este profissional.</div> : <form onSubmit={salvar}>
                        <div className="piloto-table-wrap"><table className="piloto-table"><thead><tr><th>Atendimento</th><th>Realizado em</th><th className="monetario">Devido</th><th className="monetario">Repassado</th><th className="monetario">Pendente</th><th>Alocar</th></tr></thead><tbody>{pendencia.atendimentos.map((item) => <tr key={item.atendimento_id}><td>{nomeServico(item.atendimento_id)}</td><td>{formatarDataHora(item.realizado_em)}</td><td className="monetario">{formatarMoeda(item.valor_profissional)}</td><td className="monetario">{formatarMoeda(item.valor_repassado)}</td><td className="monetario">{formatarMoeda(item.valor_pendente)}</td><td><Input type="number" min="0.01" max={item.valor_pendente} step="0.01" value={valores[item.atendimento_id] || ""} onChange={(evento) => alterarValor(item, evento.target.value)} error={valorInvalido(item) ? "Acima da pendência" : ""} /></td></tr>)}</tbody></table></div>
                        <div className="piloto-mobile-cards">{pendencia.atendimentos.map((item) => <article className="piloto-item-card" key={item.atendimento_id}><header><strong>{nomeServico(item.atendimento_id)}</strong><span>{formatarDataHora(item.realizado_em)}</span></header><dl><div><dt>Devido</dt><dd>{formatarMoeda(item.valor_profissional)}</dd></div><div><dt>Repassado</dt><dd>{formatarMoeda(item.valor_repassado)}</dd></div><div><dt>Pendente</dt><dd>{formatarMoeda(item.valor_pendente)}</dd></div></dl><Input label="Valor a alocar" type="number" min="0.01" max={item.valor_pendente} step="0.01" value={valores[item.atendimento_id] || ""} onChange={(evento) => alterarValor(item, evento.target.value)} error={valorInvalido(item) ? "Acima da pendência" : ""} /></article>)}</div>
                        <div className="piloto-form-grid"><Select label="Forma de pagamento" value={formaPagamento} onChange={(evento) => setFormaPagamento(evento.target.value)} options={FORMAS} required /><Textarea label="Observação (opcional)" value={observacao} onChange={(evento) => setObservacao(evento.target.value)} rows={3} /><div className="piloto-form-actions piloto-form-full"><Button type="submit" variant="primary" disabled={salvando}>{salvando ? "Registrando..." : "Registrar repasse"}</Button></div></div>
                    </form>}
                </SectionCard>
            )}
            <SectionCard>
                <h2 className="piloto-section-title">Repasses realizados</h2>
                {carregando ? <Loading texto="Carregando repasses..." /> : repasses.length === 0 ? <div className="piloto-empty">Nenhum repasse realizado.</div> : <><div className="piloto-table-wrap"><table className="piloto-table"><thead><tr><th>Data</th><th>Profissional</th><th className="monetario">Valor</th><th>Forma</th><th>Observação</th></tr></thead><tbody>{repasses.map((item) => <tr key={item.id}><td>{formatarDataHora(item.pago_em)}</td><td>{nomes.get(item.profissional_id) || `Profissional #${item.profissional_id}`}</td><td className="monetario">{formatarMoeda(item.valor)}</td><td>{item.forma_pagamento}</td><td>{item.observacao || "-"}</td></tr>)}</tbody></table></div><div className="piloto-mobile-cards">{repasses.map((item) => <article className="piloto-item-card" key={item.id}><header><strong>{nomes.get(item.profissional_id) || `Profissional #${item.profissional_id}`}</strong><span>{formatarDataHora(item.pago_em)}</span></header><dl><div><dt>Valor</dt><dd>{formatarMoeda(item.valor)}</dd></div><div><dt>Forma</dt><dd>{item.forma_pagamento}</dd></div><div><dt>Observação</dt><dd>{item.observacao || "-"}</dd></div></dl></article>)}</div></>}
            </SectionCard>
        </main>

    );

}


export default Repasses;
