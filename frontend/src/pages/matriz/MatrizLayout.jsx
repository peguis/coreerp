import { useCallback, useEffect, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
    Building2,
    BriefcaseBusiness,
    ClipboardList,
    LayoutDashboard,
    LogOut,
    Menu,
    ShieldCheck,
    X
} from "lucide-react";

import { useAuth } from "../../hooks/useAuth";
import { buscarUsuarioLogado } from "../../services/usuarioService";
import { useTenant } from "../../tenant/TenantContextValue";

import "./Matriz.css";

const itensAdmin = [
    { nome: "Visão geral", rota: "/matriz/dashboard", icone: LayoutDashboard },
    { nome: "Empresas", rota: "/matriz/empresas", icone: Building2 },
    { nome: "Oportunidades", rota: "/matriz/oportunidades", icone: BriefcaseBusiness },
    { nome: "Auditoria", rota: "/matriz/auditoria", icone: ClipboardList }
];

const itensVendedor = [
    { nome: "Oportunidades", rota: "/matriz/oportunidades", icone: BriefcaseBusiness }
];

export default function MatrizLayout() {
    const location = useLocation();
    const navigate = useNavigate();
    const { logout } = useAuth();
    const { identity, cssVariables } = useTenant();
    const [menuAberto, setMenuAberto] = useState(false);
    const [usuario, setUsuario] = useState(null);
    const itens = usuario?.perfil === "vendedor_pegs" ? itensVendedor : itensAdmin;

    const carregarUsuario = useCallback(async () => {
        try {
            setUsuario(await buscarUsuarioLogado());
        } catch {
            setUsuario(null);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(carregarUsuario);
        void Promise.resolve().then(() => setMenuAberto(false));
    }, [carregarUsuario, location.pathname]);

    function sair() {
        logout();
        localStorage.removeItem("usuario");
        navigate("/login");
    }

    return (
        <div className="matriz-shell" style={cssVariables} data-tenant-key="pegs-matrix">
            <aside className={`matriz-sidebar ${menuAberto ? "is-open" : ""}`}>
                <div className="matriz-brand">
                    <div className="matriz-brand-mark">
                        <img src={identity.assets.sidebarLogo} alt="Pegs" />
                    </div>
                    <div>
                        <strong>Matriz Pegs</strong>
                        <span>{usuario?.perfil === "vendedor_pegs" ? "Operação comercial" : "Administração da plataforma"}</span>
                    </div>
                </div>

                <div className="matriz-sidebar-label">Plataforma</div>
                <nav className="matriz-nav" aria-label="Navegação da matriz Pegs">
                    {itens.map((item) => {
                        const Icon = item.icone;
                        return (
                            <NavLink
                                key={item.rota}
                                to={item.rota}
                                end={item.rota === "/matriz/dashboard"}
                                className={({ isActive }) => `matriz-nav-item ${isActive ? "active" : ""}`}
                                onClick={() => setMenuAberto(false)}
                            >
                                <Icon size={19} />
                                <span>{item.nome}</span>
                            </NavLink>
                        );
                    })}
                </nav>

                <div className="matriz-sidebar-footer">
                    <div className="matriz-security-note">
                        <ShieldCheck size={18} />
                        <span>Ambiente protegido<br /><small>{usuario?.perfil === "vendedor_pegs" ? "Acesso comercial limitado" : "Acesso exclusivo pegs_admin"}</small></span>
                    </div>
                    <button type="button" className="matriz-logout" onClick={sair}>
                        <LogOut size={17} />
                        <span>Sair da matriz</span>
                    </button>
                    <div className="matriz-powered">Pegs Core · plataforma modular</div>
                </div>
            </aside>

            {menuAberto && (
                <button
                    type="button"
                    className="matriz-sidebar-overlay"
                    aria-label="Fechar menu da matriz"
                    onClick={() => setMenuAberto(false)}
                />
            )}

            <div className="matriz-content">
                <header className="matriz-topbar">
                    <button type="button" className="matriz-menu-button" aria-label="Abrir menu" onClick={() => setMenuAberto(true)}>
                        {menuAberto ? <X size={21} /> : <Menu size={21} />}
                    </button>
                    <div className="matriz-topbar-context">
                        <span className="matriz-topbar-kicker">Pegs Core</span>
                        <strong>{usuario?.perfil === "vendedor_pegs" ? "Central comercial" : "Matriz administrativa"}</strong>
                    </div>
                    <div className="matriz-topbar-user">
                        <div className="matriz-avatar">{(usuario?.nome || "P").slice(0, 1).toUpperCase()}</div>
                        <div>
                            <strong>{usuario?.nome || "Administrador Pegs"}</strong>
                            <span>{usuario?.perfil === "vendedor_pegs" ? "Vendedor Pegs" : "Administrador da plataforma"}</span>
                        </div>
                    </div>
                </header>

                <main className="matriz-main">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
