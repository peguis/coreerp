import {
    Outlet
} from "react-router-dom";


import {
    useState
} from "react";


import Sidebar from "./Sidebar";

import Topbar from "./Topbar";


import "./MainLayout.css";



export default function MainLayout() {



    const [sidebarAberta, setSidebarAberta] =

        useState(true);



    const [mobileAberto, setMobileAberto] =

        useState(false);






    return (



        <div

            className="layout"

            onClick={() => {

                if (window.innerWidth <= 900) {

                    setMobileAberto(false);

                }

            }}

        >



            <Sidebar


                aberto={sidebarAberta}


                setAberto={setSidebarAberta}


                mobileAberto={mobileAberto}


                fecharMobile={() =>
                    setMobileAberto(false)
                }


            />






            <div className="layout-content">



                <Topbar


                    abrirMenu={() =>
                        setMobileAberto(true)
                    }


                />






                <main className="layout-main">


                    <Outlet />


                </main>





            </div>





        </div>



    );


}