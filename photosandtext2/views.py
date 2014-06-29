import random, string
from flask import request, redirect, url_for, render_template, send_from_directory, flash, jsonify, g
from flask.ext.login import login_user, login_required, logout_user, current_user
from flask.ext.restless import ProcessingException
from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func
from werkzeug import secure_filename
from photosandtext2 import app, manager, login_manager
from photosandtext2.models.photo import Photo, Crop, Gallery
from photosandtext2.models.user import User
from photosandtext2.utils.general import allowed_file, date_format
from photosandtext2.forms import LoginForm

import os

#User loader for Flask-Login
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

#Serve photos from dev
if app.config['DEBUG']:
    @app.route('/media/<path:filename>')
    def send_file(filename):
        return send_from_directory('/Users/jared/Documents/PycharmProjects/photosandtext2/media', filename)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/page/<int:page>')
def home_view(page = 1):
    header_background = Photo.query.filter_by(favorite=True).order_by(func.random()).first()
    small_header = header_background.crops.filter_by(name="home800").first()
    medium_header = header_background.crops.filter_by(name="display1280").first()
    large_header = header_background.crops.filter_by(name="display1600").first()
    galleries = Gallery.query.filter(Gallery.thumbnails!=None).order_by(Gallery.updated.desc()).paginate(page, 12)
    return render_template('home.html', galleries=galleries, small_header=small_header, medium_header=medium_header, large_header=large_header, user=current_user)

@app.route('/gallery/<int:gallery_id>')
def gallery_view(gallery_id):
    gallery = Gallery.query.get_or_404(gallery_id)
    photos = gallery.photos.order_by(Photo.gallery_pos)
    dates = date_format(photos[0].exif_date_taken, photos[-1].exif_date_taken)
    return render_template('gallery.html', gallery=gallery, photos=photos, dates=dates, user=current_user)

@app.route('/gallery/<int:gallery_id>/photo/<int:gallery_pos>')
def gallery_photo_view(gallery_id, gallery_pos):
    gallery = Gallery.query.get_or_404(gallery_id)
    photos = gallery.photos.order_by(Photo.gallery_pos).paginate(gallery_pos,1,False)
    photo=photos.items[0]
    small_photo = photo.crops.filter_by(name="home800").first()
    medium_photo = photo.crops.filter_by(name="display1280").first()
    large_photo = photo.crops.filter_by(name="display1600").first()
    return render_template('photo_view.html', photos=photos, photo=photo, small_photo=small_photo, medium_photo=medium_photo, large_photo=large_photo, user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            login_user(user)
            print request.args.get("next")
            return redirect(request.args.get("next") or url_for('home_view'))
        flash('Username and password pair not found')
        return redirect(url_for("login_view"))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout_view():
    logout_user()
    return redirect(url_for("home_view"))

#Gallery edit views
@login_required
@app.route('/gallery/new')
def gallery_new_view():
    gallery = Gallery.query.filter_by(name=None, photos=None).first()
    if gallery is None:
        gallery = Gallery()
        gallery.save()
    return redirect('/gallery/edit/#/'+str(gallery.id))

@app.route('/gallery/edit/')
@login_required
def gallery_js_edit_view():
    return render_template('gallery_edit_js.html')

#API Functions
def include_url(result):
    photo = Photo.query.get(result["id"])
    result['url'] = photo.url()
    return result

def edit_crops_for_photo_api_request(result, **kw):
    photoObj = Photo.query.get(result["id"])
    cropsResult = dict()
    for crop in photoObj.crops:
        cropInfo = dict()
        cropInfo["height"] = crop.height
        cropInfo["width"] = crop.width
        cropInfo["url"] = crop.url
        cropsResult[crop.name] =cropInfo
    result["crops"] = cropsResult
    return result

def edit_thumbnails_for_gallery_api_request(result, **kw):
    galleryObj = Gallery.query.get(result["id"])
    thumbResult = dict()
    for thumbnail in galleryObj.thumbnails:
        thumbInfo = dict()
        thumbInfo["height"] = thumbnail.height
        thumbInfo["width"] = thumbnail.width
        thumbInfo["url"] = thumbnail.url
        thumbResult[thumbnail.name] =thumbInfo
    result["thumbnails"] = thumbResult
    return result

def remove_crops_for_photo_api_update(data, **kw):
    try:
        del data["crops"]
    except:
        pass
    pass

def include_crops_for_single_gallery_api_request(result, **kw):
    for photo in result["photos"]:
        photoObj = Photo.query.get(photo["id"])
        cropsResult = dict()
        for crop in photoObj.crops:
            cropInfo = dict()
            cropInfo["height"] = crop.height
            cropInfo["width"] = crop.width
            cropInfo["url"] = crop.url
            cropsResult[crop.name] =cropInfo
        photo["crops"] = cropsResult
    return result

def save_single_gallery_on_update(instance_id, **kw):
    print "Got instance: "+str(instance_id)
    gallery = Gallery.query.get(instance_id)
    gallery.save()
    pass

def remove_crops_for_single_gallery_api_update(data, **kw):
    newPhotos = []
    try:
        for photo in data["photos"]:
            del photo["crops"]
            newPhotos.append(photo)
        del data["photos"]
        data["photos"] = newPhotos
    except:
        pass
    pass

def delete_gallery_api(instance_id, **kw):
    print "Got Instance: "+str(instance_id)
    gallery = Gallery.query.get(instance_id)
    print "Instance Name: "+str(gallery.name)
    gallery.delete()
    print "Instance deleted: "+str(instance_id)
    pass

def auth_func(**kw):
    if not current_user.is_authenticated():
        raise ProcessingException(message="You must be authorized to make this request", status_code=401)

#Dont know if this counts as cheating or not.. kind of brute forcing file uploads into the API
@app.route('/api/v1/galleries/<int:gallery_id>/photos', methods=['POST'])
@login_required
def gallery_upload_view(gallery_id):
    gallery = Gallery.query.get_or_404(gallery_id)
    upload_results = list()
    uploads = request.files.items()
    for upload in uploads:
        if upload[1] and allowed_file(upload[1].filename):
            result = dict()
            prepend = ''.join(random.sample(string.letters, 6))
            filename = secure_filename(prepend+"_"+upload[1].filename)
            upload[1].save(os.path.join(app.config['PHOTO_STORE'], filename))
            photo = Photo(image=filename)
            #TODO: Rethink how this works. Update_photos ends up re-saving the photos a bunch of times. Very wasteful.
            photo.save()
            photo.prepare_photo()
            gallery.add_photo(photo)
            result['status'] = 'success'
            result['id'] = photo.id
            upload_results.append(result)
    resp = dict()
    resp['status'] = 'success'
    resp['objects'] = upload_results
    print resp
    gallery.save()
    return jsonify(resp)

@app.route('/api/v1/galleries/<int:gallery_id>/status')
def gallery_status_view(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    resp = dict()
    resp['gallery_status'] = gallery.status()
    resp['id'] = gallery.id
    return jsonify(resp)

manager.create_api(
    Photo,
    methods=['GET','POST','DELETE','PATCH','PUT'],
    url_prefix='/api/v1',
    collection_name='photos',
    results_per_page=20,
    preprocessors={
        'PUT_SINGLE':[remove_crops_for_photo_api_update, auth_func],
        'POST':[auth_func],
        'PUT':[auth_func],
        'DELETE':[auth_func],
        'PATCH':[auth_func]
    },
    postprocessors={
        'GET_SINGLE':[include_url,edit_crops_for_photo_api_request]
    }
)

manager.create_api(
    Gallery,
    methods=['GET','POST','DELETE','PATCH','PUT'],
    url_prefix='/api/v1',
    collection_name='galleries',
    results_per_page=20,
    preprocessors={
        'PUT_SINGLE':[remove_crops_for_single_gallery_api_update, auth_func],
        'POST':[auth_func],
        'PUT':[auth_func],
        'DELETE':[auth_func, delete_gallery_api],
        'PATCH':[auth_func]
    },
    postprocessors={
        'GET_MANY': [],
        'GET_SINGLE':[include_crops_for_single_gallery_api_request]
    }
)