import {

    Bell,

    Search,

    UserCircle,

    Menu

} from "lucide-react";


import "./Topbar.css";



export default function Topbar({

    abrirMenu

}) {



    const usuario =

        JSON.parse(

            localStorage.getItem("usuario")

        );





    return (



        <header className="topbar">





            <button


                className="mobile-menu"


                onClick={abrirMenu}


            >


                <Menu size={22} />


            </button>






            <div className="topbar-search">


                <Search size={18} />


                <input

                    placeholder="Pesquisar..."

                />


            </div>








            <div className="topbar-right">



                <button className="topbar-icon">


                    <Bell size={20} />


                </button>







                <div className="topbar-user">



                    <UserCircle size={34} />




                    <div>


                        <strong>

                            {

                                usuario?.nome ||

                                "Administrador"

                            }


                        </strong>



                        <span>

                            Empresa

                        </span>


                    </div>




                </div>



            </div>






        </header>



    );


}