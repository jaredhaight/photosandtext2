from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('photosandtext2.settings.DevConfig')

db = SQLAlchemy(app)

import photosandtext2.views
import photosandtext2.api.views