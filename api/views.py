from flask import url_for
from flask.ext.restful import Resource, Api
from photosandtext2 import app
from photosandtext2.models import Photo
from utils import clean_response_data

api = Api(app)

class api_get_photo(Resource):
    def get(self,photoID):
        photo = Photo.query.filter_by(id=photoID).first()
        crops = dict()
        galleries = dict()
        for crop in photo.crops:
            crops[crop.name] = crop.url()
        for gallery in photo.galleries:
            galleries[gallery.name] = url_for("get_gallery",gallerySlug=gallery.slug)
        url = url_for('return_photo', photoID=photo.id, _external=True)
        print(url)
        result = clean_response_data({"id":photo.id, "title":photo.title, "full_image":photo.url(), "crops": crops, "url": url, "created": photo.created, "updated":photo.updated})
        return result


api.add_resource(api_get_photo, '/api/photo/<photoID>/')