import { useCallback, useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

import { buscarUsuarioLogado } from "../services/usuarioService";
import Loading from "../components/Loading";


export default function HomeRedirect() {

    const [perfil, setPerfil] = useState(null);
    const [erro, setErro] = useState(false);

    const carregar = useCallback(async () => {

        try {

            const usuario = await buscarUsuarioLogado();
            setPerfil(usuario.perfil);

        } catch {

            setErro(true);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregar);

    }, [carregar]);

    if (erro) {

        return <Navigate to="/login" replace />;

    }

    if (!perfil) {

        return <Loading texto="Carregando início..." />;

    }

    return (

        <Navigate
            to={perfil === "profissional" ? "/inicio" : "/dashboard/piloto"}
            replace
        />

    );

}
