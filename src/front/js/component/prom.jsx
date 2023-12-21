import React from "react";
import { Link } from "react-router-dom";
import traje1 from "../../img/traje1.jpg"

export const Prom = () => {
    return(
        <div className="container">
            <div className="row">
                <div className="col-12 col-md-6 mb-3 mb-lg-0">
                    <div>
                    <div className="py-10 px-8 rounded" style={{
                        height: "200px",
                        backgroundImage: `url(${traje1})`,
                        backgroundSize: "cover", 
                        backgroundPosition: "center",
                        padding: "48px 28px"
                    }}>
                        <div>
                            <h3 className="fw-bold mb-1">Traje de personaje de anime &amp; Vegetales</h3>
                            <p className="mb-4">
                                Hasta
                                <span className="fw-bold"> 38% </span>
                                de descuento
                            </p>
                            <Link to="/lista_por_categorias/19">
                                <button href="#!" className="btn btn-dark">Comprar ahora</button>
                            </Link>
                        </div>
                    </div>
                    </div>
                </div>
                <div className="col-12 col-md-6">
                    <div>
                    <div className="py-10 px-8 rounded" style={{
                        height: "200px",
                        backgroundImage: `url(${traje1})`,
                        backgroundSize: "cover", 
                        backgroundPosition: "center",
                        padding: "48px 28px"
                    }}>
                        <div>
                            <h3 className="fw-bold mb-1">Otro traje de anime</h3>
                            <p className="mb-4">
                                Hasta
                                <span className="fw-bold"> 25% </span>
                                de descuento
                            </p>
                            <Link to="/lista_por_categorias/20">
                                <button href="#!" className="btn btn-dark">Comprar ahora</button>
                            </Link>                        
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    )
}