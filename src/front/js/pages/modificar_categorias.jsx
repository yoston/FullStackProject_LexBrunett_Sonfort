import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Link, useParams } from "react-router-dom";

export const Modificar_categorias = () => {
    const { theid } = useParams();
    const { store, actions } = useContext(Context);

    const Categories = store.Categories.find(Categories => Categories.id == theid);
    const [name, setName] = useState(Categories.name || "");
    const [image, setImage] = useState(Categories.image || "");
    

    const isFormValid = name && image;

    const objeto = {
        name: name,
        image: image,
       
    };

    return (
        <div>
            <form>
                <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name</label>
                    <input type="text" className="form-control" id="name" value={name} onChange={(e) => setName(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label htmlFor="image" className="form-label">Image</label>
                    <input type="text" className="form-control" id="image" value={image} onChange={(e) => setImage(e.target.value)} />
                </div>
                
                <Link to="/Categories">
                    <button disabled={!isFormValid} onClick={() => actions.modificar_categorias(theid, objeto)}>Guardar Cambios</button>
                </Link>
                <Link to="/Categories">
                    <button onClick={() => actions.delete(theid)}>Delete </button>
                </Link>
            </form>
        </div>
    );
};