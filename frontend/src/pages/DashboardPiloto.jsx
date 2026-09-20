import { useCallback, useEffect, useMemo, useState } from "react";
import {
    AlertTriangle,
    ArrowDown,
    ArrowUp,
    Banknote,
    CalendarCheck,
    ChevronRight,
    CircleDollarSign,
    Clock3,
    TrendingUp,
    WalletCards,
} from "lucide-react";
import { Link } from "react-router-dom";

import { obterDashboardPiloto } from "../services/dashboardService";
import { getErrorMessage } from "../utils/errors";
import { formatarData, formatarDataHora, formatarMoeda } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import Input from "../components/forms/Input";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


const DIAS_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];


function DashboardPiloto() {

    const [dados, setDados] = useState(null);
    const [dataInicio, setDataInicio] = useState("");
    const [dataFim, setDataFim] = useState("");
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState("");

    const carregar = useCallback(async (params = {}) => {
        try {
            setCarregando(true);
            setErro("");
            setDados(await obterDashboardPiloto(params));
        } catch (error) {
            setErro(getErrorMessage(error, "Não foi possível carregar o dashboard."));
        } finally {
            setCarregando(false);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(() => carregar());
    }, [carregar]);

    function filtrar(evento) {
        evento.preventDefault();
        const params = {};
        if (dataInicio) params.data_inicio = dataInicio;
        if (dataFim) params.data_fim = dataFim;
        carregar(params);
    }

    function percentual(valor, total) {
        const base = Number(total || 0);
        return base > 0 ? Math.round((Number(valor || 0) / base) * 100) : 0;
    }

    const grafico = useMemo(() => {
        const valores = Array.from({ length: 7 }, (_, diaSemana) => {
            const item = dados?.faturamento_por_dia_semana?.find(
                (dia) => Number(dia.dia_semana) === diaSemana
            );
            return {
                diaSemana,
                quantidade: Number(item?.quantidade_atendimentos || 0),
                valor: Number(item?.faturamento_bruto || 0),
            };
        });
        const maiorValor = Math.max(...valores.map((item) => item.valor), 0);
        const totalGrafico = valores.reduce((total, item) => total + item.valor, 0);
        const diaDestaque = maiorValor > 0
            ? valores.find((item) => item.valor === maiorValor)?.diaSemana
            : (new Date().getDay() + 6) % 7;
        return { valores, maiorValor, totalGrafico, diaDestaque };
    }, [dados]);

    const ultimosAtendimentos = dados?.ultimos_atendimentos || [];

    return (
        <main className="piloto-page dashboard-piloto-page">
            <PageHeader
                titulo="Dashboard"
                subtitulo="Aqui está o resumo da operação da empresa de hoje."
            >
                <form className="dashboard-period-form" onSubmit={filtrar}>
                    <Input
                        label="Data inicial"
                        type="date"
                        value={dataInicio}
                        onChange={(evento) => setDataInicio(evento.target.value)}
                    />
                    <Input
                        label="Data final"
                        type="date"
                        value={dataFim}
                        onChange={(evento) => setDataFim(evento.target.value)}
                    />
                    <Button type="submit" variant="primary" loading={carregando && Boolean(dados)}>
                        Atualizar
                    </Button>
                </form>
            </PageHeader>

            {erro && <Mensagem tipo="erro" texto={erro} />}
            {carregando && !dados && <Loading texto="Carregando dashboard..." />}

            {dados && (
                <>
                    <p className="piloto-periodo">
                        Período: {formatarData(dados.data_inicio)} até {formatarData(dados.data_fim)}
                    </p>

                    <section className="piloto-kpi-grid" aria-label="Resumo do período">
                        <article className="piloto-kpi-card piloto-kpi-gold">
                            <span><CircleDollarSign size={17} /> Faturamento bruto</span>
                            <strong>{formatarMoeda(dados.faturamento_bruto)}</strong>
                            <small><TrendingUp size={13} /> Período selecionado</small>
                        </article>
                        <article className="piloto-kpi-card piloto-kpi-cyan">
                            <span><CalendarCheck size={17} /> Atendimentos</span>
                            <strong>{dados.total_atendimentos}</strong>
                            <small><ArrowUp size={13} /> Registros realizados</small>
                        </article>
                        <article className="piloto-kpi-card piloto-kpi-green">
                            <span><Banknote size={17} /> Valor da casa</span>
                            <strong>{formatarMoeda(dados.valor_casa)}</strong>
                            <small>{percentual(dados.valor_casa, dados.faturamento_bruto)}% do faturamento bruto</small>
                        </article>
                        <article className="piloto-kpi-card piloto-kpi-red">
                            <span><Clock3 size={17} /> Repasses pendentes</span>
                            <strong>{formatarMoeda(dados.total_pendente_repasses)}</strong>
                            <small>Aguardando baixa</small>
                        </article>
                    </section>

                    <section className="piloto-visual-grid">
                        <article className="piloto-visual-card piloto-chart-card">
                            <header>
                                <div>
                                    <span className="piloto-overline">FATURAMENTO DO PERÍODO</span>
                                    <h2>Faturamento no período</h2>
                                    <p>Valores referentes ao período selecionado acima.</p>
                                </div>
                                <span className="piloto-card-period">Período selecionado</span>
                            </header>
                            <div className="piloto-chart-total" aria-label={`Total do gráfico: ${formatarMoeda(grafico.totalGrafico)}`}>
                                {formatarMoeda(grafico.totalGrafico)}
                            </div>
                            <div className="piloto-bar-chart" aria-label={`Faturamento por dia da semana. Soma: ${formatarMoeda(grafico.totalGrafico)}`}>
                                {grafico.valores.map((item) => {
                                    const altura = grafico.maiorValor > 0
                                        ? Math.max((item.valor / grafico.maiorValor) * 100, item.valor > 0 ? 8 : 3)
                                        : 3;
                                    const ativo = item.diaSemana === grafico.diaDestaque;
                                    return (
                                        <div className={`piloto-bar-column ${ativo ? "is-highlighted" : ""}`} key={item.diaSemana}>
                                            <span className="piloto-bar-tooltip">{formatarMoeda(item.valor)} · {item.quantidade} atend.</span>
                                            <div className="piloto-bar-track">
                                                <span style={{ height: `${altura}%` }} title={`${DIAS_SEMANA[item.diaSemana]}: ${formatarMoeda(item.valor)} — ${item.quantidade} atendimentos`} />
                                            </div>
                                            <strong>{DIAS_SEMANA[item.diaSemana]}</strong>
                                        </div>
                                    );
                                })}
                            </div>
                            <div className="piloto-chart-legend">
                                <span><i className="piloto-dot piloto-dot-gold" /> Faturamento bruto</span>
                                <span><i className="piloto-dot piloto-dot-muted" /> Sem faturamento</span>
                            </div>
                        </article>

                        <article className="piloto-visual-card piloto-attention-card">
                            <header>
                                <div>
                                    <span className="piloto-overline">VISÃO OPERACIONAL</span>
                                    <h2>O que precisa da sua atenção</h2>
                                </div>
                                <AlertTriangle size={19} />
                            </header>
                            <Link className="piloto-attention-item" to="/repasses">
                                <span className={`piloto-attention-icon ${dados.total_pendente_repasses > 0 ? "is-danger" : "is-success"}`}>
                                    {dados.total_pendente_repasses > 0 ? "!" : "✓"}
                                </span>
                                <span className="piloto-attention-copy">
                                    <strong>{dados.total_pendente_repasses > 0 ? "Repasses pendentes" : "Repasses em dia"}</strong>
                                    <small>{dados.total_pendente_repasses > 0 ? `${formatarMoeda(dados.total_pendente_repasses)} aguardando baixa.` : "Nenhum valor pendente no período."}</small>
                                </span>
                                <ChevronRight size={17} aria-hidden="true" />
                            </Link>
                            <Link className="piloto-attention-item" to="/atendimentos">
                                <span className="piloto-attention-icon piloto-attention-neutral"><CalendarCheck size={14} /></span>
                                <span className="piloto-attention-copy">
                                    <strong>Atendimentos registrados</strong>
                                    <small>{dados.total_atendimentos} no período selecionado.</small>
                                </span>
                                <ChevronRight size={17} aria-hidden="true" />
                            </Link>
                        </article>
                    </section>

                    <section className="piloto-finance-strip" aria-label="Resumo de caixa">
                        <div className="piloto-strip-item"><span>Entradas de caixa <ArrowUp size={14} /></span><strong>{formatarMoeda(dados.entradas_caixa_piloto)}</strong></div>
                        <div className="piloto-strip-item"><span>Saídas de caixa <ArrowDown size={14} /></span><strong>{formatarMoeda(dados.saidas_caixa_piloto)}</strong></div>
                        <div className="piloto-strip-item"><span>Saldo do caixa <small>(não é lucro)</small></span><strong>{formatarMoeda(dados.saldo_caixa_piloto)}</strong></div>
                        <div className="piloto-strip-item"><span>Total repassado <WalletCards size={14} /></span><strong>{formatarMoeda(dados.total_repassado)}</strong></div>
                    </section>

                    <section className="piloto-subsection piloto-recent-section">
                        <header className="piloto-section-header">
                            <div>
                                <span className="piloto-overline">OPERAÇÃO</span>
                                <h2 className="piloto-section-title">Últimos atendimentos</h2>
                            </div>
                            <Link className="piloto-section-link" to="/atendimentos">Ver todos <ChevronRight size={15} /></Link>
                        </header>
                        {ultimosAtendimentos.length === 0 ? (
                            <div className="piloto-empty">Nenhum atendimento registrado no período selecionado.</div>
                        ) : (
                            <>
                                <div className="piloto-table-wrap">
                                    <table className="piloto-table piloto-recent-table">
                                        <thead><tr><th>Profissional</th><th>Serviço</th><th>Horário</th><th>Status</th></tr></thead>
                                        <tbody>{ultimosAtendimentos.map((item) => <tr key={item.atendimento_id}><td>{item.profissional_nome}</td><td>{item.servico_nome}</td><td>{formatarDataHora(item.realizado_em)}</td><td><span className="hype-status hype-status-pago">Concluído</span></td></tr>)}</tbody>
                                    </table>
                                </div>
                                <div className="piloto-mobile-cards piloto-recent-mobile">{ultimosAtendimentos.map((item) => <article className="piloto-item-card" key={item.atendimento_id}><header><strong>{item.profissional_nome}</strong><span className="hype-status hype-status-pago">Concluído</span></header><dl><div><dt>Serviço</dt><dd>{item.servico_nome}</dd></div><div><dt>Horário</dt><dd>{formatarDataHora(item.realizado_em)}</dd></div></dl></article>)}</div>
                            </>
                        )}
                    </section>
                </>
            )}
        </main>
    );
}


export default DashboardPiloto;
