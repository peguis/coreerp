import { Navigate, Outlet } from "react-router-dom";

import { useContext } from "react";

import { AuthContext } from "../auth/AuthContext";




function PrivateRoute() {


    const {

        autenticado,

        token,

        carregando

    } = useContext(AuthContext);





    console.log(
        "PRIVATE ROUTE:",
        autenticado,
        token
    );






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