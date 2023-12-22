import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Link, Navigate } from "react-router-dom";

export const User_registration = () => {
    const { store, actions } = useContext(Context);

    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [name_contact, setNameContacto] = useState("");
    const [num_contact, setNumContacto] = useState("");
    const [create , setCreate] = useState(false)

    const isFormValid = name && name_contact && num_contact;

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const usuario = {
                name: name,
                password: password,
                name_contact: name_contact,
                num_contact: num_contact
            };

            await actions.post_usuario(usuario);
            setCreate(true)
        } catch (error) {
            console.error(error)
        }
    }

    return (
        <div className="card container mt-3" style={{width: "20rem"}}>
            <div className="card-body">
                <h1><b>Registra tu Usuario</b></h1>
                <form>
                    <div className="mb-3">
                        <label htmlFor="name" className="form-label">Name</label>
                        <input type="text" className="form-control" id="name" value={name} onChange={(e) => setName(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="inputPassword1" className="form-label">Contraseña</label>
                        <input type="password" className="form-control" id="inputPassword1" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="name_contacto" className="form-label">Nombre de Contacto</label>
                        <input type="text" className="form-control" id="name_contacto" value={name_contact} onChange={(e) => setNameContacto(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="num_contacto" className="form-label">Numero de Contacto</label>
                        <input type="text" className="form-control" id="num_contacto" value={num_contact} onChange={(e) => setNumContacto(e.target.value)} />
                    </div>
                    
                    <button disabled={!isFormValid} onClick={handleSubmit} className="btn btn-success my-2" style={{backgroundColor: "#800080"}}>
  Guardar Cambios
</button>
{create && <Navigate to='/' />}
                </form>
            </div>
        </div>
    );
};