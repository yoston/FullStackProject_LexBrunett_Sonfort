import React, {useContext, useState} from "react";
import { Context } from "../store/appContext";
import { Link, Navigate } from "react-router-dom";

export const Navbar_user = () => {
    const { store, actions } = useContext(Context)

    function seleccionarBoton(boton) {
        // Obtener todos los botones
        var botones = document.querySelectorAll('.mi-boton');
      
        // Quitar la clase 'seleccionado' de todos los botones
        botones.forEach(function(b) {
          b.classList.remove('seleccionado');
        });
      
        // Agregar la clase 'seleccionado' al botón actual
        boton.classList.add('seleccionado');
      }
      
    return (
        <ul className="list-unstyled" style={{padding:"20% 0% 20% 10%"}}>
            <Link to="/products" style={{textDecoration: "none"}}>
                <li key={1} className={`mi-boton`} onClick={(e) => seleccionarBoton(e.currentTarget)} style={{width:"247px", height:"48px",padding:"8px 28px", marginBottom:"4px",borderRadius:"8px"}}>
                    <div className="row">
                        <div className="col-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-cart-check" viewBox="0 0 16 16">
                                <path d="M11.354 6.354a.5.5 0 0 0-.708-.708L8 8.293 6.854 7.146a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                                <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1zm3.915 10L3.102 4h10.796l-1.313 7h-8.17zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0m7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                            </svg>
                        </div>
                        <div className="col-10">
                            Productos
                        </div>
                    </div>
                </li>
            </Link>

            <Link to="/categorias" style={{textDecoration: "none"}}>
                <li key={2} className={`mi-boton`} onClick={(e) => seleccionarBoton(e.currentTarget)} style={{width:"247px", height:"48px",padding:"8px 28px", marginBottom:"4px",borderRadius:"8px"}}>
                    <div className="row">
                        <div className="col-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-list-ul" viewBox="0 0 16 16">
                                <path fillRule="evenodd" d="M5 11.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m-3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2m0 4a1 1 0 1 0 0-2 1 1 0 0 0 0 2m0 4a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>
                            </svg>
                        </div>
                        <div className="col-10">
                            Categorias
                        </div>
                    </div>
                </li>
            </Link>

            <Link to="/all_ordenes" style={{textDecoration: "none"}}>
                <li key={4} className={`mi-boton`} onClick={(e) => seleccionarBoton(e.currentTarget)} style={{width:"247px", height:"48px",padding:"8px 28px", marginBottom:"4px",borderRadius:"8px"}}>
                    <div className="row">
                        <div className="col-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-bag" viewBox="0 0 16 16">
                                <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1m3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/>
                            </svg>
                        </div>
                        <div className="col-10">
                            Ordenes
                        </div>
                    </div>
                </li>
            </Link>
        </ul>
    )
}