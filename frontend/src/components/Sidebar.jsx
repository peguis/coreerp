import { NavLink } from "react-router-dom";



function Sidebar() {



    const linkStyle = ({ isActive }) => ({


        color: "white",

        textDecoration: "none",

        display: "block",

        padding: "12px",

        borderRadius: "6px",

        background:

            isActive

                ?

                "#334155"

                :

                "transparent"



    });






    return (


        <aside


            style={{


                width: "220px",

                background: "#1e293b",

                color: "white",

                padding: "20px",

                flexShrink: 0


            }}



        >



            <h2>

                CoreERP

            </h2>





            <nav>



                <NavLink

                    to="/dashboard"

                    style={linkStyle}

                >

                    Dashboard

                </NavLink>




                <NavLink

                    to="/produtos"

                    style={linkStyle}

                >

                    Produtos

                </NavLink>




                <NavLink

                    to="/clientes"

                    style={linkStyle}

                >

                    Clientes

                </NavLink>




                <NavLink

                    to="/vendas"

                    style={linkStyle}

                >

                    Vendas

                </NavLink>




                <NavLink

                    to="/estoque"

                    style={linkStyle}

                >

                    Estoque

                </NavLink>



            </nav>




        </aside>


    );


}



export default Sidebar;