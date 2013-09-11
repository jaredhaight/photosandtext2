from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('pat2_backend.settings.DevConfig')

db = SQLAlchemy(app)

import pat2_backend.api.views