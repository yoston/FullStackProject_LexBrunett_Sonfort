
/* const firebaseConfig = {

  apiKey: process.env.API_KEY,
  authDomain: process.env.AUTHDOMAIN,
  projectId: process.env.PROJECTID,
  storageBucket: process.env.STORAGEBUCKET,
  messagingSenderId: process.env.MESSAGINGSENDERID,
  appId: process.env.APPID
}; */

//const firebaseConfig = JSON.parse(process.env.FIREBASE_CONFIG)

import { initializeApp } from "firebase/app";
import { getStorage , ref , uploadBytes , getDownloadURL , deleteObject } from "firebase/storage";
import { v4 } from 'uuid';

const firebaseConfig = {
  apiKey: "AIzaSyDSBh1QQAFrXNhHBZjxrPBaoCnS6FwsjEs",
  authDomain: "sonfort-623bb.firebaseapp.com",
  projectId: "sonfort-623bb",
  storageBucket: "sonfort-623bb.appspot.com",
  messagingSenderId: "1018044863257",
  appId: "1:1018044863257:web:51c90cd6e49ea26dcbeb88",
  measurementId: "G-X94FGL5BRV"
};

export const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);

const getState = ({ getStore, getActions, setStore }) => {
  
	return {
		store: {
			categories: [],
			products: [],
			carrito: [],
			order: [],
			auth: false,
			user: null,
			creado: null,
			priceOrder: null,
			selectOpcion: null,
			name: null,
			errorLogin : false
		},
		actions: { 
			setErrorLogin : (i) => {
				setStore({errorLogin : i})
			},
			setSelectOpcion : (opcion) => {
				setStore({selectOpcion : opcion})
				console.log(opcion)
			},
			setPriceOrder: (price) => {
				setStore({priceOrder : price})
			},
			vaciar: () => {
				setStore({creado : false})
			},
			creado: () => {
				setStore({creado : true})
			},
			validar: () => {
				if ( localStorage.getItem("id") && localStorage.getItem("token")) {
					setStore({ auth : true})
				}
			},
			postUser: async (email,password) => {
				await fetch(process.env.BACKEND_URL + "api/users", {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify({
						email : email,
						password: password
					})
				})
				.then((response)=> {
					if (response.status == 200){
						setStore({ auth : true})
					}
					else{
						setStore({ errorLogin : true })
					}
					return response.json()
				})
				.then((data)=> {
					localStorage.setItem("token",data.token);
					localStorage.setItem("id",data.user_id);
					setStore({user : data.user})
					setStore({name : data.name})
				})
				await getActions().getCart()
			},

			post_user: async (obj) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + 'api/users', {
					method: 'POST',
					headers: {
					'Content-Type': 'application/json',
					},
				body: JSON.stringify(obj),
				});

			if (!response.ok) {
			// Manejo de errores para respuestas HTTP no exitosas
			throw new Error(`Error: ${response.status} - ${response.statusText}`);
			}

			const data = await response.json();
			console.log(data);

			// Llamar a la función getUser después de completar la solicitud con éxito
			await getActions().getUser();
			} catch (error) {
			// Manejo de errores generales
			console.error('Error al realizar la solicitud POST:', error);
			}
			},
			
			postAdmin: (email,password) => {
				fetch(process.env.BACKEND_URL + "api/login_admin", {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify({
						email : email,
						password: password
					})
				})
				.then((response)=> {
					if (response.status == 200){
						setStore({ auth : true})
					}
					else {
						setStore({ errorLogin : true })
					}
					return response.json()
				})
				.then((data)=> {
					localStorage.setItem("token",data.token);
					localStorage.setItem("id",data.user_id);
					setStore({user : data.user})
				})
			},
			logout : () => {
				setStore({ auth : false});
				localStorage.removeItem("token");
				localStorage.removeItem("id")
				setStore({user : "null"})
				getActions().getCart()
			},
				postRegister: (user) => {
					fetch(process.env.BACKEND_URL + "api/user", {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'Access-Control-Allow-Origin':'*'
						},
						body: JSON.stringify(user)
					})
					.then((response)=> response.json())
					.then((data)=> console.log(data))
				},
			getCategories: async() => {
				const response = await fetch(process.env.BACKEND_URL + 'api/category')
				const body = await response.json();
				setStore({categories: body})
			},
			postCategories : async (obj) => {
				await fetch(process.env.BACKEND_URL + "api/category", {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(obj)
				})
				.then((response)=> response.json())
				.then((data)=> console.log(data))
				await getActions().getCategories()
			},
			putCategories : async (id,obj) => {
				await fetch(process.env.BACKEND_URL + 'api/category/'+id, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(obj) 
				})
				.then((response)=> response.json())
				.then((data)=> console.log(data));
				await getActions().getCategories()
			},
			deleteCategories : async (id) => {
				await fetch(process.env.BACKEND_URL + 'api/category/'+id, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
				})
				.then((response) => response.json())
				.then((data) => console.log(data))
				await getActions().getCategories()
			},			
			getList: () => {
				fetch(process.env.BACKEND_URL + 'api/products', 
				{
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
				})
				.then( response => response.json())
				.then( data => setStore({ products: data }));
			},
			putProduct: async (id, obj) => {
				await fetch(process.env.BACKEND_URL + `api/products/${id}`, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(obj)
				})
				.then(response => response.json())
				.then(data => console.log(data));
				
				const product = await getStore().products.find(product => product.id == id) 
				await getActions().getList()
			},      
			postProduct: async (obj) => { 
				await fetch(process.env.BACKEND_URL + 'api/products', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(obj)
				})
				.then( response => response.json())
				.then( data => console.log(data))
				await getActions().getList()
			},
			deleteProduct: async (id) => {
				await fetch(process.env.BACKEND_URL + 'api/products/' + id, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin':'*'
				},
				}).then( response => response.json())
				.then( data => console.log(data));
				
				await getActions().getList()
				//const storageRef = ref( storage , `products/${idu}`);
				//await deleteObject(storageRef);
			},
			upload_img : async (file) => {
				const idu =v4()
				const storageRef = ref( storage , `products/${idu}`)
				await uploadBytes( storageRef,file )
				const url = await getDownloadURL(storageRef)
				return [url,idu]
			},
			getCart :  () => {
				fetch(process.env.BACKEND_URL + 'api/cart', {
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*',
						'Authorization': `Bearer ${localStorage.getItem('token')}`
					},
				})
				.then((response) => response.json())
				.then((data) =>{setStore({ carrito: data });console.log("carrito", data)})
			},
			putCart : async (updatedCart , id) => {
				await fetch(process.env.BACKEND_URL + 'api/cart/'+ id, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(updatedCart)
				})
				.then((response) => response.json())
				.then((data) => console.log(data))
				await getActions().getCart()
			},
			addOrderCart : async (updatedCart , id) => {
				await fetch(process.env.BACKEND_URL + 'api/cart_add_idOrder/'+ id, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(updatedCart)
				})
				.then((response) => response.json())
				.then((data) => console.log(data))
				await getActions().getCart()
			},
			postCart: async (amount,id_product,id_restaurant) => {
				await fetch(process.env.BACKEND_URL + 'api/cart', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify({
						amount : amount,
						id_Product : id_product,
						id_Restaurant : id_restaurant,
						id_Order: null
					}) 
				})
				.then( response => response.json())
				.then( data => console.log(data))
				await getActions().getCart()
			},
			deleteCart : async (id) => {
				await fetch(process.env.BACKEND_URL + 'api/cart/' + id, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					}
				})
				.then( response => response.json())
				.then( data => console.log(data));
				await getActions().getCart()
			},
			getOrder :  (token) => {
				fetch(process.env.BACKEND_URL + 'api/order', {
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*',
						'Authorization': `Bearer ${token}`
					},
				})
				.then((response) => response.json())
				.then((data) =>{setStore({ order : data });console.log(data)})
			},
			getAllOrder : (token) => {
				fetch(process.env.BACKEND_URL + 'api/all_order', {
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*',
						'Authorization': `Bearer ${token}`
					},
				})
				.then((response) => response.json())
				.then((data) => setStore({ order : data }))
			},
			putOrder : async (updatedOrder , id) => {
				console.log(updatedOrder)
				await fetch(process.env.BACKEND_URL + 'api/order/'+ id, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(updatedOrder)
				})
				.then((response) => response.json())
				.then((data) => console.log(data))
				await getActions().getAllOrder(localStorage.getItem("token"))
			},
			postOrder: async (order) => {
				order.id = v4();
				console.log(order);
				await fetch(process.env.BACKEND_URL + 'api/order', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					},
					body: JSON.stringify(order) 
				})
				.then( response => response.json())
				.then( data => console.log(data))
				await getActions().getOrder(localStorage.getItem("token"))
				return order.id;
			},
			deleteOrder : async (id) => {
				await fetch(process.env.BACKEND_URL + 'api/order/' + id, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin':'*'
					}
				})
				.then( response => response.json())
				.then( data => console.log(data));
				await getActions().getAllOrder(localStorage.getItem("token"))
			},
		}
	};
};

export default getState;