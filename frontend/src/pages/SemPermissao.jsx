import { Link } from "react-router-dom";

import Button from "../components/forms/Button";
import PageHeader from "../components/ui/PageHeader";

import "./Piloto.css";


export default function SemPermissao() {

    return (

        <main className="piloto-page access-denied">

            <PageHeader
                titulo="Acesso não permitido"
                subtitulo="Seu perfil não possui acesso a este módulo."
            />

            <Link to="/">
                <Button variant="primary">Ir para o início</Button>
            </Link>

        </main>

    );

}
