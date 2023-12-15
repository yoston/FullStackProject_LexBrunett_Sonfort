import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./pages/home";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import { Products } from "./pages/products.jsx";
import { Create } from "./pages/create.jsx";
import { Modificar } from "./pages/Modificar.jsx";
import injectContext from "./store/appContext";

import { Admin } from "./pages/Admin.jsx";
import { Crear_Admin } from "./pages/Crear_Admin.jsx";
import { Modificar_Admin } from "./pages/Modificar_Admin.jsx";

import { Orders } from "./pages/Orders.jsx";
import { Crear_Orders } from "./pages/Crear_Orders.jsx";
import { Modificar_Orders } from "./pages/Modificar_Orders.jsx";

import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";

//create your first component
const Layout = () => {
    //the basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";

    if(!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL/ >;

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route element={<Home />} path="/" />
                        <Route element={<Demo />} path="/demo" />
                        <Route element={<Single />} path="/single/:theid" />
                        <Route element={<Products />} path="/products" />
                        <Route element={<Modificar />} path="/Modificar/:id" />
                        <Route element={<Create />} path="/create" />
                        <Route element={<Admin />} path="/Admin" />
                        <Route element={<Crear_Admin />} path="/Crear_Admin" />
                        <Route element={<Modificar_Admin />} path="/Modificar_Admin/:id" />
                        <Route element={<Orders />} path="/Orders" />
                        <Route element={<Crear_Orders />} path="/Crear_Orders" />
                        <Route element={<Modificar_Orders />} path="/Modificar_Orders/:id" />
                        <Route element={<h1>Not found!</h1>} />
                    </Routes>
                    <Footer />
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);