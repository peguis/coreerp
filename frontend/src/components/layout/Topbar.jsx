import { Bell, Menu, Search, UserCircle } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import { buscarUsuarioLogado } from "../../services/usuarioService";


import "./Topbar.css";



export default function Topbar({

    abrirMenu

}) {



    const [usuario, setUsuario] = useState(null);
    const location = useLocation();

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






            <div className="topbar-brand">
                <img className="topbar-brand-image" src="/images/hype-logo-sidebar.png" alt="" aria-hidden="true" />
                <span>HYPE STUDIO</span>
            </div>

            <span className="topbar-context" aria-label="Tela atual">
                {location.pathname.includes("agenda") ? "Agenda" : location.pathname.includes("profissionais") ? "Profissionais" : location.pathname.includes("configur") ? "Configurações" : "Dashboard"}
            </span>










            <div className="topbar-right">
                <div className="topbar-tools" aria-hidden="true">
                    <Search size={16} />
                    <Bell size={16} />
                </div>










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
