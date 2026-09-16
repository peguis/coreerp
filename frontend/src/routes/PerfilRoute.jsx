import { useCallback, useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";

import { buscarUsuarioLogado } from "../services/usuarioService";
import Loading from "../components/Loading";


export default function PerfilRoute({ perfis }) {

    const [usuario, setUsuario] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(false);

    const carregarUsuario = useCallback(async () => {

        try {

            setUsuario(await buscarUsuarioLogado());

        } catch {

            setErro(true);

        } finally {

            setCarregando(false);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregarUsuario);

    }, [carregarUsuario]);

    if (carregando) {

        return <Loading texto="Validando perfil..." />;

    }

    if (erro) {

        return <Navigate to="/login" replace />;

    }

    if (!perfis.includes(usuario?.perfil)) {

        return <Navigate to="/sem-permissao" replace />;

    }

    return <Outlet />;

}
