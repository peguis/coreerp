import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";


function Layout() {


    return (

        <div style={{ display: "flex" }}>


            <Sidebar />


            <main
                style={{
                    flex: 1,
                    padding: 30
                }}
            >

                <Outlet />

            </main>


        </div>

    );

}


export default Layout;