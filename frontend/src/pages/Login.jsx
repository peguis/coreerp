import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../auth/AuthContext";

import { loginRequest } from "../api/auth";


function Login(){

    const navigate = useNavigate();

    const [username,setUsername] = useState("");
    const [password,setPassword] = useState("");

    const {login} = useContext(AuthContext);


    async function entrar() {

    const data = await loginRequest(
        username,
        password
    );

    login(
        data.access_token
    );

    navigate("/dashboard");

}


    return (

        <div>

            <h1>
                CoreERP Login
            </h1>


            <input
                placeholder="Email"
                value={username}
                onChange={
                    e=>setUsername(e.target.value)
                }
            />


            <input
                placeholder="Senha"
                type="password"
                value={password}
                onChange={
                    e=>setPassword(e.target.value)
                }
            />


            <button onClick={entrar}>
                Entrar
            </button>


        </div>

    )

}


export default Login;