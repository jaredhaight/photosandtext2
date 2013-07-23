from flask import request, flash
from werkzeug import secure_filename
from flask.ext.restful import Resource, Api
from photosandtext2 import app
from photosandtext2.models import Photo
from utils import render_photo_to_dict, clean_response_data
import os
api = Api(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class api_photo(Resource):
    def get(self,photoID):
        photo = Photo.query.filter_by(id=photoID).first()
        result = render_photo_to_dict(photo)
        return result

class api_photo_list(Resource):
    def get(self):
        photos = Photo.query.all()
        results = []
        for photo in photos:
            result = dict()
            crops = dict()
            result["id"] = photo.id
            result["taken"] = photo.exif_date_taken
            result["uploaded"] = photo.uploaded
            for crop in photo.crops:
                crops[crop.name] = crop.url()
            result["crops"] = crops
            result = clean_response_data(result)
            results.append(result)
        return {"results": results}

    def post(self):
        files = request.files.getlist('files[]')
        results = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['PHOTO_STORE'], filename))
                photo = Photo(image=filename)
                photo.save()
                result = render_photo_to_dict(photo)
                results.append(result)
            else:
                return 'Failed Validation'
        return results

api.add_resource(api_photo_list, '/api/photos/')
api.add_resource(api_photo, '/api/photos/<photoID>/')
