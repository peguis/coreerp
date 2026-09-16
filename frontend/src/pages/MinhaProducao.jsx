import { useCallback, useEffect, useState } from "react";

import { obterDashboardProfissional } from "../services/dashboardService";
import { getErrorMessage } from "../utils/errors";
import { formatarMoeda, formatarData } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import FormCard from "../components/forms/FormCard";
import Input from "../components/forms/Input";
import Button from "../components/forms/Button";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


function MinhaProducao() {

    const [dados, setDados] = useState(null);
    const [dataInicio, setDataInicio] = useState("");
    const [dataFim, setDataFim] = useState("");
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState("");

    const carregar = useCallback(async (params = {}) => {

        try {

            setCarregando(true);
            setErro("");
            setDados(await obterDashboardProfissional(params));

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar sua produção."));

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
            <PageHeader titulo="Minha produção" subtitulo="Acompanhe seus atendimentos, comissão e repasses." />
            <FormCard titulo="Período" subtitulo="Os valores são retornados pelo backend para o período escolhido.">
                <form className="piloto-toolbar" onSubmit={filtrar}>
                    <Input label="Data inicial" type="date" value={dataInicio} onChange={(evento) => setDataInicio(evento.target.value)} />
                    <Input label="Data final" type="date" value={dataFim} onChange={(evento) => setDataFim(evento.target.value)} />
                    <Button type="submit" variant="primary">Atualizar</Button>
                </form>
            </FormCard>
            {erro && <Mensagem tipo="erro" texto={erro} />}
            {carregando && !dados && <Loading texto="Carregando sua produção..." />}
            {dados && (
                <>
                    <p className="piloto-periodo">Período: {formatarData(dados.data_inicio)} até {formatarData(dados.data_fim)}</p>
                    <section className="piloto-grid">
                        <div className="piloto-metric"><span>Atendimentos</span><strong>{dados.quantidade_atendimentos}</strong></div>
                        <div className="piloto-metric"><span>Faturamento bruto próprio</span><strong>{formatarMoeda(dados.faturamento_bruto)}</strong></div>
                        <div className="piloto-metric"><span>Minha comissão</span><strong>{formatarMoeda(dados.valor_profissional)}</strong></div>
                        <div className="piloto-metric"><span>Valor já repassado</span><strong>{formatarMoeda(dados.valor_repassado)}</strong></div>
                        <div className="piloto-metric"><span>Valor pendente</span><strong>{formatarMoeda(dados.valor_pendente)}</strong></div>
                    </section>
                    <section className="piloto-subsection">
                        <h2 className="piloto-section-title">Resumo</h2>
                        <p>Profissional: <strong>{dados.nome}</strong></p>
                        <p>Área: <strong>{dados.area_atuacao}</strong></p>
                    </section>
                </>
            )}
        </main>

    );

}


export default MinhaProducao;
