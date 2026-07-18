import { NavLink } from "react-router-dom";


function Sidebar() {


    const linkStyle = ({ isActive }) => ({

        color: "white",

        textDecoration: "none",

        display: "block",

        padding: "10px",

        borderRadius: "6px",

        background: isActive
            ? "#334155"
            : "transparent"

    });



    return (

        <aside
            style={{
                width: "220px",
                background: "#1e293b",
                color: "white",
                minHeight: "100vh",
                padding: "20px"
            }}
        >


            <h2>
                CoreERP
            </h2>



            <nav>


                <p>
                    <NavLink
                        to="/dashboard"
                        style={linkStyle}
                    >
                        Dashboard
                    </NavLink>
                </p>



                <p>
                    <NavLink
                        to="/produtos"
                        style={linkStyle}
                    >
                        Produtos
                    </NavLink>
                </p>



                <p>
                    <NavLink
                        to="/clientes"
                        style={linkStyle}
                    >
                        Clientes
                    </NavLink>
                </p>



                <p>
                    <NavLink
                        to="/vendas"
                        style={linkStyle}
                    >
                        Vendas
                    </NavLink>
                </p>



                <p>
                    <NavLink
                        to="/estoque"
                        style={linkStyle}
                    >
                        Estoque
                    </NavLink>
                </p>



            </nav>


        </aside>

    );

}


export default Sidebar;