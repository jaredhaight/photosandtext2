from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('photosandtext2.settings.DevConfig')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login_view"
manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager.init_app(app)
