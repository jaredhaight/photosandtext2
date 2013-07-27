from flask import url_for
import datetime
from photosandtext2.models import Gallery

def clean_response_data(res):
    """
    Cleans a dict so that it can be sent out through Restful.
    """
    for key, value in res.iteritems():
        if isinstance(key, datetime.datetime):
            stringKey = key.strftime("%Y-%m-%d %H:%M:%S")
            res[stringKey] = value
            del(res[key])
        if isinstance(value, datetime.datetime):
            res[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return res

def render_photo_to_dict(photo):
    """
    Takes a Photo object, crunches it and spits out a dict for Restful response.
    """
    crops = dict()
    galleries = []
    for crop in photo.crops:
        crops[crop.name] = crop.url()
    for gallery in photo.galleries:
        result = dict()
        result["name"] = gallery.name
        result["id"] = gallery.id
        result["api_url"] = gallery.api_url()
        result["site_url"] = gallery.site_url()
        galleries.append(result)
    result = clean_response_data({
        "id":photo.id,
        "url": photo.site_url(),
        "full_image":photo.url(),
        "crops": crops,
        "galleries": galleries,
        "uploaded": photo.uploaded,
        "updated":photo.updated
    })
    return result

def get_data_from_request(request):
    """
    Takes a request and sanitizes the data whether it's JSON or a Form.
    """
    if request.json:
        data = request.json
    else:
        data = dict()
        for key,value in request.form.iteritems():
            data[key] = value
    return data

def clean_photo_data(data):
    """
    Takes a data dict and makes some sense of it.
    """
    galleryList = []
    data["galleries"] = data["galleries"].split()
    for gallery in data['galleries']:
        galleryLookup = Gallery.query.filter_by(name=gallery.lower()).first()
        print galleryLookup
        if galleryLookup:
            galleryList.append(galleryLookup)
        else:
            g = Gallery(name=gallery.lower())
            print "g: "+str(g)
            newGallery = g.save()
            print "gallery type: "+ str(type(newGallery))
            if isinstance(newGallery, Gallery):
                galleryList.append(newGallery)
            else:
                return {"message":newGallery}
    data['galleries'] = galleryList
    return data