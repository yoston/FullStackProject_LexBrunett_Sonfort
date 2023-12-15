"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from sqlalchemy import func


api = Blueprint('api', __name__)

@api.route("/user", methods=["POST"])
def post_user():
    body = request.json
    user = User.query.filter_by(email = body['email']).first()
    print(body)
    print(user)
    if user:
        return jsonify({"msg": "Usuario ya existe"}), 401
    
    next_user_id = (db.session.query(func.max(User.id)).scalar() or 0) + 1
    
    new_user = User(
        id= next_user_id,
        email=body['email'],
        password=body["password"]
    )

    db.session.add(new_user)
    db.session.commit()
 
    return jsonify({"msg" : "Usuario creado"}) , 200

@api.route("/token", methods=["POST"])
def post_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email, password=password).first()
    if User is None:
        return jsonify({"msg": "Bad username or password"}), 401
 
    access_token = create_access_token(identity=user.email)
    return jsonify({ "token": access_token, "user_id": user.email })

@api.route('/products', methods=['GET'])
def get_products():

    all_products = Product.query.all()
    products_seriallize = [product.serialize() for product in all_products]

    return jsonify(products_seriallize), 200

@api.route('/product', methods=['POST'])
def post_product():
    body = request.json

    new_product = Product(
        id=body['id'],
        name=body['name'],
        description=body['description'],
        Category=body['Category'],
        price=body['price'],
        amount=body['amount'],
        img=body['url'],
        idu=body['idu']
    )

    product = Product.query.filter_by(id=body['id']).first()
    if (product) :
        return jsonify({"message": "Prducto no creado, el ID ya existe"}), 400
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Producto creado con exito"}), 200

@api.route('/product/<id>', methods=['PUT'])
def put_product(id):
    product = Product.query.get(id)
    body = request.json

    if not product:
        return jsonify({"message": "Producto no encontrado"}), 404
    
    product.name = body['name']
    product.description = body['description']
    product.Category = body['Category']
    product.price = body['price']
    product.amount = body['amount']
    product.img=body['url']
    product.idu=body['idu']

    db.session.commit()
    
    return jsonify({"message": "Producto modificado con exito"}), 200

@api.route('/product/<id>', methods=['DELETE'])
def delete_product(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Producto no encontrado"}), 404

    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Producto eliminado con éxito"}), 200


@api.route('/carrito', methods=['GET'])
def get_carrito():
    all_items = Carrito.query.all()
    items_serialize = [item.serialize() for item in all_items]
    carrito_with_product_info = []
    for item in items_serialize:
        product_id = item["id_Producto"]
        product = Product.query.get(product_id)
        if product:
            item['product_info'] = product.serialize()
        carrito_with_product_info.append(item)
    return jsonify(carrito_with_product_info), 200

@api.route('/carrito/<int:id>', methods=['PUT'])
def put_carrito(id):
    carrito = Carrito.query.get(id)
    if not carrito:
        return jsonify({"message": "Carrito no encontrado"}), 404
    body = request.json
    carrito.cantidad = body['cantidad']
    carrito.id_Producto = body['id_Producto']
    carrito.id_User = body['id_User']
    db.session.commit()
    return jsonify({"message": "Carrito modificado con éxito"}), 200

@api.route('/carrito', methods=['POST'])
def post_carrito():
    body = request.json
    carrito = Carrito.query.filter_by(id=body['id']).first()
    if carrito:
        return jsonify({"message": "Carrito no creado, el ID ya existe"}), 400
    new_carrito = Carrito(
        id=body['id'],
        cantidad=body['cantidad'],
        id_Producto=body['id_Producto'],
        id_User=body['id_User']
    )
    db.session.add(new_carrito)
    db.session.commit()
    return jsonify({"message": "Carrito creado con éxito"}), 200

@api.route('/carrito/<int:id>', methods=['DELETE'])
def delete_carrito(id):
    carrito = Carrito.query.get(id)
    if not carrito:
        return jsonify({"message": "Carrito no encontrado"}), 404
    db.session.delete(carrito)
    db.session.commit()
    return jsonify({"message": "Carrito eliminado con éxito"}), 200
