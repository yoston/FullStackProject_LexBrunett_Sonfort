from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Category (db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    url_img = db.Column(db.String(320), unique=False, nullable=False)
    idu_img = db.Column(db.String(320), unique=False, nullable=False)
    



    def __repr__(self):
        return f'<Product {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_img": self.url_img,
            "idu_img": self.idu_img
            "description": self.description,
            "price": self.price,
            "amount": self.amount,
             "url_img": self.url_img,
            "idu_img": self.idu_img,
            "id_category": self.id_category
          

