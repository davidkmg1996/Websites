from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    des = db.Column(db.String(1000))
    fPath = db.Column(db.LargeBinary)
    profPic = db.Column(db.LargeBinary)
