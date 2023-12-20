from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Admin, Orders
from api.utils import generate_sitemap

api = Blueprint('api', __name__)

@api.route('/admin', methods=['GET'])
def get_admins():

    all_admin = Admin.query.all()
    admin_serialize = [Admin.serialize() for Admin in all_admin]

    return jsonify(admin_serialize), 200

@api.route('/admin', methods=['POST'])
def post_admins():

    body = request.json
    new_admin = Orders(id=body['id'],name=body['name'],description=body['description'],price=body['price'],amount=body['amount'])
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({"message": "Admin creado con éxito"}), 200

@api.route('/admin/<id>', methods=['PUT'])
def put_admin(id):
    admin = Admin.query.get(id)
    body = request.json

    if not admin:
        return jsonify({"message": "Admin no encontrado"}), 404
    
    admin.name = body['name']
    admin.description = body['description']
    admin.category = body['category']
    admin.products = body['products']

    db.session.commit()
    
    return jsonify({"message": "Admin modificada con éxito"}), 200

@api.route('/admin/<id>', methods=['DELETE'])
def delete_admin(id):

    admin = Admin.query.get(id)

    if not admin:
        return jsonify({"message": "Admin no encontrado"}), 404

    db.session.delete(admin)
    db.session.commit()
    
    return jsonify({"message": "Admin eliminada con éxito"}), 200

@api.route('/Orders', methods=['GET'])
def get_Orders():

    all_Orders = Orders.query.all()
    Orders_serialize = [Orders.serialize() for Orders in all_Orders]

    return jsonify(Orders_serialize), 200

@api.route('/Orders', methods=['POST'])
def post_Orders():

    body = request.json
    new_Orders = Orders(id=body['id'],status=body['status'],payment=body['payment'],products=body['products'])
    db.session.add(new_admin)
    db.session.commit()
    

    return jsonify({"message": "Order creado con éxito"}), 200

@api.route('/Orders/<id>', methods=['PUT'])
def put_admin(id):
    Orders = Orders.query.get(id)
    body = request.json

    if not Orders:
        return jsonify({"message": "Orders no encontrado"}), 404
    
    Orders.status = body['status']
    Orders.payment = body['payment']
    Orders.products = body['products']

    db.session.commit()
    
    return jsonify({"message": "Orders modificada con éxito"}), 200

@api.route('/Orders/<id>', methods=['DELETE'])
def delete_Orders(id):

    Orders = Orders.query.get(id)

    if not Orders:
        return jsonify({"message": "Orders no encontrado"}), 404

    db.session.delete(Orders)
    db.session.commit()
    
    return jsonify({"message": "Orders eliminada con éxito"}), 200

from api.models import db, User, Product, Categories, Cart,  Orders
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

@api.route('/category', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()
    categories_serialize = [Categories.serialize() for Categories in all_categories]

    return jsonify(categories_serialize), 200

@api.route('/category', methods=['POST'])
def post_categories():
    body = request.json
    new_categories = Category(
        name=body['name'],
        url_img=body['url_img'],
        idu_img=body['idu_img']
    )
    db.session.add(new_categories)
    db.session.commit()

    return jsonify({"message": "Categoría creada con éxito"}), 200

@api.route('/category/<int:id>', methods=['PUT'])
def put_categories(id):
    categories = Category.query.get(id)

    if not categories:
        return jsonify({"message": "Categoría no encontrada"}), 404
    body = request.json

    categories.name = body['name']
    categories.url_img = body['url_img']
    categories.idu_img = body['idu_img']

    db.session.commit()

    return jsonify({"message": "Categoría modificada con éxito"}), 200

@api.route('/category/<int:id>', methods=['DELETE'])
def delete_categories(id):
    categories = Category.query.get(id)

    if not categories:
        return jsonify({"message": "Categoría no encontrada"}), 404
    
    db.session.delete(categories)
    db.session.commit()

    return jsonify({"message": "Categoría eliminada con éxito"}), 200

