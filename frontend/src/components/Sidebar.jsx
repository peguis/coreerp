import { Link } from "react-router-dom";

function Sidebar() {
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
            <h2>CoreERP</h2>

            <nav>
                <p><Link to="/dashboard">Dashboard</Link></p>
                <p><Link to="/produtos">Produtos</Link></p>
                <p><Link to="/clientes">Clientes</Link></p>
                <p><Link to="/vendas">Vendas</Link></p>
                <p><Link to="/estoque">Estoque</Link></p>
            </nav>
        </aside>
    );
}

export default Sidebar;