import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Navigate } from "react-router-dom";

export const User_registration = () => {
    const { actions } = useContext(Context);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [nameContact, setNameContact] = useState("");
    const [numContact, setNumContact] = useState("");
    const [create, setCreate] = useState(false);
    const [error, setError] = useState(null);

    const isFormValid = username && email && password && nameContact && numContact;

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const usuario = {
                username: username,
                email: email,
                password: password,
                name_contact: nameContact,
                num_contact: numContact
            };

            await actions.post_user(usuario);
            setCreate(true);
        } catch (error) {
            console.error("Error al registrar el usuario:", error);
            setError("Error al registrar el usuario. Por favor, inténtalo de nuevo.");
        }
    };

    return (
        <div className="card container mt-3" style={{ width: "20rem" }}>
            <div className="card-body">
                <h1><b>Registra tu Usuario</b></h1>
                <form>
                    <div className="mb-3">
                        <label htmlFor="username" className="form-label">Nombre de Usuario</label>
                        <input type="text" className="form-control" id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Correo Electrónico</label>
                        <input type="email" className="form-control" id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="inputPassword1" className="form-label">Contraseña</label>
                        <input type="password" className="form-control" id="inputPassword1" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="nameContact" className="form-label">Nombre de Contacto</label>
                        <input type="text" className="form-control" id="nameContact" value={nameContact} onChange={(e) => setNameContact(e.target.value)} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="numContact" className="form-label">Numero de Contacto</label>
                        <input type="text" className="form-control" id="numContact" value={numContact} onChange={(e) => setNumContact(e.target.value)} />
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
