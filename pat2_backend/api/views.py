from flask import request
from werkzeug import secure_filename
from flask.ext.restful import Resource, Api, abort
from pat2_backend import app
from pat2_backend.models import Photo, Tag, Gallery
from utils import render_photo_to_dict, clean_response_data, get_data_from_request, clean_photo_data
import os
api = Api(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class api_photo(Resource):
    def get(self,photoID):
        photo = Photo.query.get(photoID)
        if not photo:
            return abort(404)
        result = render_photo_to_dict(photo)
        return result

    def post(self,photoID):
        photo = Photo.query.get(photoID)
        edited = False
        error = None
        data = get_data_from_request(request)
        cleanData = clean_photo_data(data)
        print "Received CleanData: "+str(cleanData)

        try:
            photo.desc = cleanData['desc']
            edited = True
        except:
            abort(500, message="Error while applying desc to photo", error=str(e))

        try:
            print "Clean photo tags: "+str(cleanData['tags'])
            photo.tags = cleanData['tags']
            edited = True
        except Exception, e:
            abort(500, message="Error applying tags to photo.", error=str(e))

        if edited is True:
            photo.save()
            return api_photo.get(self, photoID = photo.id)

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
        return {"count": len(results), "results": results}

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
                return abort(400, message='Invalid File Type')
        return {"count": len(results), "results":results}

class api_tag(Resource):
    def get(self, tagID):
        tag = Tag.query.filter_by(id=tagID).first()
        photos = []
        result = dict()
        result["id"] = tag.id
        result["name"] = tag.name
        result['slug'] = tag.slug
        result["site_url"] = tag.site_url()
        result["api_url"] = tag.api_url()
        for p in tag.photos:
            photo = dict()
            photo["id"] = p.id
            photo["url"] = p.url()
            photo["site_url"] = p.site_url()
            photo["api_url"] = p.api_url()
            crops = dict()
            for crop in p.crops:
                crops[crop.name] = crop.url()
            photo["crops"] = crops
            photos.append(photo)
        result["photos"] = photos
        return result

class api_tags_list(Resource):
    def get(self):
        tags = Tag.query.all()
        results = []
        for tag in tags:
            result = dict()
            result["id"] = tag.id
            result["name"] = tag.name
            result['slug'] = tag.slug
            result["site_url"] = tag.site_url()
            result["api_url"] = tag.api_url()
            results.append(result)
        return {"count": len(results), "results":results}

class api_gallery(Resource):
    def get(self, galleryID):
        gallery = Gallery.query.filter_by(id=galleryID).first()
        photos = []
        result = dict()
        for photo in gallery.photos:
            r = dict()
            crops = dict()
            r["id"] = photo.id
            r["taken"] = photo.exif_date_taken
            r["uploaded"] = photo.uploaded
            for crop in photo.crops:
                crops[crop.name] = crop.url()
            r["crops"] = crops
            r = clean_response_data(r)
            photos.append(r)
        result["id"] = gallery.id
        result["name"] = gallery.name
        result["photos"] = photos
        result["site_url"] = gallery.site_url()
        result["api_url"] = gallery.api_url()
        return result


class api_gallery_list(Resource):
    def get(self):
        galleries = Gallery.query.all()
        results = []
        for gallery in galleries:
            result = dict()
            result["id"] = gallery.id
            result["name"] = gallery.name
            result["api_url"] = gallery.api_url()
            result["site_url"] = gallery.site_url()
            results.append(result)
        return {"count": len(results), "results":results}

api.add_resource(api_photo_list, '/api/photos')
api.add_resource(api_photo, '/api/photos/<photoID>')
api.add_resource(api_tags_list, '/api/tags')
api.add_resource(api_tag, '/api/tags/<tagID>')
api.add_resource(api_gallery_list, '/api/galleries')
api.add_resource(api_gallery, '/api/galleries/<galleryID>')
