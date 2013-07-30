from flask import url_for
import datetime
from photosandtext2.models import Tag

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
    tags = []
    for crop in photo.crops:
        crops[crop.name] = crop.url()
    for tag in photo.tags:
        result = dict()
        result["name"] = tag.name
        result["id"] = tag.id
        result["api_url"] = tag.api_url()
        result["site_url"] = tag.site_url()
        tags.append(result)
    result = clean_response_data({
        "id":photo.id,
        "url": photo.site_url(),
        "full_image":photo.url(),
        "crops": crops,
        "tags": tags,
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
    try:
        tagList = []
        if isinstance(data["tags"],str):
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
        data['tags'] = tagList
        print "returning tags as: "+str(data['tags'])
    except:
        pass
    return data