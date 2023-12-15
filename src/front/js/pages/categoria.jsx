import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext.js";
import { Link } from "react-router-dom";

export const Categories = () => {
    const { store, actions } = useContext(Context);

    useEffect(() => {
        actions.getCategories();
      }, []);

      return (
        <div className="container">
              <ul>
        {store.Categories.map((item) => (
          <li key={item.id}>
            <b>
              {item.id} {item.name} {item.image}
            </b>
            <Link to={`/modificar_categorias/${item.id}`}>
              <button>Modificar</button>
            </Link>
          </li>
        ))}
              </ul>
              <Link to="/Crear_Categoria">
                <button>Crear</button>
              </Link>
              
        </div>
      );
    };