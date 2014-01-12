from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('photosandtext2.settings.DevConfig')

db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)