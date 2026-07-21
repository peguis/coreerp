import { BrowserRouter, Routes, Route } from "react-router-dom";


import Login from "../pages/Login";

import Dashboard from "../pages/Dashboard";


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


import PrivateRoute from "./PrivateRoute";

import Layout from "../components/Layout";





function AppRoutes() {


    return (


        <BrowserRouter>


            <Routes>



                {/* Rota pública */}


                <Route

                    path="/"

                    element={<Login />}

                />





                {/* Rotas protegidas */}


                <Route

                    element={<PrivateRoute />}

                >



                    <Route

                        element={<Layout />}

                    >




                        <Route

                            path="/dashboard"

                            element={<Dashboard />}

                        />





                        {/* PRODUTOS */}


                        <Route

                            path="/produtos"

                            element={<Produtos />}

                        />


                        <Route

                            path="/produtos/novo"

                            element={<NovoProduto />}

                        />


                        <Route

                            path="/produtos/:id"

                            element={<EditarProduto />}

                        />





                        {/* CLIENTES */}


                        <Route

                            path="/clientes"

                            element={<Clientes />}

                        />


                        <Route

                            path="/clientes/novo"

                            element={<NovoCliente />}

                        />


                        <Route

                            path="/clientes/:id"

                            element={<EditarCliente />}

                        />





                        {/* VENDAS */}


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





                        {/* ESTOQUE */}


                        <Route

                            path="/estoque"

                            element={<Estoque />}

                        />


                        <Route

                            path="/estoque/novo"

                            element={<NovoMovimento />}

                        />



                    </Route>


                </Route>





                {/* Qualquer rota inexistente */}


                <Route

                    path="*"

                    element={<Login />}

                />



            </Routes>


        </BrowserRouter>


    );


}



export default AppRoutes;