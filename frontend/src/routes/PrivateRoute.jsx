import { Navigate, Outlet } from "react-router-dom";

import { useContext } from "react";

import { AuthContext } from "../auth/AuthContextValue";




function PrivateRoute() {


    const {

        autenticado,

        token,

        carregando

    } = useContext(AuthContext);





    if (carregando) {

        return null;

    }





    if (!autenticado || !token) {

        return (

            <Navigate

                to="/login"

                replace

            />

        );

    }





    return <Outlet />;


}




export default PrivateRoute;
