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
import { buscarEmpresaAtual } from "../../services/empresaService";


import "./MainLayout.css";
import "../../styles/hype.css";



export default function MainLayout() {


    const location = useLocation();

    const [sidebarAberta, setSidebarAberta] =

        useState(true);



    const [mobileAberto, setMobileAberto] =

        useState(false);

    const [empresa, setEmpresa] = useState(null);


    useEffect(() => {

        void Promise.resolve().then(() => setMobileAberto(false));

    }, [location.pathname]);

    useEffect(() => {
        let montado = true;
        void Promise.resolve().then(async () => {
            try {
                const dados = await buscarEmpresaAtual();
                if (montado) setEmpresa(dados);
            } catch {
                if (montado) setEmpresa(null);
            }
        });
        return () => {
            montado = false;
        };
    }, []);






    return (



        <div
            className="layout hype-theme"
            data-tenant-theme={empresa?.tema || "dark"}
            style={{
                "--tenant-accent": empresa?.cor_primaria || "#d9ab3f",
                "--tenant-accent-secondary": empresa?.cor_secundaria || "#edc45c",
                "--hype-gold": empresa?.cor_primaria || "#d9ab3f",
                "--hype-gold-hover": empresa?.cor_secundaria || "#edc45c",
                "--hype-gold-soft": empresa?.cor_primaria
                    ? `color-mix(in srgb, ${empresa.cor_primaria} 12%, transparent)`
                    : "rgba(217, 171, 63, .12)"
            }}
        >



            <Sidebar


                aberto={sidebarAberta}


                setAberto={setSidebarAberta}


                mobileAberto={mobileAberto}


                fecharMobile={() =>
                    setMobileAberto(false)
                }

                empresa={empresa}


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

                    empresa={empresa}


                />






                <main className="layout-main">


                    <Outlet />


                </main>





            </div>





        </div>



    );


}
