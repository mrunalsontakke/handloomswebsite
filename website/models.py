from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150)) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    company_Name = db.Column(db.String(150))
    contact = db.Column(db.String(10)) 
    description = db.Column(db.String(500))
    state = db.Column(db.String(20))
    address = db.Column(db.String(200))
    image = db.Column(db.String(200), default='website/static/images/profile/00default.png')
    product_name = db.Column(db.String(100))
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150)) 
    contact = db.Column(db.String(10)) 
    role = db.Column(db.String(10))
    message = db.Column(db.String(500))
    
class Costumer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150)) 
    password = db.Column(db.String(150))
    contact = db.Column(db.String(10)) 
    company_Name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.String(100))
    status = db.Column(db.String(10)) 