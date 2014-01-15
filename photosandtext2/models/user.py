from flask.ext.login import UserMixin
from photosandtext2 import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    password = db.Column(db.Unicode)
