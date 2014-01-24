import re
from unicodedata import normalize
from photosandtext2 import app, db
from photosandtext2.models.photo import *
from photosandtext2.models.user import *
import datetime

ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]

def init_env():
    """
    Used to initialize the environment.
    """
    crop1 = CropSettings(name="thumb200",height=200,width=200)
    crop2 = CropSettings(name="thumb400",height=400,width=400)
    crop3 = CropSettings(name="home400",height=0,width=400)
    crop4 = CropSettings(name="home600",height=0,width=600)
    crop5 = CropSettings(name="home800",height=0,width=800)
    crop6 = CropSettings(name="display1280",height=0,width=1280)
    crop8 = CropSettings(name="display_t",height=0,width=100)
    crop9 = CropSettings(name="display_m",height=0,width=240)
    crop10 = CropSettings(name="display_n",height=0,width=320)
    crop11 = CropSettings(name="display",height=0,width=500)
    crop12 = CropSettings(name="display_z",height=0,width=640)
    crop13 = CropSettings(name="display_c",height=0,width=800)
    crop14 = CropSettings(name="display_b",height=0,width=1024)
    for crop in (crop1, crop2, crop3, crop4, crop5, crop6, crop7, crop8, crop9, crop10, crop11, crop12, crop13, crop14):
        db.session.add(crop)
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS