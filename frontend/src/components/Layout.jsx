import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Header from "./Header";



function Layout() {


    return (


        <div

            style={{

                minHeight: "100vh"

            }}

        >



            <Header />




            <div

                style={{

                    display: "flex",

                    minHeight: "calc(100vh - 60px)"

                }}

            >



                <Sidebar />




                <main

                    style={{

                        flex: 1,

                        padding: 30,

                        overflow: "auto"

                    }}

                >


                    <Outlet />


                </main>



            </div>




        </div>


    );


}



export default Layout;