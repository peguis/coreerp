import { Menu, UserCircle } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { buscarUsuarioLogado } from "../../services/usuarioService";


import "./Topbar.css";



export default function Topbar({

    abrirMenu

}) {



    const [usuario, setUsuario] = useState(null);

    const carregarUsuario = useCallback(async () => {
        try {
            setUsuario(await buscarUsuarioLogado());
        } catch {
            setUsuario(null);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(carregarUsuario);
    }, [carregarUsuario]);

    const nomesPerfil = {
        admin: "Administrador",
        gerente: "Gerente",
        profissional: "Profissional"
    };





    return (



        <header className="topbar">





            <button


                type="button"

                className="mobile-menu"

                aria-label="Abrir menu"


                onClick={abrirMenu}


            >


                <Menu size={22} />


            </button>






            <div className="topbar-brand">HYPE STUDIO</div>










            <div className="topbar-right">










                <div className="topbar-user">



                    <UserCircle size={34} />




                    <div>


                        <strong>

                            {

                                usuario?.nome ||

                                "Usuário autenticado"

                            }


                        </strong>



                        <span>

                            {nomesPerfil[usuario?.perfil] || "Conta ativa"}

                        </span>


                    </div>




                </div>



            </div>






        </header>



    );


}
