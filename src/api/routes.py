from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product, Category, Cart, Order
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


api = Blueprint('api', __name__)

@api.route('/user', methods=['GET'])
def get_user():
    try:
        all_users = User.query.all()

        # Serialize user data
        users_serialized = [user.serialize() for user in all_users]

        return jsonify(users_serialized), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while fetching user data"}), 500


@api.route("/user", methods=["POST"])
def post_user():
    body = request.json
    user = User.query.filter_by(email=body['email']).first()

    if user:
        return jsonify({"msg": "User already exists"}), 401

    new_user = User(
        username=body['username'],
        email=body['email'],
        password=body["password"],
        name_contact=body["name_contact"],
        num_contact=body["num_contact"]
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 200

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg" : "Usuario creado"}) , 200

@api.route('/user/<int:id>', methods=['PUT'])
def put_user(id):
    try:
        user = User.query.get(id)

        # Check if user exists
        if not user:
            return jsonify({"message": "User not found"}), 404

        body = request.json

        # Update user properties
        user.username = body.get('username', user.username)
        user.email = body.get('email', user.email)
        user.password = body.get('password', user.password)
        user.name_contact = body.get('name_contact', user.name_contact)
        user.num_contact = body.get('num_contact', user.num_contact)

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the user"}), 500

@api.route('/user/<int:id>', methods=['DELETE'])
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


# Error handling in a route
@api.route("/login_user", methods=["POST"])
def post_login_user():
    try:
        username = request.json.get("name", None)
        password = request.json.get("password", None)
        
        user = User.query.filter_by(username=username, password=password).first()

        if user is None:
            return jsonify({"error": "Invalid credentials", "message": "Bad username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({ "token": access_token, "user_id": user.id, "name": user.name}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred during login"}), 500

@api.route("/login_admin", methods=["POST"])
def post_login_admin():
    try:
        # Retrieve user credentials from the request JSON
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        # Check if both email and password are provided
        if not email or not password:
            return jsonify({"error": "Invalid input", "message": "Email and password are required"}), 400

        # Query the database to find the user by email and password
        user = User.query.filter_by(email=email, password=password).first()

        # Check if the user is not found
        if user is None:
            return jsonify({"error": "Invalid credentials", "message": "Bad email or password"}), 401

        # Generate an access token
        access_token = create_access_token(identity=user.id)

        # Return the access token and user information
        return jsonify({"token": access_token, "user_id": user.id, "user": "admin"}), 200

    except Exception as e:
        # Handle any unexpected exceptions
        return jsonify({"error": str(e), "message": "An error occurred while processing the login"}), 500


@api.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    products_serialize = [product.serialize() for product in all_products]
    product_with_product_info = []

    for item in products_serialize:
        category_id = item["id_category"]
        category = Category.query.get(category_id)
        
        if category:
            item['category_info'] = category.serialize()
            product_with_product_info.append(item)

    return jsonify(products_serialize), 200

@api.route('/products', methods=['POST'])
def post_product():
    try:
        body = request.json

        # Validate that required fields are present in the request
        required_fields = ['name', 'description', 'price', 'amount', 'url_img', 'idu_img', 'id_category']
        for field in required_fields:
            if field not in body:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        new_product = Product(
            name=body['name'],
            description=body['description'],
            price=body['price'],
            amount=body['amount'],
            url_img=body['url_img'],
            idu_img=body['idu_img'],
            id_category=body['id_category']
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the product"}), 500


@api.route('/products/<int:id>', methods=['PUT'])
def put_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Producto no encontrado"}), 404
    
    body = request.json
    product.name = body['name']
    product.description = body['description']
    product.price = body['price']
    product.amount = body['amount']
    product.url_img = body['url']
    product.idu_img = body['idu']
    product.id_category = body['id_category']
    db.session.commit()

    return jsonify({"message": "Producto modificado con éxito"}), 200

@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Producto no encontrado"}), 404
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Producto eliminado con éxito"}), 200

@api.route('/category', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()
    categories_serialize = [Category.serialize() for Categories in all_categories]

    return jsonify(categories_serialize), 200

@api.route('/category', methods=['POST'])
def post_categories():
    try:
        body = request.json

        # Validate that required fields are present in the request
        required_fields = ['name', 'url_img', 'idu_img']
        for field in required_fields:
            if field not in body:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        new_category = Category(
            name=body['name'],
            url_img=body['url_img'],
            idu_img=body['idu_img']
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({"message": "Category created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while creating the category"}), 500


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

@api.route('/cart', methods=['GET'])
@jwt_required()
def get_carts():
    id = get_jwt_identity()

    all_items = Cart.query.filter_by(id_Restaurant=id, id_Order=None).all()
    items_serialize = [item.serialize() for item in all_items]
    cart_with_product_info = []

    for item in items_serialize:
        product_id = item["id_Product"]
        product = Product.query.get(product_id)
        if product:
            item['product_info'] = product.serialize()
            cart_with_product_info.append(item)
    print(cart_with_product_info)
    return jsonify(cart_with_product_info), 200

@api.route('/cart/<int:id>', methods=['PUT'])
def put_cart(id):
    try:
        cart = Cart.query.get(id)

        # Check if cart item exists
        if not cart:
            return jsonify({"message": "Cart item not found"}), 404

        body = request.json

        # Update cart item properties
        cart.amount = body.get('amount', cart.amount)
        cart.id_Product = body.get('id_Product', cart.id_Product)
        cart.id_Order = body.get('id_Order', cart.id_Order)

        db.session.commit()

        return jsonify({"message": "Cart item updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the cart item"}), 500

@api.route('/cart_add_idOrder/<int:id>', methods=['PUT'])
def add_order_cart(id):
    try:
        cart = Cart.query.get(id)

        # Check if cart item exists
        if not cart:
            return jsonify({"message": "Cart item not found"}), 404

        body = request.json

        # Update cart item properties with order information
        cart.amount = body.get('amount', cart.amount)
        cart.id_Product = body.get('id_Product', cart.id_Product)
        cart.id_Order = body.get('id_Order', cart.id_Order)

        db.session.commit()

        return jsonify({"message": "Order added to cart item successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while adding order to the cart item"}), 500


@api.route('/cart', methods=['POST'])
def post_cart():
    body = request.json

    existente = Cart.query.filter_by(id_Product = body['id_Product'], id_Order = None).first()

    if (existente):
        existente.amount = existente.amount + 1,
        existente.id_Product=body['id_Product'],
        existente.id_Order = body['id_Order'],

        db.session.commit()
    else :
        new_cart = Cart(
            amount=body['amount'],
            id_Product=body['id_Product'],
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

@api.route('/order', methods=['GET'])
@jwt_required()
def get_order(): 
    
    all_order = Order.query.all()
    order_seriallize = [item.serialize() for item in all_order]
    order_with_info = []

    for item in order_seriallize:
        order_item = item.copy()
        order_with_info.append(order_item)

    return jsonify(order_with_info), 200

@api.route('/all_order', methods=['GET'])
@jwt_required()
def get_all_order():
    all_order = Order.query.all()
    order_with_info = []

    for item in all_order:
        carts = Cart.query.filter_by(id_Order=item.id)
        cart_with_product_info = []

        for cart in carts:
            product = Product.query.get(cart.id_Product)
            cart_info = {
                'product_info': product.serialize(),
            }
            cart_with_product_info.append(cart_info)

        order_item = item.serialize()

        order_item['products'] = cart_with_product_info
        order_with_info.append(order_item)

    return jsonify(order_with_info), 200


@api.route('/order/<id>', methods=['PUT'])
def put_order(id):
    try:
        order = Order.query.get(id)

        # Check if order exists
        if not order:
            return jsonify({"message": "Order not found"}), 404

        body = request.json

        # Update order properties
        order.state = body.get('state', order.state)
        order.day_Date = body.get('day_Date', order.day_Date)
        order.month_Date = body.get('month_Date', order.month_Date)
        order.year_Date = body.get('year_Date', order.year_Date)
        order.value = body.get('value', order.value)

        db.session.commit()

        return jsonify({"message": "Order updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e), "message": "An error occurred while updating the order"}), 500


@api.route('/order', methods=['POST'])
def post_order():
    body = request.json
    new_order = Order(
        id=body["id"],
        state= "Creada",
        day_Date=body["day_Date"],
        month_Date=body["month_Date"],
        value=body["value"],
        year_Date=body["year_Date"],
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Orden creada con éxito"}), 200

@api.route('/order/<id>', methods=['DELETE'])
def delete_order(id):

    order = Order.query.get(id)

    if not order:
        return jsonify({"message": "Orden no encontrada"}), 404

    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Orden eliminada con éxito"}), 200