from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product, Category, Cart, Order
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import re

api = Blueprint('api', __name__)

# Funciones auxiliares
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def handle_user_creation(body):
    required_fields = ['username', 'email', 'password', 'name_contact', 'num_contact']
    
    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    email = body['email']
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 401

    new_user = User(
        username=body['username'],
        email=email,
        name_contact=body["name_contact"],
        num_contact=body["num_contact"]
    )
    new_user.set_password(body["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 200

# Rutas de Usuarios
@api.route('/users', methods=['GET'])
def get_users():
    try:
        all_users = User.query.all()
        users_serialized = [user.serialize() for user in all_users]

        return jsonify(users_serialized), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching user data"}), 500

@api.route("/users", methods=["POST"])
def post_user():
    try:
        body = request.json
        response = handle_user_creation(body)
        return response

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the user"}), 500

@api.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    try:
        user = User.query.get(id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        body = request.json
        user.username = body.get('username', user.username)
        user.email = body.get('email', user.email)
                
        # Check if password is present in the request before updating
        if 'password' in body:
            user.set_password(body['password'])

        user.name_contact = body.get('name_contact', user.name_contact)
        user.num_contact = body.get('num_contact', user.num_contact)

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the user"}), 500

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        
        # Check if user exists
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while deleting the user"}), 500

# logins

@api.route("/login", methods=["POST"])
def post_login():
    try:
        # Retrieve user credentials from the request JSON
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        # Check if both username/email and password are provided
        if not email or not password:
            return jsonify({"error": "Invalid input", "message": "Username/Email and password are required"}), 400

        # Query the database to find the user by username or email
        user = User.query.filter(
            (User.username == email) | (User.email == email)
        ).first()

        # Check if the user is not found or the password is incorrect
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid credentials", "message": "Invalid username/email or password"}), 401
        
        # Generate an access token
        access_token = create_access_token(identity=user.id)

        # Return the access token and user information
        response_data = {
            "token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
            }
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Handle any unexpected exceptions
        return jsonify({"error": str(e), "message": "An error occurred while processing the login"}), 500

# Products

@api.route('/products', methods=['GET'])
def get_products():
    try:
        all_products = Product.query.all()
        products_serialized = [product.serialize() for product in all_products]

        # Enhance product data with category information
        products_with_category_info = []
        for product in products_serialized:
            category = Category.query.get(product["id_category"])
            if category:
                product['category_info'] = category.serialize()
                products_with_category_info.append(product)

        return jsonify(products_with_category_info), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching product data"}), 500

@api.route('/products', methods=['POST'])
def post_product():
    try:
        data = request.get_json()

        # Check if all required fields are present
        required_fields = ['name', 'description', 'price', 'amount', 'url_img', 'idu_img', 'id_category']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate if the category exists
        category_id = data['id_category']
        if not Category.query.get(category_id):
            return jsonify({"error": f"Category with id {category_id} does not exist"}), 400

        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the product"}), 500

@api.route('/products/<int:id>', methods=['PUT'])
def put_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()

        # Update product properties
        for field in ['name', 'description', 'price', 'amount', 'url_img', 'idu_img', 'id_category']:
            setattr(product, field, data.get(field, getattr(product, field)))

        # Validate if the updated category exists
        category_id = data.get('id_category', product.id_category)
        if not Category.query.get(category_id):
            return jsonify({"error": f"Category with id {category_id} does not exist"}), 400

        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the product"}), 500

@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while deleting the product"}), 500


# Categories

@api.route('/categories', methods=['GET'])
def get_categories():
    try:
        all_categories = Category.query.all()
        categories_serialized = [category.serialize() for category in all_categories]

        return jsonify(categories_serialized), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching category data"}), 500

@api.route('/categories', methods=['POST'])
def post_category():
    try:
        data = request.get_json()

        # Check if all required fields are present
        required_fields = ['name', 'url_img', 'idu_img']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Create a new category
        new_category = Category(**data)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({"message": "Category created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the category"}), 500

@api.route('/categories/<int:id>', methods=['PUT'])
def put_category(id):
    try:
        category = Category.query.get_or_404(id)
        data = request.get_json()

        # Update category properties
        for field in ['name', 'url_img', 'idu_img']:
            setattr(category, field, data.get(field, getattr(category, field)))

        db.session.commit()
        return jsonify({"message": "Category updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the category"}), 500

@api.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    try:
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while deleting the category"}), 500

# Cart

@api.route('/cart', methods=['GET'])
@jwt_required()
def get_carts():
    try:
        user_id = get_jwt_identity()
        all_items = Cart.query.filter_by(id_User=user_id, id_Order=None).all()
        items_serialized = [item.serialize() for item in all_items]

        cart_with_product_info = []
        for item in items_serialized:
            product_id = item["id_Product"]
            product = Product.query.get(product_id)
            if product:
                item['product_info'] = product.serialize()
                cart_with_product_info.append(item)

        return jsonify(cart_with_product_info), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching cart data"}), 500

@api.route('/cart/<int:id>', methods=['PUT'])
def put_cart(id):
    try:
        cart = Cart.query.get_or_404(id)
        data = request.get_json()

        for field in ['amount', 'id_Product', 'id_Order']:
            setattr(cart, field, data.get(field, getattr(cart, field)))

        db.session.commit()
        return jsonify({"message": "Cart item updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the cart item"}), 500

@api.route('/cart_add_idOrder/<int:id>', methods=['PUT'])
def add_order_cart(id):
    try:
        cart = Cart.query.get_or_404(id)
        data = request.get_json()

        for field in ['amount', 'id_Product', 'id_Order']:
            setattr(cart, field, data.get(field, getattr(cart, field)))

        db.session.commit()
        return jsonify({"message": "Order added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while adding order to the cart item"}), 500

@api.route('/cart', methods=['POST'])
def post_cart():
    try:
        data = request.get_json()

        # Check if all required fields are present
        required_fields = ['amount', 'id_Product', 'id_Order']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        existing_cart = Cart.query.filter_by(id_Product=data['id_Product'], id_Order=None).first()

        if existing_cart:
            existing_cart.amount += 1
            db.session.commit()
        else:
            new_cart = Cart(**data)
            db.session.add(new_cart)
            db.session.commit()

        return jsonify({"message": "Cart item created or updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while processing the cart item"}), 500

@api.route('/cart/<int:id>', methods=['DELETE'])
def delete_cart(id):
    try:
        cart = Cart.query.get_or_404(id)
        db.session.delete(cart)
        db.session.commit()

        return jsonify({"message": "Cart item deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while deleting the cart item"}), 500

# Orders

@api.route('/order', methods=['GET'])
@jwt_required()
def get_order():
    try:
        all_orders = Order.query.all()
        orders_with_info = []

        for order in all_orders:
            carts = Cart.query.filter_by(id_Order=order.id)
            cart_with_product_info = []

            for cart in carts:
                product = Product.query.get(cart.id_Product)
                cart_info = {"product_info": product.serialize()}
                cart_with_product_info.append(cart_info)

            order_item = order.serialize()
            order_item["products"] = cart_with_product_info
            orders_with_info.append(order_item)

        return jsonify(orders_with_info), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching order data"}), 500

@api.route('/order/<id>', methods=['PUT'])
def put_order(id):
    try:
        order = Order.query.get_or_404(id)
        data = request.get_json()

        for field in ['state', 'day_Date', 'month_Date', 'year_Date', 'value']:
            setattr(order, field, data.get(field, getattr(order, field)))

        db.session.commit()
        return jsonify({"message": "Order updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the order"}), 500

@api.route('/order', methods=['POST'])
def post_order():
    try:
        data = request.get_json()

        # Check if all required fields are present
        required_fields = ['id', 'day_Date', 'month_Date', 'year_Date', 'value']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        new_order = Order(
            id=data['id'],
            state=data.get('state', 'Creada'),
            day_Date=data['day_Date'],
            month_Date=data['month_Date'],
            year_Date=data['year_Date'],
            value=data['value']
        )

        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the order"}), 500

@api.route('/order/<id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while deleting the order"}), 500

@api.route('/all_order', methods=['GET'])
@jwt_required()
def get_all_order():
    try:
        all_orders = Order.query.all()
        orders_with_info = []

        for order in all_orders:
            carts = Cart.query.filter_by(id_Order=order.id)
            cart_with_product_info = []

            for cart in carts:
                product = Product.query.get(cart.id_Product)
                cart_info = {"product_info": product.serialize()}
                cart_with_product_info.append(cart_info)

            order_item = order.serialize()
            order_item["products"] = cart_with_product_info
            orders_with_info.append(order_item)

        return jsonify(orders_with_info), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching all order data"}), 500
