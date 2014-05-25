from photosandtext2.settings import Config

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/pat2'
    PHOTO_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/photos'
    RAW_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/raw'
    CROP_STORE = '/Users/jared/Documents/PycharmProjects/photosandtext2/media/crops'
    DEBUG = True