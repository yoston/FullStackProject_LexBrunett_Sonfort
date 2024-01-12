
# """
# This module takes care of starting the API Server, Loading the DB and Adding the endpoints
# """


# import os
# from flask import Flask, request, jsonify, url_for, send_from_directory
# from flask_migrate import Migrate
# from flask_swagger import swagger
# from flask_cors import CORS
# from api.utils import APIException, generate_sitemap
# from api.models import db
# from api.routes import api
# from api.admin import setup_admin
# from api.commands import setup_commands

# from flask_jwt_extended import JWTManager

# from flask import Flask
# from firebase_admin import credentials,initialize_app


# cred = credentials.Certificate("api/key.json")


# default_app = initialize_app(cred)


# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "12345678"
    
#     from .userApi import userApi
#     app.register_blueprint(userApi, url_prefix = "/user")

    








# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries

# // Your web app's Firebase configuration
# const firebaseConfig = {
#   apiKey: "AIzaSyCblEsWNHBMkJEymbCnh0lJqy1LUI3qiJk",
#   authDomain: "digitalstore-58a25.firebaseapp.com",
#   projectId: "digitalstore-58a25",
#   storageBucket: "digitalstore-58a25.appspot.com",
#   messagingSenderId: "766747723027",
#   appId: "1:766747723027:web:2a5a6f11fb7797501e86e6"
# };

# // Initialize Firebase
# const app = initializeApp(firebaseConfig);

