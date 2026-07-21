import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../auth/AuthContext";
import { loginRequest } from "../api/auth";


function Login() {


    const navigate = useNavigate();


    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [erro, setErro] = useState("");



    const { login } = useContext(AuthContext);





    async function entrar(e) {


        e.preventDefault();


        setErro("");


        console.log(
            "ENVIANDO LOGIN:",
            username,
            password
        );



        try {


            const data = await loginRequest(

                username,

                password

            );



            console.log(
                "RESPOSTA LOGIN:",
                data
            );



            login(

                data.access_token

            );



            navigate(
                "/dashboard"
            );



        } catch (erro) {



            console.log(
                "ERRO LOGIN:",
                erro
            );



            setErro(

                erro.response?.data?.detail ||

                "Usuário ou senha inválidos"

            );


        }


    }








    return (


        <main

            style={{

                padding: 40,

                maxWidth: 400,

                margin: "auto"

            }}

        >



            <h1>

                CoreERP

            </h1>



            <h2>

                Login

            </h2>





            {

                erro &&

                <p

                    style={{

                        color: "red"

                    }}

                >

                    {erro}

                </p>

            }





            <form onSubmit={entrar}>


                <input


                    placeholder="Email"


                    type="email"


                    value={username}


                    onChange={

                        e => setUsername(

                            e.target.value

                        )

                    }


                    style={{

                        width: "100%",

                        padding: 10

                    }}


                />




                <br />

                <br />







                <input


                    placeholder="Senha"


                    type="password"


                    value={password}


                    onChange={

                        e => setPassword(

                            e.target.value

                        )

                    }


                    style={{

                        width: "100%",

                        padding: 10

                    }}


                />




                <br />

                <br />







                <button

                    type="submit"

                >

                    Entrar

                </button>




            </form>




        </main>


    );


}


export default Login;