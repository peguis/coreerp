import {
    LayoutDashboard,
    Users,
    Package,
    Boxes,
    ShoppingCart,
    Scissors,
    Wallet,
    Settings,
    CalendarDays,
    LogOut,
    Menu,
    X
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";

import { buscarUsuarioLogado } from "../../services/usuarioService";

import "./Sidebar.css";


const menusAdministrativos = [
    {
        grupo: "Operação",
        itens: [
            { nome: "Dashboard", rota: "/dashboard/piloto", icone: LayoutDashboard },
            { nome: "Agenda", rota: "/agenda", icone: CalendarDays },
            { nome: "Novo atendimento", rota: "/atendimentos/novo", icone: Scissors },
            { nome: "Atendimentos", rota: "/atendimentos", icone: Scissors }
        ]
    },
    {
        grupo: "Gestão financeira",
        itens: [
            { nome: "Repasses", rota: "/repasses", icone: Wallet },
            { nome: "Financeiro", rota: "/financeiro", icone: Wallet }
        ]
    },
    {
        grupo: "Cadastros e operação",
        itens: [
            { nome: "Profissionais", rota: "/profissionais", icone: Users },
            { nome: "Config. da operação", rota: "/configuracoes/agenda", icone: Settings },
            { nome: "Clientes", rota: "/clientes", icone: Users }
        ]
    },
    {
        grupo: "Produtos e estoque",
        itens: [
            { nome: "Vendas", rota: "/vendas", icone: ShoppingCart },
            { nome: "Produtos", rota: "/produtos", icone: Package },
            { nome: "Estoque", rota: "/estoque", icone: Boxes }
        ]
    },
    {
        grupo: "Sistema",
        itens: [
            { nome: "Configurações", rota: "/configuracoes", icone: Settings }
        ]
    }
];

const menusProfissional = [
    { nome: "Início", rota: "/inicio", icone: LayoutDashboard },
    { nome: "Minha agenda", rota: "/agenda", icone: CalendarDays },
    { nome: "Novo atendimento", rota: "/atendimentos/novo", icone: Scissors },
    { nome: "Meus atendimentos", rota: "/atendimentos", icone: Scissors },
    { nome: "Minha produção", rota: "/minha-producao", icone: Wallet }
];


export default function Sidebar({
    aberto = true,
    setAberto,
    mobileAberto = false,
    fecharMobile
}) {
    const navigate = useNavigate();
    const [perfil, setPerfil] = useState(null);

    const carregarPerfil = useCallback(async () => {
        try {
            const usuario = await buscarUsuarioLogado();
            setPerfil(usuario.perfil);
        } catch {
            setPerfil(null);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(carregarPerfil);
    }, [carregarPerfil]);

    const gruposDeMenu = perfil === "profissional"
        ? [{ grupo: "Minha operação", itens: menusProfissional }]
        : menusAdministrativos;

    function logout() {
        localStorage.removeItem("token");
        localStorage.removeItem("usuario");
        navigate("/login");
    }

    function clicarMenu() {
        if (window.innerWidth <= 900) fecharMobile?.();
    }

    return (
        <aside
            onClick={(evento) => evento.stopPropagation()}
            className={`sidebar ${!aberto ? "collapsed" : ""} ${mobileAberto ? "mobile-open" : ""}`}
        >
            <div className="sidebar-top">
                <div className="sidebar-logo">
                    <img className="sidebar-logo-image" src="/images/hype-logo-sidebar.png" alt="HYPE STUDIO — Barbearia & Tattoo" />
                </div>

                <button
                    type="button"
                    className="sidebar-toggle"
                    aria-label={mobileAberto ? "Fechar menu" : "Alternar sidebar"}
                    onClick={() => {
                        if (window.innerWidth <= 900) {
                            fecharMobile?.();
                            return;
                        }

                        setAberto(!aberto);
                    }}
                >
                    {mobileAberto ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            <nav className="sidebar-menu" aria-label="Navegação principal">
                {perfil && gruposDeMenu.map((grupo) => (
                    <section className="sidebar-menu-section" key={grupo.grupo} aria-label={grupo.grupo}>
                        <p className="sidebar-menu-group-title">{grupo.grupo}</p>
                        <div className="sidebar-menu-group-items">
                            {grupo.itens.map((item) => {
                                const Icon = item.icone;

                                return (
                                    <NavLink
                                        key={item.nome}
                                        to={item.rota}
                                        end
                                        aria-label={item.nome}
                                        title={item.nome}
                                        onClick={clicarMenu}
                                        className={({ isActive }) => isActive ? "menu-item active" : "menu-item"}
                                    >
                                        <Icon size={20} />
                                        <span>{item.nome}</span>
                                    </NavLink>
                                );
                            })}
                        </div>
                    </section>
                ))}
            </nav>

            <div className="sidebar-studio-card">
                <img className="sidebar-studio-logo" src="/images/hype-logo-sidebar.png" alt="" aria-hidden="true" />
                <span><strong>HYPE STUDIO</strong><small>Barbearia &amp; Tattoo</small></span>
            </div>
            <small className="sidebar-powered">Powered by Pegs</small>

            <button className="sidebar-logout" onClick={logout}>
                <LogOut size={18} />
                <span>Sair</span>
            </button>
        </aside>
    );
}
