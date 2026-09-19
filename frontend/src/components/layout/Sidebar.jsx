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

import { buscarUsuarioLogado, listarModulosEmpresa } from "../../services/usuarioService";

import "./Sidebar.css";


const menusAdministrativos = [
    {
        grupo: "Operação",
        itens: [
            { nome: "Dashboard", rota: "/dashboard/piloto", icone: LayoutDashboard, modulo: "dashboard" },
            { nome: "Agenda", rota: "/agenda", icone: CalendarDays, modulo: "agenda" },
            { nome: "Novo atendimento", rota: "/atendimentos/novo", icone: Scissors, modulo: "atendimentos" },
            { nome: "Atendimentos", rota: "/atendimentos", icone: Scissors, modulo: "atendimentos" }
        ]
    },
    {
        grupo: "Gestão financeira",
        itens: [
            { nome: "Repasses", rota: "/repasses", icone: Wallet, modulo: "repasses" },
            { nome: "Financeiro", rota: "/financeiro", icone: Wallet, modulo: "financeiro" }
        ]
    },
    {
        grupo: "Cadastros e operação",
        itens: [
            { nome: "Profissionais", rota: "/profissionais", icone: Users, modulo: "profissionais" },
            { nome: "Config. da operação", rota: "/configuracoes/agenda", icone: Settings, modulo: "servicos" },
            { nome: "Clientes", rota: "/clientes", icone: Users, modulo: "clientes" }
        ]
    },
    {
        grupo: "Produtos e estoque",
        itens: [
            { nome: "Vendas", rota: "/vendas", icone: ShoppingCart, modulo: "vendas" },
            { nome: "Produtos", rota: "/produtos", icone: Package, modulo: "produtos" },
            { nome: "Estoque", rota: "/estoque", icone: Boxes, modulo: "estoque" }
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
    { nome: "Minha agenda", rota: "/agenda", icone: CalendarDays, modulo: "agenda" },
    { nome: "Novo atendimento", rota: "/atendimentos/novo", icone: Scissors, modulo: "atendimentos" },
    { nome: "Meus atendimentos", rota: "/atendimentos", icone: Scissors, modulo: "atendimentos" },
    { nome: "Minha produção", rota: "/minha-producao", icone: Wallet, modulo: "atendimentos" }
];


export default function Sidebar({
    aberto = true,
    setAberto,
    mobileAberto = false,
    fecharMobile
}) {
    const navigate = useNavigate();
    const [perfil, setPerfil] = useState(null);
    const [modulosAtivos, setModulosAtivos] = useState(null);

    const carregarPerfil = useCallback(async () => {
        try {
            const [usuario, modulos] = await Promise.all([
                buscarUsuarioLogado(),
                listarModulosEmpresa()
            ]);
            setPerfil(usuario.perfil);
            setModulosAtivos(new Set(modulos.filter((modulo) => modulo.ativo).map((modulo) => modulo.codigo)));
        } catch {
            setPerfil(null);
            setModulosAtivos(null);
        }
    }, []);

    useEffect(() => {
        void Promise.resolve().then(carregarPerfil);
    }, [carregarPerfil]);

    const filtrarItens = (itens) => itens.filter((item) => (
        !modulosAtivos || !item.modulo || modulosAtivos.has(item.modulo)
    ));
    const gruposDeMenu = perfil === "profissional"
        ? [{ grupo: "Minha operação", itens: filtrarItens(menusProfissional) }]
        : menusAdministrativos.map((grupo) => ({ ...grupo, itens: filtrarItens(grupo.itens) }));

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
                {perfil && gruposDeMenu.filter((grupo) => grupo.itens.length > 0).map((grupo) => (
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
