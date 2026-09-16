import {
    Outlet
} from "react-router-dom";


import {
    useEffect,
    useState
} from "react";


import { useLocation } from "react-router-dom";


import Sidebar from "./Sidebar";

import Topbar from "./Topbar";


import "./MainLayout.css";
import "../../styles/hype.css";



export default function MainLayout() {


    const location = useLocation();

    const [sidebarAberta, setSidebarAberta] =

        useState(true);



    const [mobileAberto, setMobileAberto] =

        useState(false);


    useEffect(() => {

        void Promise.resolve().then(() => setMobileAberto(false));

    }, [location.pathname]);






    return (



        <div className="layout hype-theme">



            <Sidebar


                aberto={sidebarAberta}


                setAberto={setSidebarAberta}


                mobileAberto={mobileAberto}


                fecharMobile={() =>
                    setMobileAberto(false)
                }


            />


            {mobileAberto && (

                <button

                    type="button"

                    className="mobile-sidebar-overlay"

                    aria-label="Fechar menu"

                    onClick={() => setMobileAberto(false)}

                />

            )}






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
