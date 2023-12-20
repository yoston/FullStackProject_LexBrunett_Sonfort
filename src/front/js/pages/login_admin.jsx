import React, { useState , useContext } from "react";
import { Context } from "../store/appContext";

export const Admin_login = () => {
    const { store , actions } = useContext( Context );

    const [email , setEmail] = useState("");
    const [password , setPassword] = useState("");

    return (
        <form>
            <div className="mb-3">
                <label htmlFor="inputName1" className="form-label">Name</label>
                <input type="text" className="form-control" id="inputName1" value={email} onChange={(e) => setEmail(e.target.value)}/>
            </div>
            <div className="mb-3">
                <label htmlFor="inputPassword1" className="form-label">Password</label>
                <input type="password" className="form-control" id="inputPassword1" value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>
            <div>
                <button className="btn btn-primary" onClick={(e) => {e.preventDefault(); actions.postAdmin(email,password)}}>Login</button>
            </div>
        </form>
    )
}