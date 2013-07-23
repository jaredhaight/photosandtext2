from flask import url_for
import datetime

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
    crops = dict()
    galleries = dict()
    for crop in photo.crops:
        crops[crop.name] = crop.url()
    for gallery in photo.galleries:
        galleries[gallery.name] = url_for("get_gallery",gallerySlug=gallery.slug)
    url = url_for('return_photo', photoID=photo.id, _external=True)
    print(url)
    result = clean_response_data({"id":photo.id, "full_image":photo.url(), "crops": crops, "url": url, "uploaded": photo.uploaded, "updated":photo.updated})
    return result