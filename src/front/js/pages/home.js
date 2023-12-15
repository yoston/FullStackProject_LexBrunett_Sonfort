import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { Link } from "react-router-dom";

export const Home = () => {
	const { store, actions } = useContext(Context);
	

	return (
		<div className="text-center mt-5">
			<Link to="/Categories">
				<button>categorias</button>
      			</Link>
    
			<Link to="/products">
				<button>products</button>
			</Link>

			<Link to="/user_registration">
				<button>Registro</button>
			</Link>

			<Link to="/user_login">
				<button>Login</button>
			</Link>
		</div>
	);
};