import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Header from "./Header";


function Layout() {


    return (

        <div>


            <Header />


            <div
                style={{
                    display: "flex"
                }}
            >


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


        </div>

    );

}


export default Layout;