import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask.ext.login import LoginManager

pat2_env = os.environ.get('PAT2_ENV')
app = Flask(__name__)
print pat2_env
if pat2_env == 'DEV':
    app.config.from_object('photosandtext2.settings.dev.DevConfig')
if pat2_env == 'PROD':
    app.config.from_object('photosandtext2.settings.prod.ProdConfig')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login_view"
manager = APIManager(app, flask_sqlalchemy_db=db)
login_manager.init_app(app)
