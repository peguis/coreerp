import { useCallback, useEffect, useMemo, useState } from "react";

import { buscarUsuarioLogado, listarUsuarios } from "../services/usuarioService";
import { listarClientes } from "../services/clienteService";
import { listarProfissionais } from "../services/profissionalService";
import { listarServicos } from "../services/servicoService";
import { listarAtendimentos } from "../services/atendimentoService";
import { getErrorMessage } from "../utils/errors";
import { formatarMoeda, formatarPercentual, formatarDataHora } from "../utils/formatters";

import PageHeader from "../components/ui/PageHeader";
import SectionCard from "../components/ui/SectionCard";
import SearchInput from "../components/forms/SearchInput";
import Loading from "../components/Loading";
import Mensagem from "../components/Mensagem";

import "./Piloto.css";


function Atendimentos() {

    const [usuario, setUsuario] = useState(null);
    const [atendimentos, setAtendimentos] = useState([]);
    const [clientes, setClientes] = useState([]);
    const [servicos, setServicos] = useState([]);
    const [profissionais, setProfissionais] = useState([]);
    const [usuarios, setUsuarios] = useState([]);
    const [pesquisa, setPesquisa] = useState("");
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState("");

    const ehProfissional = usuario?.perfil === "profissional";

    const carregar = useCallback(async () => {

        try {

            setCarregando(true);
            setErro("");
            const usuarioDados = await buscarUsuarioLogado();
            const [atendimentosDados, clientesDados, servicosDados] = await Promise.all([
                listarAtendimentos({ pagina: 1, limite: 100 }),
                listarClientes(),
                listarServicos({ ativo: true, pagina: 1, limite: 100 })
            ]);

            setUsuario(usuarioDados);
            setAtendimentos(Array.isArray(atendimentosDados) ? atendimentosDados : []);
            setClientes(Array.isArray(clientesDados) ? clientesDados : []);
            setServicos(Array.isArray(servicosDados) ? servicosDados : []);

            if (!ehProfissional && ["admin", "gerente"].includes(usuarioDados.perfil)) {

                const [profissionaisDados, usuariosDados] = await Promise.all([
                    listarProfissionais({ ativo: true, pagina: 1, limite: 100 }),
                    listarUsuarios()
                ]);
                setProfissionais(Array.isArray(profissionaisDados) ? profissionaisDados : []);
                setUsuarios(Array.isArray(usuariosDados) ? usuariosDados : []);

            }

        } catch (error) {

            setErro(getErrorMessage(error, "Não foi possível carregar os atendimentos."));

        } finally {

            setCarregando(false);

        }

    }, [ehProfissional]);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    const nomes = useMemo(() => ({
        clientes: new Map(clientes.map((item) => [item.id, item.nome])),
        servicos: new Map(servicos.map((item) => [item.id, item.nome])),
        profissionais: new Map(profissionais.map((item) => [
            item.id,
            usuarios.find((usuarioItem) => usuarioItem.id === item.usuario_id)?.nome || `Profissional #${item.id}`
        ]))
    }), [clientes, profissionais, servicos, usuarios]);

    const filtrados = atendimentos.filter((item) => {

        const texto = pesquisa.trim().toLowerCase();
        if (!texto) return true;

        return [
            item.id,
            nomes.clientes.get(item.cliente_id),
            nomes.servicos.get(item.servico_id),
            nomes.profissionais.get(item.profissional_id),
            item.forma_pagamento
        ].some((valor) => String(valor || "").toLowerCase().includes(texto));

    });

    function tituloProfissional(id) {

        return nomes.profissionais.get(id) || `Profissional #${id}`;

    }

    function dadosCard(item) {

        return (
            <article className="piloto-item-card" key={item.id}>
                <header>
                    <strong>Atendimento #{item.id}</strong>
                    <span>{formatarDataHora(item.realizado_em)}</span>
                </header>
                <dl>
                    {!ehProfissional && <div><dt>Profissional</dt><dd>{tituloProfissional(item.profissional_id)}</dd></div>}
                    <div><dt>Serviço</dt><dd>{nomes.servicos.get(item.servico_id) || `Serviço #${item.servico_id}`}</dd></div>
                    <div><dt>Cliente</dt><dd>{nomes.clientes.get(item.cliente_id) || "Não informado"}</dd></div>
                    <div><dt>Valor</dt><dd>{formatarMoeda(item.valor)}</dd></div>
                    <div><dt>Pagamento</dt><dd>{item.forma_pagamento}</dd></div>
                    <div><dt>Comissão aplicada</dt><dd>{formatarPercentual(item.percentual_profissional)}</dd></div>
                    <div><dt>{ehProfissional ? "Meu valor" : "Valor profissional"}</dt><dd>{formatarMoeda(item.valor_profissional)}</dd></div>
                    {!ehProfissional && <div><dt>Valor casa</dt><dd>{formatarMoeda(item.valor_casa)}</dd></div>}
                </dl>
            </article>
        );

    }

    return (

        <main className="piloto-page">
            <PageHeader
                titulo={ehProfissional ? "Meus atendimentos" : "Atendimentos"}
                subtitulo={ehProfissional ? "Consulte apenas os atendimentos vinculados a você." : "Histórico de atendimentos da empresa."}
            />
            {erro && <Mensagem tipo="erro" texto={erro} />}
            <SectionCard>
                <SearchInput
                    value={pesquisa}
                    onChange={(evento) => setPesquisa(evento.target.value)}
                    placeholder="Buscar por serviço, cliente ou profissional..."
                />
            </SectionCard>
            <SectionCard>
                {carregando ? <Loading texto="Carregando atendimentos..." /> : filtrados.length === 0 ? (
                    <div className="piloto-empty">Nenhum atendimento encontrado.</div>
                ) : (
                    <>
                        <div className="piloto-table-wrap">
                            <table className="piloto-table">
                                <thead><tr><th>Data/hora</th>{!ehProfissional && <th>Profissional</th>}<th>Serviço</th><th>Cliente</th><th className="monetario">Valor</th><th>Pagamento</th><th className="numerico">Comissão</th><th className="monetario">{ehProfissional ? "Meu valor" : "Valor profissional"}</th>{!ehProfissional && <th className="monetario">Casa</th>}</tr></thead>
                                <tbody>{filtrados.map((item) => <tr key={item.id}><td>{formatarDataHora(item.realizado_em)}</td>{!ehProfissional && <td>{tituloProfissional(item.profissional_id)}</td>}<td>{nomes.servicos.get(item.servico_id) || `Serviço #${item.servico_id}`}</td><td>{nomes.clientes.get(item.cliente_id) || "-"}</td><td className="monetario">{formatarMoeda(item.valor)}</td><td>{item.forma_pagamento}</td><td className="numerico">{formatarPercentual(item.percentual_profissional)}</td><td className="monetario">{formatarMoeda(item.valor_profissional)}</td>{!ehProfissional && <td className="monetario">{formatarMoeda(item.valor_casa)}</td>}</tr>)}</tbody>
                            </table>
                        </div>
                        <div className="piloto-mobile-cards">{filtrados.map(dadosCard)}</div>
                    </>
                )}
            </SectionCard>
        </main>

    );

}


export default Atendimentos;
