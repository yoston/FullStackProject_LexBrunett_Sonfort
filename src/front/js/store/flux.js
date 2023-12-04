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
      Categories: []
    },
    actions: {
      updateList: () => {
        fetch("/Categories",
          {
            headers: {
              'Content-Type': 'application/json'
            },
          }).then( response => response.json())
          .then( data => setStore({ Categories: data }));
      },
      updateCategories: (id, obj) => {
        fetch(`/Categories/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
          .then(response => response.json())
          .then(data => console.log(data));
        
        const Category = getStore().Categories.find(Category => Category.id == id) 
        if (Category.url != obj.url){
          const storageRef = ref( storage , `Categories/${obj.idu}`);
          deleteObject(storageRef);
        }
      },      
      createdProduct: (obj) => {
        fetch("/Categories", {
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
        fetch("/Categories/" + id, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
        }).then( response => response.json())
          .then( data => console.log(data));

        const storageRef = ref( storage , `Categories/${idu}`);
        deleteObject(storageRef);
      },
      upload_img : async (file) => {
        const idu =v4()
        const storageRef = ref( storage , `Categories/${idu}`)
        await uploadBytes( storageRef,file )
        const url = await getDownloadURL(storageRef)
        return [url,idu]
      }
    }
  };
};

export default getState;