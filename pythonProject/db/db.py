__author__ = "nicolaanghileri"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String, primary_key=True)
    password = db.column(db.Password)
    children = db.relationship('Child', backref='users', lazy='True')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}:"


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    weight = db.Column(db.Double)
    height = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, birth_date, weight, height):
        self.name = name
        self.birth_date = birth_date
        self.weight = weight
        self.height = height

    def _repr(self):
        return f"{self.name}:{self.birth_date}:{self.weight}:{self.height}"