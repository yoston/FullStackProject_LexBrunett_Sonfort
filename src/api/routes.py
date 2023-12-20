from flask import Flask, request, jsonify, url_for, Blueprint
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


