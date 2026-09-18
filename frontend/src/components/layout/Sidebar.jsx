import {
    LayoutDashboard,
    Users,
    Package,
    Boxes,
    ShoppingCart,
    Scissors,
    Wallet,
    Settings,
    CalendarDays,
    LogOut,
    Menu,
    X
} from "lucide-react";


import {
    NavLink,
    useNavigate
} from "react-router-dom";


import { useCallback, useEffect, useState } from "react";


import { buscarUsuarioLogado } from "../../services/usuarioService";


import "./Sidebar.css";



const menusAdministrativos = [


    {
        nome: "Dashboard piloto",
        rota: "/dashboard/piloto",
        icone: LayoutDashboard
    },


    {
        nome: "Agenda",
        rota: "/agenda",
        icone: CalendarDays
    },


    {
        nome: "Clientes",
        rota: "/clientes",
        icone: Users
    },


    {
        nome: "Produtos",
        rota: "/produtos",
        icone: Package
    },


    {
        nome: "Estoque",
        rota: "/estoque",
        icone: Boxes
    },


    {
        nome: "Vendas",
        rota: "/vendas",
        icone: ShoppingCart
    },


    {
        nome: "Novo atendimento",
        rota: "/atendimentos/novo",
        icone: Scissors
    },


    {
        nome: "Atendimentos",
        rota: "/atendimentos",
        icone: Scissors
    },


    {
        nome: "Config. da operação",
        rota: "/configuracoes/agenda",
        icone: Settings
    },


    {
        nome: "Profissionais",
        rota: "/profissionais",
        icone: Users
    },


    {
        nome: "Repasses",
        rota: "/repasses",
        icone: Wallet
    },


    {
        nome: "Financeiro",
        rota: "/financeiro",
        icone: Wallet
    },


    {
        nome: "Configurações",
        rota: "/configuracoes",
        icone: Settings
    }


];


const menusProfissional = [

    {
        nome: "Início",
        rota: "/inicio",
        icone: LayoutDashboard
    },

    {
        nome: "Minha agenda",
        rota: "/agenda",
        icone: CalendarDays
    },

    {
        nome: "Novo atendimento",
        rota: "/atendimentos/novo",
        icone: Scissors
    },

    {
        nome: "Meus atendimentos",
        rota: "/atendimentos",
        icone: Scissors
    },

    {
        nome: "Minha produção",
        rota: "/minha-producao",
        icone: Wallet
    }

];





export default function Sidebar({


    aberto = true,

    setAberto,

    mobileAberto = false,

    fecharMobile


}) {



    const navigate = useNavigate();

    const [perfil, setPerfil] = useState(null);

    const carregarPerfil = useCallback(async () => {

        try {

            const usuario = await buscarUsuarioLogado();
            setPerfil(usuario.perfil);

        } catch {

            setPerfil(null);

        }

    }, []);

    useEffect(() => {

        void Promise.resolve().then(carregarPerfil);

    }, [carregarPerfil]);

    const menus = perfil === "profissional"
        ? menusProfissional
        : menusAdministrativos;






    function logout() {


        localStorage.removeItem("token");

        localStorage.removeItem("usuario");


        navigate("/login");


    }







    function clicarMenu() {


        if (window.innerWidth <= 900) {

            fecharMobile?.();

        }


    }







    return (



        <aside



            onClick={(e) => e.stopPropagation()}



            className={

                `sidebar

                ${!aberto ? "collapsed" : ""}

                ${mobileAberto ? "mobile-open" : ""}`

            }


        >





            <div className="sidebar-top">





                <div className="sidebar-logo">


                    <span className="sidebar-brand-mark" aria-hidden="true">H</span>
                    <span className="sidebar-brand-copy">
                        <strong>HYPE STUDIO</strong>
                        <small>BARBEARIA &amp; TATTOO</small>
                    </span>


                </div>








                <button

                    type="button"

                    className="sidebar-toggle"

                    aria-label={mobileAberto ? "Fechar menu" : "Alternar sidebar"}

                    onClick={() => {

                        if (window.innerWidth <= 900) {

                            fecharMobile?.();

                            return;

                        }

                        setAberto(!aberto);

                    }}

                >

                    {mobileAberto ? <X size={20} /> : <Menu size={20} />}

                </button>





            </div>









            <nav className="sidebar-menu">



                {


                    perfil && menus.map(item => {


                        const Icon = item.icone;




                        return (



                            <NavLink



                                key={item.nome}



                                to={item.rota}

                                end

                                aria-label={item.nome}

                                title={item.nome}



                                onClick={clicarMenu}



                                className={({ isActive }) =>



                                    isActive

                                        ?

                                        "menu-item active"

                                        :

                                        "menu-item"



                                }


                            >




                                <Icon size={20} />




                                <span>

                                    {item.nome}

                                </span>




                            </NavLink>



                        );



                    })


                }



            </nav>









            <div className="sidebar-studio-card">
                <span className="sidebar-studio-avatar">H</span>
                <span><strong>HYPE STUDIO</strong><small>Barbearia &amp; Tattoo</small></span>
            </div>
            <small className="sidebar-powered">Powered by Pegs</small>

            <button



                className="sidebar-logout"



                onClick={logout}



            >



                <LogOut size={18} />



                <span>

                    Sair

                </span>



            </button>






        </aside>



    );


}
