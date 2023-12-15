import { initializeApp } from "firebase/app";
import { getStorage , ref , uploadBytes , getDownloadURL , deleteObject } from "firebase/storage";
import { v4 } from 'uuid';

const firebaseConfig = {
  apiKey: process.env.API_KEY,
  authDomain: process.env.AUTHDOMAIN,
  projectId: process.env.PROJECTID,
  storageBucket: process.env.STORAGEBUCKET,
  messagingSenderId: process.env.MESSAGINGSENDERID,
  appId: process.env.APPID
};

export const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);

const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      products: [],
      Orders: []
    },
    actions: {
      updateList: () => {
        fetch("/products",
          {
            headers: {
              'Content-Type': 'application/json'
            },
          }).then( response => response.json())
          .then( data => setStore({ products: data }));
      },
updateOrders: (id, obj) => {
        fetch(`/Orders/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
          .then(response => response.json())
          .then(data => console.log(data));
        
        const Order = getStore().Orders.find(Order => Order.id == id) 
        if (product.url != obj.url){
          const storageRef = ref( storage , `Orders/${obj.idu}`);
          deleteObject(storageRef);
        }
      },      
      createdOrders: (obj) => {
        fetch("/Orders", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
          .then( response => response.json())
          .then( data => console.log(data))
      },
      deleteOrders: (id,idu) => {
        fetch("/Orders/" + id, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
        }).then( response => response.json())
          .then( data => console.log(data));

        const storageRef = ref( storage , `products/${idu}`);
        deleteObject(storageRef);
      },
      updateProduct: (id, obj) => {
        fetch(`/product/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
          .then(response => response.json())
          .then(data => console.log(data));
        
        const product = getStore().products.find(product => product.id == id) 
        if (product.url != obj.url){
          const storageRef = ref( storage , `products/${obj.idu}`);
          deleteObject(storageRef);
        }
      },      
      createdProduct: (obj) => {
        fetch("/product", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
          .then( response => response.json())
          .then( data => console.log(data))
      },
      deleteProduct: (id,idu) => {
        fetch("/product/" + id, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
        }).then( response => response.json())
          .then( data => console.log(data));

        const storageRef = ref( storage , `products/${idu}`);
        deleteObject(storageRef);
      },
      upload_img : async (file) => {
        const idu =v4()
        const storageRef = ref( storage , `products/${idu}`)
        await uploadBytes( storageRef,file )
        const url = await getDownloadURL(storageRef)
        return [url,idu]
      }
    }
  };
};

export default getState;