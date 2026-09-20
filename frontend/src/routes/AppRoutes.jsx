import {
    Navigate,
    Route,
    Routes
} from "react-router-dom";

import PrivateRoute from "./PrivateRoute";
import PerfilRoute from "./PerfilRoute";

import MainLayout from "../components/layout/MainLayout";

import Login from "../pages/Login";
import HomeRedirect from "../pages/HomeRedirect";
import SemPermissao from "../pages/SemPermissao";
import InicioProfissional from "../pages/InicioProfissional";
import MinhaProducao from "../pages/MinhaProducao";
import Atendimentos from "../pages/Atendimentos";
import NovoAtendimento from "../pages/NovoAtendimento";
import DashboardPiloto from "../pages/DashboardPiloto";
import Servicos from "../pages/Servicos";
import Profissionais from "../pages/Profissionais";
import Repasses from "../pages/Repasses";

import Dashboard from "../pages/Dashboard";
import Clientes from "../pages/Clientes";
import NovoCliente from "../pages/NovoCliente";
import EditarCliente from "../pages/EditarCliente";
import Produtos from "../pages/Produtos";
import NovoProduto from "../pages/NovoProduto";
import EditarProduto from "../pages/EditarProduto";
import Estoque from "../pages/Estoque";
import Movimentos from "../pages/Movimentos";
import NovoMovimento from "../pages/NovoMovimento";
import Vendas from "../pages/Vendas";
import NovaVenda from "../pages/NovaVenda";
import DetalhesVenda from "../pages/DetalhesVenda";
import Financeiro from "../pages/Financeiro";
import NovoLancamento from "../pages/NovoLancamento";
import EditarLancamento from "../pages/EditarLancamento";
import Configuracoes from "../pages/Configuracoes";
import ConfiguracaoAgenda from "../pages/ConfiguracaoAgenda";
import Agenda from "../pages/Agenda";
import MatrizLayout from "../pages/matriz/MatrizLayout";
import MatrizDashboard from "../pages/matriz/MatrizDashboard";
import MatrizEmpresas from "../pages/matriz/MatrizEmpresas";
import MatrizEmpresaDetalhe from "../pages/matriz/MatrizEmpresaDetalhe";
import MatrizProvisionar from "../pages/matriz/MatrizProvisionar";
import MatrizAuditoria from "../pages/matriz/MatrizAuditoria";


const ADMINISTRADORES = ["pegs_admin", "admin", "gerente"];
const ATENDIMENTO = ["pegs_admin", "admin", "gerente", "profissional"];


export default function AppRoutes() {

    return (

        <Routes>
                <Route path="/login" element={<Login />} />

                <Route element={<PrivateRoute />}>
                    <Route path="/" element={<HomeRedirect />} />
                    <Route element={<PerfilRoute perfis={["pegs_admin"]} />}>
                        <Route element={<MatrizLayout />}>
                            <Route path="/matriz" element={<Navigate to="/matriz/dashboard" replace />} />
                            <Route path="/matriz/dashboard" element={<MatrizDashboard />} />
                            <Route path="/matriz/empresas" element={<MatrizEmpresas />} />
                            <Route path="/matriz/empresas/nova" element={<MatrizProvisionar />} />
                            <Route path="/matriz/empresas/:empresaId" element={<MatrizEmpresaDetalhe />} />
                            <Route path="/matriz/auditoria" element={<MatrizAuditoria />} />
                        </Route>
                    </Route>
                    <Route element={<MainLayout />}>
                        <Route path="/sem-permissao" element={<SemPermissao />} />

                        <Route element={<PerfilRoute perfis={ADMINISTRADORES} />}>
                            <Route path="/dashboard" element={<Dashboard />} />
                            <Route path="/dashboard/piloto" element={<DashboardPiloto />} />
                            <Route path="/servicos" element={<Servicos />} />
                            <Route path="/profissionais" element={<Profissionais />} />
                            <Route path="/repasses" element={<Repasses />} />

                            <Route path="/clientes" element={<Clientes />} />
                            <Route path="/clientes/novo" element={<NovoCliente />} />
                            <Route path="/clientes/:id/editar" element={<EditarCliente />} />
                            <Route path="/produtos" element={<Produtos />} />
                            <Route path="/produtos/novo" element={<NovoProduto />} />
                            <Route path="/produtos/:id/editar" element={<EditarProduto />} />
                            <Route path="/estoque" element={<Estoque />} />
                            <Route path="/estoque/movimentos" element={<Movimentos />} />
                            <Route path="/estoque/novo" element={<NovoMovimento />} />
                            <Route path="/vendas" element={<Vendas />} />
                            <Route path="/vendas/nova" element={<NovaVenda />} />
                            <Route path="/vendas/:id" element={<DetalhesVenda />} />
                            <Route path="/financeiro" element={<Financeiro />} />
                            <Route path="/financeiro/novo" element={<NovoLancamento />} />
                            <Route path="/financeiro/:id/editar" element={<EditarLancamento />} />
                            <Route path="/configuracoes" element={<Configuracoes />} />
                            <Route path="/configuracoes/agenda" element={<ConfiguracaoAgenda />} />
                        </Route>

                        <Route element={<PerfilRoute perfis={ATENDIMENTO} />}>
                            <Route path="/agenda" element={<Agenda />} />
                            <Route path="/atendimentos" element={<Atendimentos />} />
                            <Route path="/atendimentos/novo" element={<NovoAtendimento />} />
                        </Route>

                        <Route element={<PerfilRoute perfis={["profissional"]} />}>
                            <Route path="/inicio" element={<InicioProfissional />} />
                            <Route path="/minha-producao" element={<MinhaProducao />} />
                            <Route path="/dashboard/profissional" element={<MinhaProducao />} />
                        </Route>
                    </Route>
                </Route>

                <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

    );

}
