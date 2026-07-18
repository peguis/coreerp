import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../auth/AuthContext";

import {
    buscarUsuarioLogado
} from "../services/usuarioService";


function Header() {


    const { logout } = useContext(AuthContext);

    const navigate = useNavigate();


    const [usuario, setUsuario] = useState(null);



    useEffect(() => {

        carregarUsuario();

    }, []);



    async function carregarUsuario() {

        const dados = await buscarUsuarioLogado();

        setUsuario(dados);

    }



    function sair() {

        logout();

        navigate("/");

    }



    return (

        <header
            style={{
                height: "60px",
                borderBottom: "1px solid #ddd",
                display: "flex",
                justifyContent: "flex-end",
                alignItems: "center",
                padding: "0 30px",
                gap: "20px"
            }}
        >


            <span>

                {
                    usuario
                        ? `Olá, ${usuario.nome}`
                        : "Carregando..."
                }

            </span>



            <button
                onClick={sair}
            >
                Sair
            </button>


        </header>

    );

}


export default Header;