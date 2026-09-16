import { Link } from "react-router-dom";

import PageHeader from "../components/ui/PageHeader";

import "./Piloto.css";


export default function InicioProfissional() {

    return (

        <main className="piloto-page">

            <PageHeader
                titulo="Início"
                subtitulo="Acesse rapidamente sua rotina de atendimentos"
            />

            <section className="piloto-grid">

                <Link className="piloto-link-card" to="/atendimentos/novo">
                    <strong>Novo atendimento</strong>
                    <span>Registre um serviço realizado agora.</span>
                </Link>

                <Link className="piloto-link-card" to="/atendimentos">
                    <strong>Meus atendimentos</strong>
                    <span>Consulte seus atendimentos registrados.</span>
                </Link>

                <Link className="piloto-link-card" to="/minha-producao">
                    <strong>Minha produção</strong>
                    <span>Acompanhe produção, repasses e pendências.</span>
                </Link>

            </section>

        </main>

    );

}
