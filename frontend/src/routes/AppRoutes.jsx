import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import PrivateRoute from "./PrivateRoute";

import MainLayout from "../components/layout/MainLayout";

import Login from "../pages/Login";

import Dashboard from "../pages/Dashboard";

import Clientes from "../pages/Clientes";
import NovoCliente from "../pages/NovoCliente";
import EditarCliente from "../pages/EditarCliente";

import Produtos from "../pages/Produtos";
import NovoProduto from "../pages/NovoProduto";
import EditarProduto from "../pages/EditarProduto";

import Estoque from "../pages/Estoque";
import NovoMovimento from "../pages/NovoMovimento";
import Movimentos from "../pages/Movimentos";

import Vendas from "../pages/Vendas";
import NovaVenda from "../pages/NovaVenda";
import DetalhesVenda from "../pages/DetalhesVenda";

import Financeiro from "../pages/Financeiro";
import NovoLancamento from "../pages/NovoLancamento";
import EditarLancamento from "../pages/EditarLancamento";

import Configuracoes from "../pages/Configuracoes";

export default function AppRoutes() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Navigate to="/dashboard" replace />}
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route element={<PrivateRoute />}>

                    <Route element={<MainLayout />}>

                        <Route
                            path="/dashboard"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/clientes"
                            element={<Clientes />}
                        />

                        <Route
                            path="/clientes/novo"
                            element={<NovoCliente />}
                        />

                        <Route
                            path="/clientes/:id/editar"
                            element={<EditarCliente />}
                        />

                        <Route
                            path="/produtos"
                            element={<Produtos />}
                        />

                        <Route
                            path="/produtos/novo"
                            element={<NovoProduto />}
                        />

                        <Route
                            path="/produtos/:id/editar"
                            element={<EditarProduto />}
                        />

                        <Route
                            path="/estoque"
                            element={<Estoque />}
                        />

                        <Route
                            path="/estoque/movimentos"
                            element={<Movimentos />}
                        />

                        <Route
                            path="/estoque/novo"
                            element={<NovoMovimento />}
                        />

                        <Route
                            path="/vendas"
                            element={<Vendas />}
                        />

                        <Route
                            path="/vendas/nova"
                            element={<NovaVenda />}
                        />

                        <Route
                            path="/vendas/:id"
                            element={<DetalhesVenda />}
                        />

                        <Route
                            path="/financeiro"
                            element={<Financeiro />}
                        />

                        <Route
                            path="/financeiro/novo"
                            element={<NovoLancamento />}
                        />

                        <Route
                            path="/financeiro/:id/editar"
                            element={<EditarLancamento />}
                        />

                        <Route
                            path="/configuracoes"
                            element={<Configuracoes />}
                        />

                    </Route>

                </Route>

                <Route
                    path="*"
                    element={<Navigate to="/dashboard" replace />}
                />

            </Routes>

        </BrowserRouter>

    );

}