from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    name_contact = db.Column(db.String(80), unique=True, nullable=False)
    num_contact = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name_contact":self.name_contact,
            "num_contact":self.num_contact
        }

class Product (db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    url_img = db.Column(db.String(250), unique=False, nullable=True)
    idu_img = db.Column(db.String(250), unique=False, nullable=True)
    id_category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category')

    def __repr__(self):
        return f'<Product {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "amount": self.amount,
            "url_img": self.url_img,
            "idu_img": self.idu_img,
            "id_category": self.id_category
        }
class Category (db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    url_img = db.Column(db.String(320), unique=False, nullable=False)
    idu_img = db.Column(db.String(320), unique=False, nullable=False)
    
    def __repr__(self):
        return f'<Category {self.name}>'
      
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "idu_img": self.idu_img
        }

class Order (db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String , primary_key=True)
    state = db.Column(db.String(80), unique=False, nullable=False)
    day_Date = db.Column(db.String(20), unique=False, nullable=False)
    month_Date = db.Column(db.String(20), unique=False, nullable=False)
    year_Date = db.Column(db.String(20), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f'<Orden {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "state": self.state,
            "day_Date": self.day_Date,
            "month_Date": self.month_Date,
            "year_Date": self.year_Date,
            "value": self.value,
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    id_Product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product')
    id_Order = db.Column(db.String, db.ForeignKey('order.id'), nullable=True)
    order = db.relationship('Order')

    def __repr__(self):
        return f'<Cart {self.id}>'
    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "id_Product": self.id_Product,
            "id_Order": self.id_Order
        }
