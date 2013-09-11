import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/pat2'
    PHOTO_STORE = '/Users/jared/Documents/PycharmProjects/pat2_backend/media/photos'
    PHOTO_BASE_URL = '/media/photos'
    RAW_STORE = '/Users/jared/Documents/PycharmProjects/pat2_backend/media/raw'
    CROP_STORE = '/Users/jared/Documents/PycharmProjects/pat2_backend/media/crops'
    CROP_BASE_URL = '/media/crops'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

class DevConfig(Config):
    DEBUG = True

