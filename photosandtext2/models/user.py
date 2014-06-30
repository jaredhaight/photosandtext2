from flask.ext.login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from photosandtext2 import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

