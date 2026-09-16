import { useCallback, useEffect, useState } from "react";

import { obterDashboardPiloto } from "../services/dashboardService";
import { getErrorMessage } from "../utils/errors";
import { formatarMoeda, formatarData } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


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

            setErro(getErrorMessage(error, "Não foi possível carregar o dashboard do piloto."));

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

    return (

        <main className="piloto-page">

            <PageHeader
                titulo="Dashboard do piloto"
                subtitulo="Produção, comissões e caixa da operação Barbearia + Tattoo"
            />

            <FormCard
                titulo="Período"
                subtitulo="O backend consolida os valores do período informado."
            >
                <form className="piloto-toolbar" onSubmit={filtrar}>
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
                    <Button type="submit" variant="primary">Atualizar</Button>
                </form>
            </FormCard>

            {erro && <Mensagem tipo="erro" texto={erro} />}
            {carregando && !dados && <Loading texto="Carregando dashboard do piloto..." />}

            {dados && (

                <>
                    <p className="piloto-periodo">
                        Período: {formatarData(dados.data_inicio)} até {formatarData(dados.data_fim)}
                    </p>

                    <section>
                        <h2 className="piloto-section-title">Produção e comissões</h2>
                        <div className="piloto-grid">
                            <div className="piloto-metric"><span>Atendimentos</span><strong>{dados.total_atendimentos}</strong></div>
                            <div className="piloto-metric"><span>Faturamento bruto</span><strong>{formatarMoeda(dados.faturamento_bruto)}</strong></div>
                            <div className="piloto-metric"><span>Valor profissionais</span><strong>{formatarMoeda(dados.valor_profissionais)}</strong></div>
                            <div className="piloto-metric"><span>Valor casa</span><strong>{formatarMoeda(dados.valor_casa)}</strong></div>
                            <div className="piloto-metric"><span>Valor repassado</span><strong>{formatarMoeda(dados.total_repassado)}</strong></div>
                            <div className="piloto-metric"><span>Valor pendente</span><strong>{formatarMoeda(dados.total_pendente_repasses)}</strong></div>
                        </div>
                    </section>

                    <section>
                        <h2 className="piloto-section-title">Caixa do piloto</h2>
                        <div className="piloto-grid">
                            <div className="piloto-metric"><span>Entradas de caixa do piloto</span><strong>{formatarMoeda(dados.entradas_caixa_piloto)}</strong></div>
                            <div className="piloto-metric"><span>Saídas de caixa do piloto</span><strong>{formatarMoeda(dados.saidas_caixa_piloto)}</strong></div>
                            <div className="piloto-metric"><span>Saldo de caixa do piloto (não é lucro)</span><strong>{formatarMoeda(dados.saldo_caixa_piloto)}</strong></div>
                        </div>
                    </section>

                    <section className="piloto-subsection">
                        <h2 className="piloto-section-title">Por profissional</h2>
                        <div className="piloto-table-wrap">
                            <table className="piloto-table">
                                <thead><tr><th>Profissional</th><th>Área</th><th className="numerico">Atendimentos</th><th className="monetario">Bruto</th><th className="monetario">Valor profissional</th><th className="monetario">Casa</th><th className="monetario">Repassado</th><th className="monetario">Pendente</th></tr></thead>
                                <tbody>{dados.por_profissional.map((item) => <tr key={item.profissional_id}><td>{item.nome}</td><td>{item.area_atuacao}</td><td className="numerico">{item.quantidade_atendimentos}</td><td className="monetario">{formatarMoeda(item.faturamento_bruto)}</td><td className="monetario">{formatarMoeda(item.valor_profissional)}</td><td className="monetario">{formatarMoeda(item.valor_casa)}</td><td className="monetario">{formatarMoeda(item.valor_repassado)}</td><td className="monetario">{formatarMoeda(item.valor_pendente)}</td></tr>)}</tbody>
                            </table>
                        </div>
                        <div className="piloto-mobile-cards">{dados.por_profissional.map((item) => <article className="piloto-item-card" key={item.profissional_id}><header><strong>{item.nome}</strong><span>{item.area_atuacao}</span></header><dl><div><dt>Atendimentos</dt><dd>{item.quantidade_atendimentos}</dd></div><div><dt>Bruto</dt><dd>{formatarMoeda(item.faturamento_bruto)}</dd></div><div><dt>Valor profissional</dt><dd>{formatarMoeda(item.valor_profissional)}</dd></div><div><dt>Casa</dt><dd>{formatarMoeda(item.valor_casa)}</dd></div><div><dt>Repassado</dt><dd>{formatarMoeda(item.valor_repassado)}</dd></div><div><dt>Pendente</dt><dd>{formatarMoeda(item.valor_pendente)}</dd></div></dl></article>)}</div>
                    </section>

                    <section className="piloto-grid">
                        <div className="piloto-subsection"><h2 className="piloto-section-title">Por serviço</h2><div className="piloto-table-wrap"><table className="piloto-table"><thead><tr><th>Serviço</th><th className="numerico">Quantidade</th><th className="monetario">Faturamento bruto</th></tr></thead><tbody>{dados.por_servico.map((item) => <tr key={item.servico_id}><td>{item.nome}</td><td className="numerico">{item.quantidade}</td><td className="monetario">{formatarMoeda(item.faturamento_bruto)}</td></tr>)}</tbody></table></div><div className="piloto-mobile-cards">{dados.por_servico.map((item) => <article className="piloto-item-card" key={item.servico_id}><header><strong>{item.nome}</strong></header><dl><div><dt>Quantidade</dt><dd>{item.quantidade}</dd></div><div><dt>Faturamento bruto</dt><dd>{formatarMoeda(item.faturamento_bruto)}</dd></div></dl></article>)}</div></div>
                        <div className="piloto-subsection"><h2 className="piloto-section-title">Por forma de pagamento</h2><div className="piloto-table-wrap"><table className="piloto-table"><thead><tr><th>Forma</th><th className="numerico">Atendimentos</th><th className="monetario">Total</th></tr></thead><tbody>{dados.por_forma_pagamento.map((item) => <tr key={item.forma_pagamento}><td>{item.forma_pagamento}</td><td className="numerico">{item.quantidade_atendimentos}</td><td className="monetario">{formatarMoeda(item.valor_total)}</td></tr>)}</tbody></table></div><div className="piloto-mobile-cards">{dados.por_forma_pagamento.map((item) => <article className="piloto-item-card" key={item.forma_pagamento}><header><strong>{item.forma_pagamento}</strong></header><dl><div><dt>Atendimentos</dt><dd>{item.quantidade_atendimentos}</dd></div><div><dt>Total</dt><dd>{formatarMoeda(item.valor_total)}</dd></div></dl></article>)}</div></div>
                    </section>
                </>

            )}

        </main>

    );

}


export default DashboardPiloto;
