import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/pat2'
    PHOTO_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/photos'
    PHOTO_BASE_URL = '/media/photos'
    RAW_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/raw'
    CROP_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/crops'
    CROP_BASE_URL = '/media/crops'
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
    #TODO - Get Secret Key working from environment variable. Might be an issue with OSX or Pycharm
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'ITsAS3cr3t!P4dding0utTHISBecauS31tS0uldB3loooonnnngggg'
    DEBUG = False

class DevConfig(Config):
    DEBUG = True

