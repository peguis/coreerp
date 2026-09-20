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
import { TenantErrorState, TenantLoading } from "../../tenant/TenantContext";
import { useTenant } from "../../tenant/TenantContextValue";


import "./MainLayout.css";
import "../../styles/hype.css";

export default function MainLayout() {


    const location = useLocation();

    const [sidebarAberta, setSidebarAberta] =

        useState(true);



    const [mobileAberto, setMobileAberto] =

        useState(false);

    const tenant = useTenant();


    useEffect(() => {

        void Promise.resolve().then(() => setMobileAberto(false));

    }, [location.pathname]);

    if (tenant.status === "loading") return <TenantLoading />;
    if (tenant.status === "error") return <TenantErrorState error={tenant.error} />;

    const { identity, cssVariables } = tenant;






    return (



        <div
            className={`layout tenant-shell tenant-theme tenant-theme-${identity.tenantKey}`}
            data-tenant-key={identity.tenantKey}
            data-tenant-theme={identity.tenantTheme}
            style={cssVariables}
        >



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
