import { Navigate, Outlet } from "react-router-dom";

import { useContext } from "react";

import { AuthContext } from "../auth/AuthContext";




function PrivateRoute() {


    const { autenticado, token } =
        useContext(AuthContext);


    console.log(
        "PRIVATE ROUTE:",
        autenticado,
        token
    );





    return <Outlet />;


}




export default PrivateRoute;