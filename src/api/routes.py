"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Categories
from api.utils import generate_sitemap

api = Blueprint('api', __name__)

@api.route('/Categories', methods=['GET'])
def get_Categories():

    all_Categories = Categories.query.all()
    Categories_seriallize = [Categories.serialize() for Categories in all_Categories]

    return jsonify(Categories_seriallize), 200

@api.route('/Categories', methods=['POST'])
def post_Categories():

    body = request.json
    new_Categories = Categories(name=body['name'],image=body["image"])
    db.session.add(new_Categories)
    db.session.commit()

    return jsonify({"message": "Categorias creadas con éxito"}), 200

@api.route('/Categories/<int:id>', methods=['PUT'])
def put_Categories(id):
    Categories = Categories.query.get(id)
    body = request.json

    if not Categories:
        return jsonify({"message": "Categorias no encontradas"}), 404
    
    if "name" in body:
        Categories.name = body['name']
    if "image" in body:
        Categories.image = body['image']
    
    db.session.commit()

    return jsonify({"message": "Categoria modificada con éxito"}), 200

@api.route('/Categories/<int:id>', methods=['DELETE'])
def delete_Categories(id):

    Categories = Categories.query.get(id)

    if not Categories:
        return jsonify({"message": "Categoria no encontrada"}), 404

    db.session.delete(Categories)
    db.session.commit()
    
    return jsonify({"message": "Categoria eliminada con éxito"}), 200

@api.route('/product', methods=['POST'])