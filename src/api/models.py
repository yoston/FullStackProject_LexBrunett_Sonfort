from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean(), unique=True, nullable=False)
    payment = db.Column(db.Boolean(), unique=False, nullable=False)
    # Establece la relación uno a muchos con productos
    products = db.relationship('Product', backref='Trademark', lazy=True)

    def __repr__(self):

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "url_img": self.url_img,
            "idu_img": self.idu_img
            "description": self.description,
            "price": self.price,
            "amount": self.amount,

