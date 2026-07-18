import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../auth/AuthContext";

import { loginRequest } from "../api/auth";


function Login() {


    const navigate = useNavigate();


    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");


    const { login } = useContext(AuthContext);



    async function entrar(e) {

        e.preventDefault();


        try {


            const data = await loginRequest(
                username,
                password
            );


            login(
                data.access_token
            );


            navigate("/dashboard");



        } catch (erro) {


            alert(
                "Usuário ou senha inválidos"
            );


        }


    }



    return (


        <div
            style={{
                padding: 40
            }}
        >


            <h1>
                CoreERP Login
            </h1>



            <form onSubmit={entrar}>


                <div>

                    <input

                        placeholder="Email"

                        value={username}

                        onChange={
                            e => setUsername(e.target.value)
                        }

                    />

                </div>



                <br />



                <div>

                    <input

                        placeholder="Senha"

                        type="password"

                        value={password}

                        onChange={
                            e => setPassword(e.target.value)
                        }

                    />

                </div>



                <br />



                <button type="submit">

                    Entrar

                </button>



            </form>


        </div>


    );


}


export default Login;