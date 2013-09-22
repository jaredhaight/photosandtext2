import datetime
from flask.ext.restful import abort
from pat2_backend.models import Tag, Gallery

def clean_response_data(res):
    """
    Takes a response and converts non-string values to strings so we can sent it out as JSON
    """
    for key, value in res.iteritems():
        if isinstance(key, datetime.datetime):
            stringKey = key.isoformat()
            res[stringKey] = value
            del(res[key])
        if isinstance(value, datetime.datetime):
            res[key] = value.isoformat()
    return res

def render_photo_to_dict(photo):
    """
    Takes a Photo object, combines it with relevant Crop and Tag objects and converts it to a dict.
    Used to create responses for Photo API
    """
    crops = dict()
    exif=dict()
    tags = []
    gallery = dict()
    gallery["name"] = photo.gallery.name
    gallery["id"] = photo.gallery_id
    gallery["api_url"] = photo.gallery.api_url()
    for crop in photo.crops:
        crops[crop.name] = crop.url()
    for tag in photo.tags:
        result = dict()
        result["name"] = tag.name
        result["id"] = tag.id
        result["api_url"] = tag.api_url()
        tags.append(result)
    exif['aperture'] = photo.exif_aperture
    exif['date_taken'] = photo.exif_date_taken
    exif['focal_length'] = photo.exif_focal
    exif['shutter_speed'] = photo.exif_shutter
    exif['iso'] = photo.exif_iso
    exif = clean_response_data(exif)
    result = clean_response_data({
        "id":photo.id,
        "full_image":photo.url(),
        "crops": crops,
        "tags": tags,
        "uploaded": photo.uploaded,
        "updated":photo.updated,
        "filename": photo.filename(),
        "desc": photo.desc,
        "exif":exif,
        "gallery": gallery
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
    Takes a photo request from POST and makes sure that it fits what we want from a photo object.
    Mainly used to convert random tag strings (ex: {"tags":"foo, bar, banana"}) into an actual list of tags.
    If we're given a string, it will creates tags that don't exist yet.
    """
    tagList = []
    try:
        # If we received a string, look up tags and append them. Create tags as needed.
        print "Tag data type: "+str(type(data["tags"]))
        if isinstance(data["tags"],str) or isinstance(data["tags"],unicode):
            print "Got string of tags: "+data["tags"]
            data["tags"] = data["tags"].split()
            for tag in data['tags']:
                tagLookup = Tag.query.filter_by(name=tag.lower()).first()
                print tagLookup
                if tagLookup:
                    tagList.append(tagLookup)
                else:
                    g = Tag(name=tag.lower())
                    newTag = g.save()
                    print "tag type: "+ str(type(newTag))
                    if isinstance(newTag, Tag):
                        tagList.append(newTag)
                    else:
                        return {"message":newTag}
            print "returning tags as: "+str(data['tags'])
        #if we received a dict, look up tags and append them. Can't create from a dict (yet).
        elif isinstance(data["tags"],list):
            for tag in data["tags"]:
                tagLookup = Tag.query.filter_by(name=tag["name"].lower()).first()
                if tagLookup:
                    tagList.append(tagLookup)
                else:
                    abort(500, message="Could not find the tags you passed. You can create new tags by passing them in as a string")
    except Exception, e:
        abort(500, message="Error while cleaning data", error=str(e))
    data['tags'] = tagList
    if isinstance(data["gallery"],str) or isinstance(data["gallery"],unicode):
        gallery = Gallery.query.filter_by(name=data["gallery"]).first()
        if not gallery:
            gallery = Gallery(name=data["gallery"])
            gallery.save()
        data["gallery"] = gallery
    return data