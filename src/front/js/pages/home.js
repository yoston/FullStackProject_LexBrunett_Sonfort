import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Carousel } from "../component/carrusel.jsx";
import { Products_user } from "./products_user.jsx"
import "../../styles/home.css";

export const Home = () => {
	const {store} = useContext(Context)
	
	return (
		<div style={{overflow: "hidden"}}>	
			<Carousel/>
			<Products_user/>
		</div>
	);
};