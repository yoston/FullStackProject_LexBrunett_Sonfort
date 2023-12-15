"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product, Categories, Cart,  Orders
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

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


@api.route('/cart', methods=['GET'])
@jwt_required()
def get_carts():
    id = get_jwt_identity()

    all_items = Cart.query.filter_by( id_Restaurant = id  , id_Order = None ).all()
    items_serialize = [item.serialize() for item in all_items]
    cart_with_product_info = []

    for item in items_serialize:
        product_id = item["id_Product"]
        product = Product.query.get(product_id)
        if product:
            item['product_info'] = product.serialize()
        cart_with_product_info.append(item)

    return jsonify(cart_with_product_info), 200

@api.route('/cart/<int:id>', methods=['PUT'])
def put_cart(id):
    cart = Cart.query.get(id)

    if not cart:
        return jsonify({"message": "Carrito no encontrado"}), 404
    
    body = request.json

    cart.amount = body['amount']
    cart.id_Producto = body['id_Product']
    cart.id_Restaurant = body['id_Restaurant']
    cart.id_Order = body['id_Order']

    db.session.commit()

    return jsonify({"message": "Carrito modificado con éxito"}), 200

@api.route('/cart_add_idOrder/<int:id>', methods=['PUT'])
def add_order_cart(id):
    cart = Cart.query.get(id)

    if not cart:
        return jsonify({"message": "Carrito no encontrado"}), 404
    
    body = request.json

    cart.amount = body['amount']
    cart.id_Producto = body['id_Product']
    cart.id_Restaurant = body['id_Restaurant']
    cart.id_Order = body['id_Order']

    db.session.commit()

    return jsonify({"message": "orden annadida con éxito"}), 200

@api.route('/cart', methods=['POST'])
def post_cart():
    body = request.json

    existente = Cart.query.filter_by(id_Product = body['id_Product'], id_Restaurant = body['id_Restaurant'], id_Order = None).first()

    if (existente):
        existente.amount = existente.amount + 1,
        existente.id_Product=body['id_Product'],
        existente.id_Restaurant=body['id_Restaurant'],
        existente.id_Order = body['id_Order'],

        db.session.commit()
    else : 
        new_cart = Cart(
            amount=body['amount'],
            id_Product=body['id_Product'],
            id_Restaurant=body['id_Restaurant'],
            id_Order = body['id_Order']
        )

        db.session.add(new_cart)
        db.session.commit()

    return jsonify({"message": "Carrito creado con éxito"}), 200

@api.route('/cart/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get(id)

    if not cart:
        return jsonify({"message": "Carrito no encontrado"}), 404
    
    db.session.delete(cart)
    db.session.commit()

    return jsonify({"message": "Carrito eliminado con éxito"}), 200
