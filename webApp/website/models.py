from flask_login import UserMixin
from website import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    ikon = db.Column(db.Integer(), default = 0)
    epic = db.Column(db.Integer(), default = 0)
    mc = db.Column(db.Integer(), default = 0)
    powder = db.Column(db.Integer(), default = 0)
    indy = db.Column(db.Integer(), default=0)
    fav1 = db.Column(db.String(length=100))
    fav2 = db.Column(db.String(length=100))
    fav3 = db.Column(db.String(length=100))
    fav4 = db.Column(db.String(length=100))



class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False, unique=True)
    state = db.Column(db.String(length=2), nullable=False)
    reigon = db.Column(db.String(length=20), nullable=False)
    lat = db.Column(db.String(length=100), nullable=False)
    lon = db.Column(db.String(length=100), nullable=False)
    ikon = db.Column(db.Integer(), default = 0)
    epic = db.Column(db.Integer(), default = 0)
    mc = db.Column(db.Integer(), default = 0)
    powder = db.Column(db.Integer(), default = 0)
    indy = db.Column(db.Integer(), default = 0)
    forecast0 = db.Column(db.Float())
    forecast1 = db.Column(db.Float())
    forecast2 = db.Column(db.Float())
    forecast3 = db.Column(db.Float())
    forecast4 = db.Column(db.Float())
    forecast5 = db.Column(db.Float())
    forecast6 = db.Column(db.Float())
    forecast7 = db.Column(db.Float())
    forecast8 = db.Column(db.Float())
    forecast9 = db.Column(db.Float())
    
