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

const PEGS_DEFAULTS = {
    accent: "#6f8cff",
    accentSecondary: "#9bb0ff",
    accentSoft: "rgba(111, 140, 255, .14)"
};


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
            className="layout pegs-theme hype-theme"
            data-tenant-theme={empresa?.tema || "pegs"}
            style={{
                "--tenant-accent": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--tenant-accent-secondary": empresa?.cor_secundaria || PEGS_DEFAULTS.accentSecondary,
                "--pegs-accent": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--pegs-accent-secondary": empresa?.cor_secundaria || PEGS_DEFAULTS.accentSecondary,
                "--pegs-accent-soft": empresa?.cor_primaria
                    ? `color-mix(in srgb, ${empresa.cor_primaria} 14%, transparent)`
                    : PEGS_DEFAULTS.accentSoft,
                /* Tokens globais também seguem o tenant para evitar Pegs/HYPE
                   misturados nas telas que ainda usam componentes legados. */
                "--color-primary": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--primary": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--primary-color": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--focus-ring": empresa?.cor_primaria
                    ? `0 0 0 3px color-mix(in srgb, ${empresa.cor_primaria} 18%, transparent)`
                    : "0 0 0 3px rgba(111, 140, 255, .18)",
                /* Aliases mantidos para as telas legadas durante a migração visual. */
                "--hype-gold": empresa?.cor_primaria || PEGS_DEFAULTS.accent,
                "--hype-gold-hover": empresa?.cor_secundaria || PEGS_DEFAULTS.accentSecondary,
                "--hype-gold-soft": empresa?.cor_primaria
                    ? `color-mix(in srgb, ${empresa.cor_primaria} 12%, transparent)`
                    : PEGS_DEFAULTS.accentSoft
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
