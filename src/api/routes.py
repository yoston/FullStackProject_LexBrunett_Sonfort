"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
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