import { Navigate } from "react-router-dom";
import { useContext } from "react";

import { AuthContext } from "../auth/AuthContext";

import Loading from "../components/Loading";

export default function ProtectedRoute({ children }) {

    const {

        autenticado,

        carregando

    } = useContext(AuthContext);

    if (carregando) {

        return <Loading texto="Carregando..." />;

    }

    if (!autenticado) {

        return <Navigate to="/login" replace />;

    }

    return children;

}