import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";

import PrivateRoute from "./PrivateRoute";


import Produtos from "../pages/Produtos";
import Clientes from "../pages/Clientes";
import Vendas from "../pages/Vendas";
import Estoque from "../pages/Estoque";
import NovoProduto from "../pages/NovoProduto";
import EditarProduto from "../pages/EditarProduto";
import NovoCliente from "../pages/NovoCliente";
import EditarCliente from "../pages/EditarCliente";
import NovaVenda from "../pages/NovaVenda";
import DetalhesVenda from "../pages/DetalhesVenda";
import NovoMovimento from "../pages/NovoMovimento";


function AppRoutes() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Login />}
                />

                <Route
                    path="/produtos"
                    element={
                        <PrivateRoute>
                            <Produtos />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/clientes"
                    element={
                        <PrivateRoute>
                            <Clientes />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/vendas"
                    element={
                        <PrivateRoute>
                            <Vendas />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/estoque"
                    element={
                        <PrivateRoute>
                            <Estoque />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/produtos/novo"
                    element={
                        <PrivateRoute>
                            <NovoProduto />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/produtos/:id"
                    element={
                        <PrivateRoute>
                            <EditarProduto />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/clientes/novo"
                    element={
                        <PrivateRoute>
                            <NovoCliente />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/clientes/:id"
                    element={
                        <PrivateRoute>
                            <EditarCliente />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/vendas/nova"
                    element={
                        <PrivateRoute>
                            <NovaVenda />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/vendas/:id"
                    element={
                        <PrivateRoute>
                            <DetalhesVenda />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/estoque/novo"
                    element={
                        <PrivateRoute>
                            <NovoMovimento />
                        </PrivateRoute>
                    }
                />

                <Route
                    path="/dashboard"
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    }
                />

            </Routes>

        </BrowserRouter>

    )

}


export default AppRoutes;
