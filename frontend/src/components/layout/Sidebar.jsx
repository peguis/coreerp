import {
    LayoutDashboard,
    Users,
    Package,
    Boxes,
    ShoppingCart,
    Wallet,
    Settings,
    LogOut,
    Menu
} from "lucide-react";


import {
    NavLink,
    useNavigate
} from "react-router-dom";


import "./Sidebar.css";



const menus = [


    {
        nome: "Dashboard",
        rota: "/dashboard",
        icone: LayoutDashboard
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





export default function Sidebar({


    aberto = true,

    setAberto,

    mobileAberto = false,

    fecharMobile


}) {



    const navigate = useNavigate();






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


                    <h2>

                        CoreERP

                    </h2>



                    <span>

                        SaaS ERP

                    </span>


                </div>








                <button

                    className="sidebar-toggle"

                    onClick={() =>
                        setAberto(!aberto)
                    }

                >

                    <Menu size={20} />

                </button>





            </div>









            <nav className="sidebar-menu">



                {


                    menus.map(item => {


                        const Icon = item.icone;




                        return (



                            <NavLink



                                key={item.nome}



                                to={item.rota}



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